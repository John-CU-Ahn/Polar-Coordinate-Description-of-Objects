# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 12:24:39 2023

@author: jahn39
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import nd2
from tifffile import tifffile

#Uncomment the below line and add the directory to the csv file of the radii
#rad_df = pd.read_csv()

rows,cols = rad_df.shape

#Add a save directory for the polar coordinate graphs
#save_directory = ""

for i in range(rows):
    print(i)
    plt.plot(rad_df.iloc[i,:])
    #You can add a y limit for consistency
    #plt.ylim(())
    plt.title("frame " + str (i))
    plt.savefig(save_directory + "/frame " + str(i) + ".png")
    plt.show()

