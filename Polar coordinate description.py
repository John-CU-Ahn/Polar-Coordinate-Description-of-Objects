# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 12:05:46 2023

@author: jahn39
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import nd2
from tifffile import tifffile

def creatLineIterator(P1,P2,img):
   imageH = img.shape[0]
   imageW = img.shape[1]
   P1X = P1[0]
   P1Y = P1[1]
   P2X = P2[0]
   P2Y = P2[1]

   #difference and absolute difference between points
   #used to calculate slope and relative location between points
   dX = P2X - P1X
   dY = P2Y - P1Y
   
   #predefine numpy array for output based on distance between points
   dXa = np.abs(dX)
   dYa = np.abs(dY)
   
   shape = np.maximum(dYa,dXa)
   itbuffer = np.empty((int(shape),3),dtype=np.float32)
   
   itbuffer.fill(np.nan)
   
   #Obtain coordinates along the line using a form of Bresenham's algorithm
   negY = P1Y > P2Y
   negX = P1X > P2X
   if P1X == P2X: #vertical line segment
       itbuffer[:,0] = P1X
       if negY:
           itbuffer[:,1] = np.arange(P1Y - 1,P1Y - dYa - 1,-1)
       else:
           itbuffer[:,1] = np.arange(P1Y+1,P1Y+dYa+1)              
   elif P1Y == P2Y: #horizontal line segment
       itbuffer[:,1] = P1Y
       if negX:
           itbuffer[:,0] = np.arange(P1X-1,P1X-dXa-1,-1)
       else:
           itbuffer[:,0] = np.arange(P1X+1,P1X+dXa+1)
   else: #diagonal line segment
       steepSlope = dYa > dXa
       if steepSlope:
           slope = dX/dY
           if negY:
               itbuffer[:,1] = np.arange(P1Y-1,P1Y-dYa-1,-1)
           else:
               itbuffer[:,1] = np.arange(P1Y+1,P1Y+dYa+1)
           itbuffer[:,0] = (slope*(itbuffer[:,1]-P1Y)).astype(np.int) + P1X
       else:
           slope = dY/dX
           if negX:
               itbuffer[:,0] = np.arange(P1X-1,P1X-dXa-1,-1)
           else:
               itbuffer[:,0] = np.arange(P1X+1,P1X+dXa+1)
           itbuffer[:,1] = (slope*(itbuffer[:,0]-P1X)).astype(np.int) + P1Y

   #Remove points outside of image
   colX = itbuffer[:,0]
   colY = itbuffer[:,1]
   itbuffer = itbuffer[(colX >= 0) & (colY >=0) & (colX<imageW) & (colY<imageH)]

   #Get intensities from img ndarray
   itbuffer[:,2] = img[itbuffer[:,1].astype(np.uint),itbuffer[:,0].astype(np.uint)]

   return itbuffer

def lineXYIntensityPoints(line):
    #This function is just extracting x,y,and intensity lists from the creatLineIterator function
    xlist = []
    ylist = []
    pixlist = []
    for i in line:
        xpoint = i[0]
        xlist.append(xpoint)
    for i in line:
        ypoint = i[1]
        ylist.append(ypoint)
    for i in line:
        pixpoint = i[2]
        pixlist.append(pixpoint)
    return xlist, ylist, pixlist

def polar2cart(r, theta):
    #polar to cartesian coordinates
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y

#radius is the desired radius for the line profile
#thetas is the list of angles that are going to be surveyed
#cent_x is the x coordinate of the center of the pattern of interest
#cent_y, ditto but with y
#img is the array of pixels that are going to be analyzed
def genEndCoord(radius,thetas,cent_x,cent_y):
    x2_list = []
    y2_list = []

    #this for loop is going to generate the x2,y2 points for each theta based on the specified radius
    for theta in thetas:
        x,y = polar2cart(radius,theta)
        
        x2 = int(x + cent_x)
        y2 = int(y + cent_y)
        
        x2_list.append(x2)
        y2_list.append(y2)
    return x2_list,y2_list

def linProfSweep2(x2_list,y2_list,cent_x,cent_y,thetas,img):
    #this for loop is going to go through each of the x2,y2 generated points to calculate the line profile
    #for each theta
    
    #int_list is a list of intensity lists for each theta angle
    #x_list is the list of x coordinates surveyed
    #y_list is the list of y coordinates surveyed
    int_list = []
    x_list = []
    y_list = []
    for i,j in zip(x2_list,y2_list):
        line = creatLineIterator([i,j],[cent_x,cent_y],img)
        xlist, ylist, intlist = lineXYIntensityPoints(line)
        
        x_list_integers = []
        y_list_integers = []
        
        for b in xlist:
            x_list_integers.append(int(b))
        
        for c in ylist:
            y_list_integers.append(int(c))

        int_list.append(intlist)
        x_list.append(x_list_integers)
        y_list.append(y_list_integers)

    return int_list,x_list,y_list

