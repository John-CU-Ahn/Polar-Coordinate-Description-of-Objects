# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 06:16:55 2023

@author: jahn39
"""

import cv2
from cv2 import VideoWriter, VideoWriter_fourcc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from nd2reader import ND2Reader
from natsort import natsorted
import os

#Add a file directory with the frames in the line below
file_directory = ""
#Write a name of the movie file as an mp4
name = ".mp4"


file_li = os.listdir(file_directory)
sfile_li = natsorted(file_li)
sfile_list = [i for i in sfile_li if 'frame' in i]

new_frames = []
for filename in sfile_list:
    file_path = os.path.join(file_directory,filename)
    print(filename)

    frame = cv2.imread(file_path)
    rows,cols,ch = frame.shape
    width = cols
    height = rows
    
    new_frames.append(frame)
    
tot = len(new_frames)
video_length = 10
FPS = int(tot/video_length)



fourcc = VideoWriter_fourcc(*'mp4v')
video = VideoWriter(name, fourcc, float(FPS), (width, height), True)

for i in new_frames:
    frame = np.uint8(i)
    #print(frame)
    video.write(frame)

video.release()