
#ライブラリのインポート
import sys
import cv2
from matplotlib.pyplot import sca
import numpy as np
import glob
import random
import cv2


# 画像ファイルの読み込み
img = cv2.imread('data/colorado.png')


# 画像ファイルが読み込めなかったとき
if img is None:
    sys.exit('Can not read image')

h,w=img.shape[:2]

for i in range(1000):
    w1=random.randint(0,2)
    h1=w1*random.randint(0,8)
    hn=random.randint(0,h-h1)
    wn=random.randint(0,w-w1)
    x=30
    for j in range(h1):
        for k in range(w1):
            if (j>0 and j<h1-1)or(k>0 and k<w1-1):
                for l in range(3):
                    if img[hn+j][wn+k][l]<(255-x):
                        img[hn+j][wn+k][l]+=x
                    else:
                        img[hn+j][wn+k][l]=255
                


# 表示ウィンドウに画像を表示
cv2.imshow('win_img', img)

# キー入力待機
cv2.waitKey(0)

# 表示ウィンドウを削除
cv2.destroyWindow('win_img')

