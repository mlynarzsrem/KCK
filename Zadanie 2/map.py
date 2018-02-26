#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division             # Division in Python 2.7
import matplotlib
matplotlib.use('Agg')                       # So that we can render files without GUI
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
from math import floor
from matplotlib import colors

def angle(svl,pvl):
    cos=pvl/svl
    return cos
def vector_length(vec):
    sumv=0
    for i in range(len(vec)):
        sumv+=vec[i]**2
    return sumv

def sun_vector(x,y,h):
    return [750-x,750-y,10000-h]

def perp_vector(x,y,h):
    return [x-750,y-750,0]

def advanced_shader(x,y,h):
    svl=vector_length(sun_vector(x,y,h))
    pvl=vector_length(perp_vector(x,y,h))
    cos=angle(svl,pvl)
    v=1-20*cos
    if(v<0):
        v=0
    return v
def min_or_max(what,data):
    ex_list = []
    width = int(data[0][0])
    height= int(data[0][1])
    if(what=="max"):
        for i in range(1, height):
            ex_list.append(max(data[i]))
        return max(ex_list)
    else:
        for i in range(1, height):
            ex_list.append(min(data[i]))
        return min(ex_list)

def simple_shader(min_val,max_val,left,right):
    max_dif = max_val - min_val
    act_dif=abs(left-right)
    prop=act_dif/max_dif
    if(right>left):
        v=0.8+0.2*prop
    else:
        v=1-0.2*prop
    return v


def create_image(data):
    width = int(data[0][0])
    height= int(data[0][1])
    max_val=min_or_max("max",data)
    min_val = min_or_max("min", data)
    max_dif=max_val-min_val
    img = np.zeros((width, height, 3))
    for i in range(1, height):
        for j in range(width):
            v=1
            dif=140*(data[i][j]/max_val)
            v=advanced_shader(i,j,data[i][j])
            #if(j!=0):
               #v=simple_shader(min_val,max_val,data[i][j-1],data[i][j])
            img[i][j] = hsv2rgb(140-dif, 1, v)
    return img

def map_create(data):
    plt.figure(figsize=(7,7))
    plt.imshow(create_image(data), aspect='auto')
    plt.savefig('map.pdf')

def hsv2rgb(h, s, v):
    if(v==0):
        return (0,0,0)
    else:
        h/=60
        i=floor(h)
        f=h-i
        p = v * (1 - s)
        q = v * (1 - (s * f))
        t = v * (1 - (s * (1 - f)))
        if (i==0):
            return (v, t, p)
        if (i==1):
            return (q, v, p)
        if (i==2):
            return (p, v, t)
        if (i==3):
            return (p, q, v)
        if (i==4):
            return (t, p, v)
        if (i==5):
            return (v, p, q)

def castListToFloat(strList):  # Przerabia listę Stringów na listę floatów
    floatList = []
    for i in range(len(strList)):
        floatList.append(float(strList[i]))
    return floatList

def generateData(filename):  # Odczytuje dane z pojedynczego pliku
    tab = []
    with open(filename) as f:
        for line in f:
            tab.append(castListToFloat(line.split()))
    return tab

map_create(generateData("big.dem"))
