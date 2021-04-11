import cv2
import numpy as np
import sys
import math
import glob

def plength(p1,p2):
    dx=p1[0]-p2[0]
    dy=p1[1]-p2[1]
    l=math.sqrt(dx*dx+dy*dy)
    return l

def get_center(image,w=1,cutsize=150):
    # image 待测图像
    # w 图像缩放比例
    # cutsize 中心点裁剪范围 当检测出的中心点距离图像边缘的距离小于这个值时会被自动跳过不取
    img_cp=image
    height1, width1 = img_cp.shape[:2]
    # 获取检测出的目标轮廓
    cnts,_=cv2.findContours(img_cp,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    anum=len(cnts)
    bnum=anum
    cutnum=0
    center=np.zeros([anum,2],dtype=np.int32)
    pointcorner=np.zeros([anum,8],dtype=np.int32)
    for i in range(0,anum):
        # 将获取的图像由大到小排列取第i个
        cnt_second=sorted(cnts,key=cv2.contourArea,reverse=True)[i]
        # 使用最小的矩形框将所得轮廓包围，返回四个角点坐标
        box =cv2.minAreaRect(cnt_second)

        points=np.int0(cv2.boxPoints(box))
        #mask=np.zeros(image.shape,np.uint8)
        #mask=cv2.drawContours(mask,[points],-1,255,2)
        # 将获取的角点坐标转换回原图大小
        p1x,p1y=int(points[0,0]/w),int(points[0,1]/w)
        p2x,p2y=int(points[1,0]/w),int(points[1,1]/w)
        p3x,p3y=int(points[2,0]/w),int(points[2,1]/w)
        p4x,p4y=int(points[3,0]/w),int(points[3,1]/w)
        # 计算中心点坐标，若中心点距离图像边缘过近则跳过不取
        center_x,center_y=(p1x+p3x)/2,(p1y+p3y)/2
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
    cosp=np.zeros((anum,1))
    acosp=np.zeros_like(cosp)
    for i in range(0,anum):
        p=(centernew[i][0],centernew[i][1])
        p1=(pointcorner[i,0],pointcorner[i,1])
        p2=(pointcorner[i,2],pointcorner[i,3])
        p3=(pointcorner[i,4],pointcorner[i,5])
        p4=(pointcorner[i,6],pointcorner[i,7])
        # 计算两个边长，取长边进行偏转角计算
        l12=plength(p1,p2)
        l14=plength(p1,p4)
        if l12>l14 :
            cosp[i]=(p2[0]-p1[0])/l12
            flag=p2[1]-p1[1]
        else:
            cosp[i]=(p4[0]-p1[0])/l14
            flag=p4[1]-p1[1]
        acosp[i]=(math.acos(cosp[i])/math.pi)*180
        if flag<0:
            acosp[i]=-acosp[i]+180

    return center,acosp,anum


def trans_to_world(center,rvecs,mtx,dx=18,dy=37,worldx0=659,worldy0=527,Zc=1420):
    thingx, thingy=center[0], center[1]
    fx, fy=mtx[0][0], mtx[1][1]
    dxc=Zc/fx*abs(thingx-worldx0)
    dyc=Zc/fy*abs(thingy-worldy0)
    numrvecs=len(rvecs)
    transx, transy, transz=0, 0, 0
    for i in range(0,numrvecs-1):
        transx=transx+rvecs[i][0]
        transy=transy+rvecs[i][1]
        transz=transz+rvecs[i][2]
    transx=math.radians(transx/numrvecs)
    transy=math.radians(transy/numrvecs)
    transz=math.radians(transz/numrvecs)      
    Rx=np.array([[1,0,0],[0,math.cos(transx),math.sin(transx)],[0,-math.sin(transx),math.cos(transx)]])
    Ry=np.array([[math.cos(transy),0,math.sin(transy)],[0,1,0],[-math.sin(transy),0,math.cos(transy)]])
    Rz=np.array([[math.cos(transz),math.sin(transz),0],[-math.sin(transz),math.cos(transz),0],[0,0,1]])
    trans=np.dot(np.dot(Rx,Ry),Rz)
    dpoint=np.array([dxc,dyc,1])
    dpoint=dpoint.T
    dw=np.dot(trans,dpoint)
    dxw=dw[0]
    dyw=dw[1]
    if thingx-worldx0<=0:
        dxw=dxw
    else:
        dxw=-dxw
    if thingy-worldy0<=0:
        dyw=dyw
    else:
        dyw=-dyw
    #dxw=math.floor(dxw)-dx
    #dyw=math.floor(dyw)-dy
    return dxw,dyw


def tawer_based(angle,i,block_w=25,pass_center=np.array([200,200]),r=4*math.sqrt(2),tran_to_angle_1=0,tran_to_angle_2=90):
    level=i//3
    lnum=i%3
    if level%2==0:
        isou=True
    else:
        isou=False
        
    if isou:
        trans_angle=tran_to_angle_1-angle
        if angle > 90:
            trans_angle=180-angle
    else:
        trans_angle=tran_to_angle_2-angle
        if angle > 90:
            trans_angle=-trans_angle


    #angle_dx=r*math.sin(trans_angle)
    #angle_dy=r*(1-math.cos(trans_angle))

    if isou==True and lnum==0:
        object_point=(pass_center[0],pass_center[1]-block_w)
    else:
        if isou==True and lnum==1:
            object_point=(pass_center[0],pass_center[1])
        else:
            if isou==True and lnum==2:
                object_point=(pass_center[0],pass_center[1]+block_w)
            else:
                if isou==False and lnum==0:
                    object_point=(pass_center[0]-block_w,pass_center[1])
                else:
                    if isou==False and lnum==1:
                        object_point=(pass_center[0],pass_center[1])
                    else:
                        if isou==False and lnum==2:
                            object_point=(pass_center[0]+block_w,pass_center[1])
        
    fix_x=r*math.sin(trans_angle*math.pi/180)
    fix_y=r*(1-math.cos(trans_angle*math.pi/180))

    object_point=(object_point[0]+fix_x,object_point[1]+fix_y)

    return object_point,trans_angle,level