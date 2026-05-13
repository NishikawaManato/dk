import cv2
import sys
import numpy as np

img = cv2.imread('D:/data/LBP.jpg')
if img is None:
    sys.exit()
mu=10
sigma=400
noise=np.random.randint(0,4,img.shape)
noise[:,:,1]=noise[:,:,0]
noise[:,:,2]=noise[:,:,0]
img1=np.where(noise==0,255,img)
img1=np.where(noise==1,0,img1)
retval = cv2.imwrite('D:/data/SoltPepperNoise.jpg',img1)