import cv2
import numpy as np
import sys
num=12366
infile1='C:/Users/okaji/Desktop/data/drive.avi'
infile2='C:/Users/okaji/Desktop/完成動画/9/'+str(num)+'.avi'
video1=cv2.VideoCapture(infile1)
if not video1.isOpened():
    sys.exit('can not read image.')

video2=cv2.VideoCapture(infile2)
if not video2.isOpened():
    sys.exit('can not read image.')
count=0
for _ in range(600):
    #つぎふれーむのよみとり
    ret1,img1=video1.read()
    if not ret1:
        sys.exit()

    ret2,img2=video2.read()
    if not ret2:
        sys.exit()

    if cv2.waitKey(1)==27:
        sys.exit()
    noise=np.zeros(img1.shape,dtype=np.uint8)
    noise=np.where(img1!=img2,img2,0)
    count_img=np.where(img1[:,:,0]!=img2[:,:,0],abs(img1[:,:,0]-img2[:,:,0]),0)
    count_img=np.where(img1[:,:,1]!=img2[:,:,1],abs(img1[:,:,1]-img2[:,:,1]),count_img)
    count_img=np.where(img1[:,:,2]!=img2[:,:,2],abs(img1[:,:,2]-img2[:,:,2]),count_img)
    count+=np.count_nonzero(count_img)/100

    cv2.imshow('image',noise)
print(count/6)