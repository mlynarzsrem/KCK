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

def plot_color_gradients(gradients, names):
    # For pretty latex fonts (commented out, because it does not work on some machines)
    #rc('text', usetex=True)
    #rc('font', family='serif', serif=['Times'], size=10)
    rc('legend', fontsize=10)

    column_width_pt = 400         # Show in latex using \the\linewidth
    pt_per_inch = 72
    size = column_width_pt / pt_per_inch

    fig, axes = plt.subplots(nrows=len(gradients), sharex=True, figsize=(size, 0.75 * size))
    fig.subplots_adjust(top=1.00, bottom=0.05, left=0.25, right=0.95)


    for ax, gradient, name in zip(axes, gradients, names):
        # Create image with two lines and draw gradient on it
        img = np.zeros((2, 1024, 3))
        for i, v in enumerate(np.linspace(0, 1, 1024)):
            img[:, i] = gradient(v)

        im = ax.imshow(img, aspect='auto')
        im.set_extent([0, 1, 0, 1])
        ax.yaxis.set_visible(False)

        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.25
        y_text = pos[1] + pos[3]/2.
        fig.text(x_text, y_text, name, va='center', ha='left', fontsize=10)

    fig.savefig('my-gradients.pdf')

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

def gradient_rgb_bw(v):
    return (v,v,v)


def gradient_rgb_gbr(v):
    if(v<0.5): #(0,1,0) ->(0,0,1)
        return (0, 1-2*v, 0+2*v)
    else: #(0,0,1) ->(1,0,0)
        v-=0.5
        return (0+v*2,0, 1-2*v)


def gradient_rgb_gbr_full(v):

    if(0<v<=0.25): #(0,1,0) ->(0,1,1)
        return (0,1,0+4*v)
    if(0.25<v<=0.5): #(0,1,1) ->(0,0,1)
        v-=0.25
        return (0,1-4*v,1)
    if(0.5 < v <= 0.75): #(0,0,1) ->(1,0,1)
        v-=0.5
        return (0+4*v,0,1)
    if (0.75 < v <= 1): #(1,0,1) ->(1,0,0)
        v -= 0.75
        return (1,0,1-4*v)


def gradient_rgb_wb_custom(v):
    if(0<v<=0.14): #(1,1,1) ->(1,0,1)
        return (1,1-v*7.1,1)
    if(0.14<v<=0.28): #(1,0,1) ->(0,0,1)
        v-=0.14
        return (1-v*7.1,0,1)
    if(0.28 < v <= 0.42): #(0,0,1) ->(0,1,1)
        v-=0.28
        return (0,0+v*7.1,1)
    if (0.42 < v <= 0.56): #(0,1,1) ->(0,1,0)
        v -= 0.42
        return (0,1,1-7.1*v)
    if(0.56<v<=0.70): #(0,1,0) ->(1,1,0)
        v-=0.56
        return (0+7.1*v,1,0)
    if(0.70 < v <= 0.84): #(1,1,0) ->(1,0,0)
        v-=0.70
        return (1,1-7.1*v,0)
    if (0.84 < v <= 1): #(1,0,0) ->(0,0,0)
        v -= 0.84
        return (1-v*6.25,0,0)


def gradient_hsv_bw(v):
    return hsv2rgb(0, 0, v)


def gradient_hsv_gbr(v):
    if(v<0.5): #(120,1,1) ->(240,1,1)
        return hsv2rgb(120 +240*v, 1, 1)
    else:
        v-=0.5
        return hsv2rgb(240+240*v, 1, 1)

def gradient_hsv_unknown(v):
    return hsv2rgb(120-120*v, 0.5, 1)


def gradient_hsv_custom(v):
    return hsv2rgb(0+320*v, 1-v, 1)

if __name__ == '__main__':
    def toname(g):
        return g.__name__.replace('gradient_', '').replace('_', '-').upper()

    gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
                 gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom)

    plot_color_gradients(gradients, [toname(g) for g in gradients])