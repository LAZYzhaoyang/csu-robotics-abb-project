import cv2
import numpy as np
import sys
import math
import glob

def image_pre_deal(imgc1,W=1,isgray=False,isauto=True):
    # imgc1 待处理图像
    # w 处理图像时对图像进行缩放处理的比例
    # isgray 决定是否使用灰度图进行处理，若为否则选择hsv图像第3通道的图像值进行处理
    # isauto 决定是否使用自动阈值

    # 图像缩放处理
    height1, width1 = imgc1.shape[:2]
    size = (int(width1*W), int(height1*W))
    imgc1= cv2.resize(imgc1, size, interpolation=cv2.INTER_AREA)
    # 生成灰度图和hsv图像，默认选择hsv图像进行处理
    gray=cv2.cvtColor(imgc1,cv2.COLOR_BGR2GRAY)
    hsv=cv2.cvtColor(imgc1,cv2.COLOR_BGR2HSV)
    trans_image=hsv[:,:,2]
    if isgray:
        trans_image=gray
    # 阈值化处理
    if isauto:
        thresh=cv2.adaptiveThreshold(trans_image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C ,cv2.THRESH_BINARY,7,30) 
    else:
        ret,thresh=cv2.threshold(gray,170,255,cv2.THRESH_BINARY) 
    mask=thresh
    # 将hsv图像与mask进行与运算，并进行二值化运算
    black=cv2.bitwise_and(hsv,hsv,mask=mask)
    black_gray=cv2.cvtColor(black,cv2.COLOR_HSV2BGR)#二值图转bgr通道
    black_gray=cv2.cvtColor(black_gray,cv2.COLOR_BGR2GRAY)#bgr转灰度图
    # 将得到的图再次进行阈值化处理
    _, thresh=cv2.threshold(black_gray,10,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    img_morph=cv2.morphologyEx(thresh,cv2.MORPH_OPEN,(3,3))# 开运算，降噪处理
    img_morph=cv2.erode(img_morph,(3,3),img_morph,iterations=2)# 腐蚀图像
    morph=cv2.dilate(img_morph,(3,3),img_morph,iterations=2)# 膨胀处理
    cv2.imwrite('morph.jpg',morph)
    return morph
"""
def restore_image()
"""