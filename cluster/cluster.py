import random

import sys

import os
from PIL import Image
from sklearn.cluster import KMeans

here = sys.path[0]

def random_color(k):
    colors = []
    for i in range(k):
        R = random.randint(0,256)
        G = random.randint(0,256)
        B = random.randint(0,256)
        color = (R,G,B)
        colors.append(color)
    return colors

def image_segmentation(data,k,width, height):
    estimator = KMeans(n_clusters=k)
    estimator.fit_predict(data)
    lable_pred = estimator.labels_

    newImg = Image.new("RGB",(width,height))

    colors = random_color(k)

    for i in range(width):
        for j in range(height):
            index = i*height+j
            newImg.putpixel((i,j),colors[lable_pred[index]])


    newImg.save(os.path.join(here,"pic","cluster_{}.jpg".format(k)))

if __name__ == '__main__':
    if not os.path.exists(os.path.join(here,"pic")):
        os.makedirs(os.path.join(here,"pic"))

    im = Image.open(os.path.join(here,'pic.jpg'))
    width, height = im.size
    data = []
    for i in range(width):
        for j in range(height):
            data.append(list(im.getpixel((i,j))))

    k = input("请输入k值：")
    image_segmentation(data,int(k),width, height)






