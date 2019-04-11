# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 18:10:59 2019

@author: Admin
"""

import cv2
import numpy as np
import glob


"""
mask=cv2.imread('009.jpg')
point=np.array([[1671, 2926],
                 [2782, 3100],
                 [2405, 2874],
                 [2309, 2429],
                 [2113, 1879],
                 [2732, 2166],
                 [2717, 3047],
                 [2739, 2996]])
for i in range(0,len(point)):
    green = (0,0,0)
    center=(point[i][0],point[i][1])
    mask=cv2.circle( mask,center,50,green,2)  
cv2.imwrite('newworld.png',mask)
a=range(0,7)
b=len(a)
"""

images1 = glob.glob('*.bmp')
num=1
for fname in images1:
    img=cv2.imread(fname)
    cv2.imwrite(str(num)+'.png',img)
    num=num+1

#center=textcode2.reconizedpoint(path)
"""
sendwords = str(1000) + ',' + str(2000) + ',' + str(0) + ',' + str(300) + ',' + str(1) + ',' + str(1) + '/0D'
"""