# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 10:25:57 2019

@author: Admin
"""

import cv2
import numpy as np
path='textphoto.jpg'
#def reconizedpoint(path)
img=cv2.imread(path)

    # 缩小图像  
height, width = img.shape[:2]  
size = (int(width*1), int(height*1))  
img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)  

gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)#转灰度图
hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)#转hsv色彩空间


#get black area
#ret,thresh=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C ,cv2.THRESH_BINARY,11) #阈值化处理，大于148的变为白色（0为黑色，255为白），输入灰度图
ret,thresh=cv2.threshold(gray,80,255,cv2.THRESH_BINARY) #阈值化处理，大于148的变为白色（0为黑色，255为白），输入灰度图
mask=thresh#构建掩模
black=cv2.bitwise_and(hsv,hsv,mask=mask)#hsv与掩模进行与运算，提取黑色区域

#将黑色区域进行二值化处理
black_gray=cv2.cvtColor(black,cv2.COLOR_HSV2BGR)#hsv转bgr
black_gray=cv2.cvtColor(black_gray,cv2.COLOR_BGR2GRAY)#bgr转灰度图
          
#binaryzation
_, thresh=cv2.threshold(black_gray,10,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)#阈值化处理，大于10的变为白色
img_morph=cv2.morphologyEx(thresh,cv2.MORPH_OPEN,(3,3))#开运算，去噪声
img_morph=cv2.erode(img_morph,(3,3),img_morph,iterations=2)#腐蚀图像
morph=cv2.dilate(img_morph,(3,3),img_morph,iterations=2)#膨胀图像


#获取中心区域轮廓及坐标 
img_cp=morph.copy()#复制原来的图像到一张新的图像上

cnts,_=cv2.findContours(img_cp,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)#轮廓检测，输入二值图，cnts为返回的轮廓
anum=len(cnts)
cutnum=0
center=np.zeros([anum,2],dtype=np.int32)
for i in range(0,anum):
    cnt_second=sorted(cnts,key=cv2.contourArea,reverse=True)[i]#按照轮廓的面积从大到小进行排序，输出第a个轮廓
    box =cv2.minAreaRect(cnt_second)#最小矩形面积
    points=np.int0(cv2.boxPoints(box))#查找旋转矩形的 4 个顶点，points为四个顶点坐标
    mask=np.zeros(gray.shape,np.uint8)#生成灰度图同样大小的零矩阵，uint8是无符号八位整型,表示范围是[0, 255]的整数
    mask=cv2.drawContours(mask,[points],-1,255,2)#进行轮廓的颜色填充，第一个参数是一张图片，可以是原图或者其他。第二个参数是轮廓，一个列表。第三个参数是对轮廓（第二个参数）的索引，当需要绘制独立轮廓时很有用，若要全部绘制可设为-1。接下来的参数是轮廓的颜色和厚度。
    p1x,p1y=points[0,0],points[0,1]
    p3x,p3y=points[2,0],points[2,1]
    center_x,center_y=(p1x+p3x)/2,(p1y+p3y)/2#得到中心坐标
    cutsize=75
    if center_y<cutsize or center_y>height-cutsize:
        cutnum=cutnum+1
        continue
    center[i][0]=int(center_x)
    center[i][1]=int(center_y)

centernew=np.zeros([anum-cutnum,2],dtype=np.int32)
newnum=0
for i in range(0,anum):
    if center[i][0]!=0:
        centernew[newnum][0]=center[i][0]
        centernew[newnum][1]=center[i][1]
        newnum=newnum+1
anum=anum-cutnum
center=centernew

        


cv2.imshow('img',morph)
cv2.waitKey(5000)
cv2.destroyAllWindows()



img2=cv2.imread(path)
for i in range(0,anum):
    b = (255,0,0)
    p=(centernew[i][0],centernew[i][1])
    img2=cv2.circle(img2,p,50,b,2)
cv2.imwrite('trytextphoto.jpg',img2)
 # return center
