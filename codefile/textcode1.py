# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 14:09:38 2019

@author: Admin
"""
import numpy as np
import math
transx1=0
transy1=180
transz1=0
transx1=math.radians(transx1)
transy1=math.radians(transy1)
transz1=math.radians(transz1)
a=transx1
b=transy1
c=transz1
Rx1=np.array([[1,0,0],
              [0,math.cos(transx1),math.sin(transx1)],
              [0,-math.sin(transx1),math.cos(transx1)]])
Ry1=np.array([[math.cos(transy1),0,math.sin(transy1)],
               [0,1,0],
               [-math.sin(transy1),0,math.cos(transy1)]])
Rz1=np.array([[math.cos(transz1),math.sin(transz1),0],
               [-math.sin(transz1),math.cos(transz1),0],
               [0,0,1]])
trans1=np.dot(np.dot(Rx1,Ry1),Rz1)
trans2=np.array([[math.cos(b)*math.cos(c),math.cos(b)*math.sin(c),math.sin(b)],
[-math.cos(a)*math.sin(c)-math.cos(c)*math.sin(a)*math.sin(b),math.cos(a)*math.cos(c)-math.sin(a)*math.sin(b)*math.sin(c),math.cos(b)*math.sin(a)],
[math.sin(a)*math.sin(c)-math.cos(a)*math.cos(c)*math.sin(b),-math.cos(c)*math.sin(a)-math.cos(a)*math.sin(b)*math.sin(c),math.cos(a)*math.cos(b)]])
