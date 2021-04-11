import cv2
import numpy as np
import sys
import math
import glob

def calibration(imgpath,wnum=11,hnum=8,imgtype='jpg'):
    # termination criteria1
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((wnum*hnum,3), np.float32)
    objp[:,:2] = np.mgrid[0:wnum,0:hnum].T.reshape(-1,2)
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    images = glob.glob(imgpath + '/*'+imgtype)
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (wnum,hnum),None,cv2.CALIB_CB_ADAPTIVE_THRESH)
        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)
            cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            imgpoints.append(corners)
    
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
    return ret, mtx, dist, rvecs, tvecs


def fix_image(image, mtx, dist,name='camera.jpg'):
    # image 需要进行去畸变的图像
    # mtx 标定所得的相机内参矩阵
    # dist 标定所得的畸变系数向量
    h,w = image.shape[:2]
    #h,w=960,1280
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),0,(w,h)) 
    dst = cv2.undistort(image, mtx, dist, None, newcameramtx)

    x,y,w,h = roi
    dst= dst[y:y+h, x:x+w]
    cv2.imwrite(name,dst)
    return dst