def genSingleLineProfDFs(int_list,rads):
        #This int_list is a list of line profile lists
        #This function will generate one dataframe of one frame of theta values vs line profile pixel intensities
        Frame_index = []
        #rads = np.linspace(0,np.pi*2,360)
        for i in rads:
            frnm = 'Radians ' + str(i)
            
            Frame_index.append(frnm)
        
        #Creating the list of lists of radii values collected from each frame
        #list_Radii was imported from the Movie Analysis file
        df_load = []
        for i in int_list:
            df_load.append(i)
        
        df = pd.DataFrame(df_load, index=Frame_index)
        return df


def radiiThreshold(data, threshold):
    
    #This for loop will generate the total number of 255s in original list
    c = -1
    clist = []
    for i in data:
        if i == 255:
            c = c + 1
            clist.append(c)
        else:
            c = c + 1
    clist_np = np.asarray(clist)
    shp = clist_np.shape[0]
    
    #This for loop should calculate the index point in the list at which the threshold is met
    c2 = -1
    c2_list = []
    for i in data:
        if i == 255:
            c2 = c2 + 1
            
            #new list that should exclude all of the data points before the index point 'i'
            sliced_list = data[c2:]
            
            #new list to which the number of 255s surveyed in sliced_list should be collected
            whitepix_list = []
            c3 = -1
            for j in sliced_list:
                if j == 255:
                    c3 = c3 + 1
                    whitepix_list.append(c3)
                else:
                    c3 = c3 + 1
            whitepix_list_np = np.asarray(whitepix_list)
            shp2 = whitepix_list_np.shape[0]
            
            #The i needs to be less than or equal to the specified threshold
            #And then the index at which the 255 is located should be recorded and stored in c2_list
            #That index number will then be the radius?
            #No, it should be divided by the shape of the list and then multiplied by the specified survey radius
            #from the other functions in the function library
            if shp2/shp <= threshold:
                c2_list.append(c2)
        else:
            c2 = c2 + 1
    if len(c2_list) == 0:
        c2_list.append(0)
    #print(c2_list)    
    return c2_list[0]
#Ld is the length of the data set
#per is the percentage of the calculated radius relative to Ld
#radii_num needs to be subtracted by 1 because the number that the position represents should be included
#in the radius length

def scaledRadii(data,radii_num,max_len):
    Ld = len(data)
    #print(Ld)
    per = (radii_num-1)/Ld
    tru_rad = max_len - max_len*per
    return tru_rad

#surv_radius in pixel values
#thresh is the threshold at which the radius will be set
#dataframe is a single frame of a video that has 360 radian values and however many pixels were collected
#in the line profile
def iterOneFrame(dataframe,thresh):
    shp = dataframe.shape
    rows = shp[0]
    max_len = shp[1]
    #print(max_len)
    list_radii = []
    
    z = -1
    for i in range(rows):
        z = z + 1
        llist = dataframe.iloc[i,:]
        #print(llist)
        sli_list = llist.values.tolist()
        cleaned_sli_list = [x for x in sli_list if str(x) != 'nan']
        clean_list_new = pd.DataFrame(cleaned_sli_list)
                
        r = radiiThreshold(llist,thresh)
        x = scaledRadii(clean_list_new,r,max_len)
        
        list_radii.append(x)
    #print(list_radii)
    return list_radii


def collectRadii(current_image, rads, survey_radius, thresh):
    #determining kernel size could be necessary to filter out noise
    kernel = np.ones((5, 5), np.uint8)
    
    imagem = cv2.bitwise_not(current_image)
    img_dil = cv2.dilate(imagem, kernel, iterations=1)
    contours, hierarchies = cv2.findContours(img_dil, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    #contours might be detected incorrectly? Depends on upstream denoising
    v = contours[[len(i) for i in contours].index(max([len(i) for i in contours]))] 
    
    M = cv2.moments(v)
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    
    
    x2_list,y2_list = genEndCoord(survey_radius,rads,cx,cy)
    int_list,x_list,y_list = linProfSweep2(x2_list,y2_list,cx,cy,rads,img_dil)
    one_frame_line_prof = genSingleLineProfDFs(int_list,rads)
    
    list_radii = iterOneFrame(one_frame_line_prof,thresh)
    
    return list_radii
    
#Uncomment the line below and add the directory of your tif image stack    
#df = tifffile.imread()

time,x,y = df.shape

#Be careful with survey radius
#If it's too large and it goes out of frame, an error will pop up
#If it's too small, won't detect tentacles
survey_radius = 60
#thresh, can filter out some noise along line profiles
thresh = 0.95
rads = np.linspace(0,np.pi*2,360)


rad_df = []
for i in range(time):
    print(i)
    current_image = df[i,:,:]*255
    list_radii = collectRadii(current_image, rads, survey_radius, thresh)
    rad_df.append(list_radii)

rad_df = pd.DataFrame(rad_df)

#Uncomment the line below and save the csv with a title of your choice
#rad_df.to_csv(".csv")




