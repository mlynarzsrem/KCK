from pylab import *
import skimage
from skimage import data, io, filters, exposure, feature, morphology
from skimage.morphology import square
from skimage.filters import rank
from skimage.util.dtype import convert
from skimage import img_as_float, img_as_ubyte
from skimage.color import rgb2hsv, hsv2rgb, rgb2gray
from skimage.filters.edges import convolve
from matplotlib import pylab as plt
import numpy as np
from numpy import array

def get_index(list,value):
    for i in range(len(list)):
        if(list[i]==value):
            return i
    return -1
def find_most_common(img,fr=0,to=255):
    img = img_as_ubyte(img)
    histo, x = np.histogram(img, range(0, 256), density=True)
    maxvl=max(histo[fr:to])
    index = get_index(histo, maxvl)
    col = 1 * ((index +30) / 255)
    return col

def plot_hist(img):
    img = img_as_ubyte(img)
    histo, x = np.histogram(img, range(0, 256), density=True)
    plot(histo)
    xlim(0, 255)
    plt.show()

def show_image(img):
    io.imshow(img)
    plt.show()

def sobel_filter(img):
    return abs(filters.sobel(img))**0.5

def median_filter(img):
    med=filters.rank.median(img,ones([3, 3], dtype=uint8))
    return med

def mean_filter(img):
    res=filters.rank.mean(img,ones([3,3], dtype=uint8))
    return res

def gaussian_filter(img):
    gauss=filters.gaussian(img,sigma=3)
    return gauss

def erosion_filter(img,n):
    for i in range(n):
        image=morphology.erosion(img, square(5))
    return image

def dilatation_filter(img,n):
    for i in range(n):
        image=morphology.dilation(img, square(5))
    return image

def convolve_filter(img):
    K = array([[1,1,1],
               [1,1,1],
               [1,1,1]])
    K = K / sum(K)
    return convolve(img, K)


def normalize(img,perc=0.0):
    img=img_as_float(img)
    MIN = np.percentile(img, perc)
    MAX = np.percentile(img, 100 - perc)
    norm = (img - MIN) / (MAX - MIN)
    norm[norm[:, :] > 1] = 1
    norm[norm[:, :] < 0] = 0
    return norm

def gamma_filter(img,gamma=0.0):
    tmp=img**gamma
    return tmp

def run_filters(img):
    img = median_filter(img)
    img = (1 - img)
    mc=find_most_common(img,fr=30,to=225)
    img[img<mc]=0
    img = erosion_filter(img, 5)
    img=dilatation_filter(img,5)
    img = mean_filter(img)
    img = sobel_filter(img)
    return img

fname="img/samolot01.jpg"
image=io.imread(fname)
org_img=image
img=rgb2gray(image) #1 to biały 0 to czarny
img=run_filters(img)
minz=img[img!=0].min()
for i in range(len(img)):
    for j in range(len(img[i])):
        if(img[i][j]>0.06):
            org_img[i][j]=[255,0,0]
show_image(org_img)