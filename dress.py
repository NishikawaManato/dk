import sys
import cv2
import numpy as np
import random
imagefile='data/fruits.png'
img=cv2.imread(imagefile)
if img is None:
    sys.exit('Can not read image')


img[:,:,0]=np.where(img[:,:,0]>100,0,img[:,:,0])
cv2.imshow('win_img',img)
cv2.waitKey(0)
cv2.destroyWindow('win_img')
