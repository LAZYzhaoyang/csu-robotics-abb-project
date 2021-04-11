import cv2
import numpy as np
import TIS
import socket
import time
import sys
import math
import glob
import coordingnate_tool as cod
import image_tool as it
import camera_tool as cam

imagepath='/media/silverbullet/data_and_programing_file/abbshowcode/camera1'
w=0.5
cutsize=250
r=4*math.sqrt(2)
pass_center=np.array([200,0])

dx=12
dy=0
worldx0=640
worldy0=480
Zc=1420

block_w=25
block_l=75
block_h=15

ret1, mtx1, dist1, rvecs1, tvecs1 =cam.calibration(imagepath,11,8,'jpg')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.125.4', 4005) # current server, and the port number is 10000
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)
# Wait for a connection
print >> sys.stderr, 'waiting for a connection'
connection, client_address = sock.accept()
print >> sys.stderr, 'connection from', client_address
#isstart=input("if start this program?true or false")

Tis1 = TIS.TIS("41814186", 1280, 960,30, True)
#Tis2 = TIS.TIS("41814186", 1280, 960,30, True)
# Start the pipeline so the camera streams
Tis1.Start_pipeline()  
#Tis2.Start_pipeline() 
# Create an OpenCV output window for two cameras 
#cv2.namedWindow('Window1')  
#cv2.namedWindow('Window2') 
# Get the image. It is a numpy array 
while Tis1.Snap_image(1) is False:
    Tis1.Snap_image(1)
 # Snap an image with one second timeout
image = Tis1.Get_image()
# Display the result
#cv2.imshow('Window1', image)

image=cam.recover_image(image,mtx1,dist1,name='camera1.jpg')
morph=it.image_pre_deal(image,w,False,False)
center,acosp,anum=cod.get_center(morph,w,cutsize)

for i in range(0,anum):
    dxw,dyw=cod.trans_to_world(center[i,:],rvecs1,mtx1,dx,dy,worldx0,worldy0,Zc)
    angle=acosp[i]
    tran_to_angle_1=0
    tran_to_angle_2=90

    object_point,trans_angle,level=cod.tawer_based(angle,i,block_w,pass_center,r,tran_to_angle_1,tran_to_angle_2)
    trans_angle=float(trans_angle)
    print(trans_angle)
    put_x=object_point[0]
    put_y=object_point[1]
    put_z=level*block_h

    if abs(dxw)>=300 or abs(dyw)>=300:
        continue
    hight=0
    sendwords1=str(dxw)+','+str(dyw)+',0,'+str(hight)+',1,0/0D'
    sendwords2=str(dxw)+','+str(dyw)+',0,100,1,0/0D'
    sendwords3=str(put_x)+','+str(put_y)+','+str(trans_angle)+','+str(put_z)+',2,0/0D'
    retools='0,-250,0,200,0,0/0D'
    send=[]
    send.append(sendwords1)
    send.append(sendwords2)
    send.append(sendwords3)
    send.append(retools)
    print(send)
    for j in range(0,len(send)):
        data = connection.recv(16)
        if data == 'pass':
            print >> sys.stderr, 'sending data back to the client'
            connection.sendall(send[j])
            print('wait next command')
        else:
            print >> sys.stderr, 'no more data for', client_address
            connection.sendall(retools)
            break
    print('finish a block trans')

print('finish all block trans')
# Stop the pipeline and clean up
Tis1.Stop_pipeline()    
#cv2.destroyAllWindows()
connection.close()
#print >> 'Program ends'



"""
        
        drophight1 = 300
        drophight2=0
        thinghight=15
        #sendwords2 = str(dxw2) + ',' + str(dyw2) + ',' + str(0) + ',' + str(drophight2) + ',' + str(1) + ',' + str(0) + '/0D'
        pickuppoint = str(dxw1) + ',' + str(dyw1) + ',0,' + str(drophight1) + ',1,0/0D'
        putpointup='200,0,0,'+str(drophight1)+',1,0/0D'
        putdownpoint='200,0,0,'+str(drophight2)+',1,0/0D'
        putdown='200,0,0,'+str(drophight2)+',2,0/0D'
        retools='0,-250,0,200,0,0/0D'
        drophight2=drophight2+thinghight
        bnum=bnum-1
        actionnum=5
        sends.append(sendwords1)
        
        
        
        # Receive the data in small chunks and retransmit it
        data = connection.recv(16)
        print >> sys.stderr, 'received "%s"' % data
        if (data == 'pass' and actionnum!=0):
            print >> sys.stderr, 'sending data back to the client'
            connection.sendall(sendwords1)
            actionnum=actionnum-1
            #print >> 'wait next command'

        else:
            print >> sys.stderr, 'no more data for', client_address
            connection.sendall(retools)
            break
            
        data = connection.recv(16)
        print >> sys.stderr, 'received "%s"' % data
        if (data == 'pass' and actionnum!=0):
            print >> sys.stderr, 'sending data back to the client'
            connection.sendall(pickuppoint)
            actionnum=actionnum-1
            #print >> 'wait next command'
                
        else:
            print >> sys.stderr, 'no more data for', client_address
            connection.sendall(retools)
            break
            
        data = connection.recv(16)
        print >> sys.stderr, 'received "%s"' % data
        if (data == 'pass' and actionnum!=0):
            print >> sys.stderr, 'sending data back to the client'
            connection.sendall(putpointup)
            actionnum=actionnum-1
            #print >> 'wait next command'
        else:
            print >> sys.stderr, 'no more data for', client_address
            connection.sendall(retools)
            break
            
        data = connection.recv(16)
        print >> sys.stderr, 'received "%s"' % data
        if (data == 'pass' and actionnum!=0):
            print >> sys.stderr, 'sending data back to the client'
            connection.sendall(putdownpoint)
            actionnum=actionnum-1
            #print >> 'wait next command'
        else:
            print >> sys.stderr, 'no more data for', client_address
            connection.sendall(retools)
            print >> 'END'
            break
            
        data = connection.recv(16)
        print >> sys.stderr, 'received "%s"' % data
        if (data == 'pass' and actionnum!=0):
            print >> sys.stderr, 'sending data back to the client'
            connection.sendall(putdown)
            actionnum=actionnum-1
            #print >> 'wait next command'
        else:
            print >> sys.stderr, 'no more data for', client_address
            connection.sendall(retools)
            #print >> 'END'
            break
        
        data = connection.recv(16)
        print >> sys.stderr, 'received "%s"' % data
        if (data == 'pass'):
            print >> sys.stderr, 'sending data back to the client'
            connection.sendall(retools)
            ifopencamera2=0
            #print >> 'end'
        else:
            print >> sys.stderr, 'no more data for', client_address
            connection.sendall(retools)
            ifopencamera2=0
            #print >> 'END'
            break
           
    
    # Clean up the connection
    connection.close()
    """

    




