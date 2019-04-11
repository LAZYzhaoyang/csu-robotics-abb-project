import cv2
import numpy as np
import socket
import time
import sys
import math
import glob

def plength(p1,p2):
    dx=p1[0]-p2[0]
    dy=p1[1]-p2[1]
    l=math.sqrt(dx*dx+dy*dy)
    return l

w=0.1
path1='textphoto2.jpg'
imgc1=cv2.imread(path1)  
height1, width1 = imgc1.shape[:2]
size = (int(width1*w), int(height1*w))
imgc1= cv2.resize(imgc1, size, interpolation=cv2.INTER_AREA)
gray=cv2.cvtColor(imgc1,cv2.COLOR_BGR2GRAY)
hsv=cv2.cvtColor(imgc1,cv2.COLOR_BGR2HSV)
#get black area
#ret,thresh=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,3) 
ret,thresh=cv2.threshold(gray,125,255,cv2.THRESH_BINARY) 
mask=thresh
black=cv2.bitwise_and(hsv,hsv,mask=mask)

black_gray=cv2.cvtColor(black,cv2.COLOR_HSV2BGR)
black_gray=cv2.cvtColor(black_gray,cv2.COLOR_BGR2GRAY)
#binaryzation
_, thresh=cv2.threshold(black_gray,10,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
img_morph=cv2.morphologyEx(thresh,cv2.MORPH_OPEN,(3,3))
img_morph=cv2.erode(img_morph,(3,3),img_morph,iterations=2)
morph=cv2.dilate(img_morph,(3,3),img_morph,iterations=2)
cv2.imwrite('morph.jpg',morph)

img_cp=morph.copy()
cnts,_=cv2.findContours(img_cp,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
anum=len(cnts)
bnum=anum
cutnum=0
center=np.zeros([anum,2],dtype=np.int32)
pointcorner=np.zeros([anum,8],dtype=np.int32)
for i in range(0,anum):
    cnt_second=sorted(cnts,key=cv2.contourArea,reverse=True)[i]
    box =cv2.minAreaRect(cnt_second)
    points=np.int0(cv2.boxPoints(box))
    mask=np.zeros(gray.shape,np.uint8)
    
    mask=cv2.drawContours(mask,[points],-1,255,2)
    p1x,p1y=int(points[0,0]/w),int(points[0,1]/w)
    p2x,p2y=int(points[1,0]/w),int(points[1,1]/w)
    p3x,p3y=int(points[2,0]/w),int(points[2,1]/w)
    p4x,p4y=int(points[3,0]/w),int(points[3,1]/w)

    center_x,center_y=(p1x+p3x)/2,(p1y+p3y)/2
    cutsize=2
    if center_y<cutsize or center_y>height1-cutsize:
        cutnum=cutnum+1
        continue
    if center_x<cutsize or center_x>width1-cutsize:
        cutnum=cutnum+1
        continue
    center[i][0]=int(center_x)
    center[i][1]=int(center_y)
    pointcorner[i,:]=[p1x,p1y,p2x,p2y,p3x,p3y,p4x,p4y]
centernew=np.zeros([anum-cutnum,2],dtype=np.int32)
pointcornernew=np.zeros([anum-cutnum,8],dtype=np.int32)
newnum=0
for i in range(0,anum):
    if center[i][0]!=0:
        centernew[newnum][0]=center[i][0]
        centernew[newnum][1]=center[i][1]
        pointcornernew[newnum,:]=pointcorner[i,:]
        newnum=newnum+1
anum=anum-cutnum
center=centernew
pointcorner=pointcornernew
print pointcorner
cosp=np.zeros((anum))
acosp=np.zeros_like(cosp)
img2=cv2.imread(path1)
for i in range(0,anum):
    b = (255,0,0)
    r = (0,0,255)
    g = (0,255,0)
    b1 = (128,128,0)
    b2 = (0,128,128)
    b3 = (128,0,128)
    p=(centernew[i][0],centernew[i][1])
    p1=(pointcorner[i,0],pointcorner[i,1])
    p2=(pointcorner[i,2],pointcorner[i,3])
    p3=(pointcorner[i,4],pointcorner[i,5])
    p4=(pointcorner[i,6],pointcorner[i,7])
    img2=cv2.circle(img2,p,1,b,2)
    img2=cv2.circle(img2,p1,2,r,2)
    img2=cv2.circle(img2,p2,2,g,2)
    img2=cv2.circle(img2,p3,2,b1,2)
    img2=cv2.circle(img2,p4,2,b2,2)
    l12=plength(p1,p2)
    l14=plength(p1,p4)
    if l12>l14 :
        cosp[i]=(p2[0]-p1[0])/l12
    else:
        cosp[i]=(p4[0]-p1[0])/l14
    acosp[i]=(math.acos(cosp[i])/math.pi)*180

print 'cosp'
print cosp

print 'acosp'
print acosp

cv2.imwrite('trytextphoto.jpg',img2)
