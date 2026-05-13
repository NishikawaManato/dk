import sys
import cv2
import numpy as np
from scipy.stats import norm
import random
import math
import time
from scipy import *
#import cupy as np
# 警告メッセージを非表示
import warnings
warnings.filterwarnings("ignore")

# ノイズ点の数と速度
cut_wide=5
count = 1080*50
point_speed_min = 0
point_speed_max = 0
clear_level=50
SideSlide=0
noiseshape=np.array([[1,1,1],
                     [1,1,1],
                     [1,1,1]])
squear=True
move='gaussrain'
concat=True
rain=False
slide_mean=0
slide_sigma=0
theta=0
infile='C:/Users/okaji/Desktop/data/drive2.avi'
n=20
p=0.5
a=0
angle=0

#動画入出力の関数
def fileInOpen(infile):
    #読み込みファイル指定
    video=cv2.VideoCapture(infile)
    if not video.isOpened():
        sys.exit('can not read image.')
    else :
        return video

def fileOutOpen(move,timely,count,minspeed,maxspeed,mean,sigma,clear,concat,rain):
    filename=move+str(count)
    if move=='slide_normal':
        filename+='('+str(minspeed)+','+str(maxspeed)+')'
    elif move=='slide_gauss':
        filename+='('+str(mean)+','+str(sigma)+')'
    elif move=='brown':
        filename+='('+str(minspeed)+','+str(maxspeed)+')'
    elif move=='gaussrain':
        filename+='('+str(n)+','+str(p)+','+str(a)+')'
    elif move=='random':
        filename+='(random)'
    elif move=='gaussbrown':
        filename+='('+str(mean)+','+str(sigma)+')'
    else:
        sys.exit('fileOutOpen:"move" is wrong.')
    
    filename+=str(clear)
    if rain :
        filename+='雨'
    else :
        filename+='ノイズ'
    if concat :
        filename+='動画'
    
    return str(filename+timely)

def videoGet(video):
    h,w=(int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)),int(video.get(cv2.CAP_PROP_FRAME_WIDTH)))
    fps=int(video.get(cv2.CAP_PROP_FPS))
    frame_count=int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    return h,w,fps,frame_count

#ノイズの詳細の関数
def maskshift(v1,v2,backmask):
    h,w=backmask.shape[:2]
    #下を排除
    backmask1=backmask[:h-v1,:,:3]
    #上に追加する配列を作成
    mask1=np.zeros((v1,w,3),dtype=np.uint8)
    
    #上の配列を結合
    mask=np.concatenate([mask1,backmask1],0)

    #右を排除
    backmask2=mask[:,:w-v2,:3]

    #左に追加する配列の作成
    mask2=np.zeros((h,v2,3),dtype=np.uint8)

    #左の配列を結合
    mask=np.concatenate([mask2,backmask2],1)

    return mask

def noisesize(backmask,noiseshape):
    if squear==True :
        return noisesize2(backmask,noiseshape)
    else:
        return noisesize1(backmask,noiseshape)

def noisesize1(backmask,noiseshape):                                 #処理が遅すぎる！！！！！
    # ① noiseshape → 構造要素に変換
    kernel = (noiseshape > 0).astype(np.uint8)

    # ② 1フレームのノイズマスク mask (H,W,3) を用意
    gray = (mask[...,0] > 0).astype(np.uint8)          # 1ch に落とす

    # ③ 膨張（dilate）でサイズ拡張
    gray_dil = cv2.dilate(gray, kernel, iterations=1)

    # ④ 3ch へ復元（broadcast）
    mask_size = gray_dil[...,None] * mask
    return mask_size

def noisesize2(backmask,noiseshape):
    mask_size=np.zeros(backmask.shape,dtype=np.uint8)
    for v1 in range(noiseshape.shape[0]):
        mask_size=np.where(mask_size==0,maskshift(v1,0,backmask),mask_size)
    mask_size2=mask_size
    for v2 in range(noiseshape.shape[1]):
        mask_size2=np.where(mask_size2==0,maskshift(0,v2,mask_size),mask_size2)
    return mask_size2
    
def maskRangeMaker(h,w,maskhw):
    maskRange=np.ones((h,w,3),dtype=np.uint8)
    maskRange*=255
    for i in range(maskhw.shape[0]):
        maskRange[maskhw[i,0]:maskhw[i,1],maskhw[i,2]:maskhw[i,3],:]=0
    return maskRange

#ノイズの初期値の関数
def pointsSet(move,h,w,count,minspeed,maxspeed,mean,sigma):
    if move=='slide_normal':
        points=slidePointsSet(h,w,count,minspeed,maxspeed)
    elif  move=='brown':
        points=RandomWalkPointsSet(h,w,count,minspeed,maxspeed)
    elif move=='slide_gauss':
        points=slideGaussPointsSet(h,w,count,mean,sigma)
    elif move=='spin':
        points=spinPointsSet(h,w,count)
    elif move=='gaussrain':
        points=GaussrainSet(h,w,count,mean,sigma)
    elif move=='random':
        points=randomSet(h,w,count)
    elif move=='gaussbrown':
        points=GaussrainSet(h,w,count,mean,sigma)
    else:
        sys.exit('pointsSet:"move" is wrong.')
    return points

def slidePointsSet(h,w,count,minspeed,maxspeed):
    # ノイズ点の初期位置をランダムに設定
    drops = np.zeros((7,count), dtype=int)  # Each drop has (x, y, speed)
    drops[0] = np.random.randint(0, h-1, count)  # Random x positions
    drops[1] = np.random.randint(0, w-1, count)  # Random y positions (starting above the frame)
    if maxspeed>0:
        drops[2] = np.random.randint(minspeed, maxspeed, count)  # Random speeds
    drops[3] = np.random.randint(0, 255, count)  # Random R positions
    drops[4] = np.random.randint(0, 255, count)  # Random G positions
    drops[5] = np.random.randint(0, 255, count)  # Random B positions
    return drops

def slideGaussPointsSet(h,w,count,mean,sigma):
    # ノイズ点の初期位置をランダムに設定
    
    drops = np.zeros((7,count), dtype=int)  # Each drop has (x, y, speed)
    save=np.zeros((1,count),dtype=int)
    if mean>0 :
        save = np.random.randint(0,mean*2,count*h)
    drops[0] = np.random.randint(0, h-1, count)  # Random x positions
    drops[1] = np.random.randint(0, w-1, count)  # Random y positions (starting above the frame)
    drops[2] = np.random.normal(mean, sigma, count)  # Random speeds
    drops[2] = np.where(drops[2]>mean+cut_wide,save,drops[2])
    drops[2] = np.where(drops[2]<mean-cut_wide,save,drops[2])
    drops[3] = np.random.randint(0, 255, count)  # Random R positions
    drops[4] = np.random.randint(0, 255, count)  # Random G positions
    drops[5] = np.random.randint(0, 255, count)  # Random B positions
    return drops

def spinPointsSet(h,w,count):
    # ノイズ点の初期位置をランダムに設定
    points = []

    for y in range(h-1):
        for _ in range(count):
            x = random.randint(0, w - 1)
            theta=math.asin((h/2-y)/math.sqrt((x-(w/2))*(x-w/2)+(y-(h/2))*(y-(h/2))))
            if (x-(w/2))/math.sqrt((x-(w/2))*(x-w/2)+(y-(h/2))*(y-(h/2)))<0:
                theta=math.pi-theta
            r = random.randint(0,255)
            g = random.randint(0,255)
            b = random.randint(0,255)
            points.append([y,x,theta,r,g,b])


    return np.array(points).T

def RandomWalkPointsSet(h,w,count,minV,maxV):
    # ノイズ点の初期位置をランダムに設定
    drops = np.zeros((7,count), dtype=int)  # Each drop has (x, y, speed)
    drops[0] = np.random.randint(0, h-1, count)  # Random x positions
    drops[1] = np.random.randint(0, w-1, count)  # Random y positions (starting above the frame)
    if maxV>0:
        drops[2] = np.random.randint(minV, maxV, count)  # Random speeds
    drops[3] = np.random.randint(0, 255, count)  # Random R positions
    drops[4] = np.random.randint(0, 255, count)  # Random G positions
    drops[5] = np.random.randint(0, 255, count)  # Random B positions
    return drops

def GaussrainSet(h,w,count,mean,sigma):
    # ノイズ点の初期位置をランダムに設定
    noisecount=count
    """
    if mean==0:
        noisecount=count
    elif sigma==0:
        noisecount=count
    else:
        noisecount=int(count/(1-(2*norm.cmf(mean-cut_wide-1,mean,sigma))))

    """
    drops = np.zeros((7,noisecount), dtype=int)  # Each drop has (x, y, speed)
    drops2 = np.zeros((7,0),dtype=int)
    drops[0] = np.random.randint(0, h-1, noisecount)  # Random x positions
    drops[1] = np.random.randint(0, w-1, noisecount)  # Random y positions (starting above the frame)
    drops[2] = np.random.binomial(n, p, noisecount)  # Random speeds
    drops[3] = np.random.randint(1, 255, noisecount)  # Random R positions
    drops[4] = np.random.randint(1, 255, noisecount)  # Random G positions
    drops[5] = np.random.randint(1, 255, noisecount)  # Random B positions
    drops[6] = drops[2]
    drops[2] = drops[2]+a*np.ones(noisecount,dtype=int)
    if mean==0:
        drops2=drops
    else :
        for i in range (drops.shape[1]):
            if drops[2,i]!=0:
                drops2=np.append(drops2,drops[0:7,i:i+1],axis=1)
    print(drops2.shape)
    return drops2
def randomSet(h,w,count):
    drops=np.zeros((7,count),dtype=int)
    drops[0] = np.random.randint(0, h-1, count)  # Random x positions
    drops[1] = np.random.randint(0, w-1, count)  # Random y positions (starting above the frame)
    drops[3] = np.random.randint(0, 255, count)  # Random R positions
    drops[4] = np.random.randint(0, 255, count)  # Random G positions
    drops[5] = np.random.randint(0, 255, count)  # Random B positions
    return drops

#ノイズの動きの関数
def pointMove(move,h,w,points):
    if move=='slide_normal':
        return slidePointsMove(h,w,points)
    elif move=='slide_gauss':
        return slidePointsMove(h,w,points)
    elif move=='brown':
        return RandomWalkPointsMove(h,w,points)
    elif move=='gaussrain':
        return gaussrainMove(h,w,points)
    elif move=='random':
        return randomMove(h,w,points)
    elif move=='gaussbrown':
        return RandomWalkPointsMove(h,w,points)
    else:
        sys.exit('pointMove:"move" is wrong.')

def slidePointsMove(h,w,point):
    #次のフレームを作成
    backmask=np.zeros((h,w,3),dtype=np.uint8)
    kari=np.zeros((1,point.shape[1]),dtype=float)
    kari[:]=point[2]
    point[0] =point[0]+kari*math.cos(math.radians(theta))
    point[1] =point[1]+kari*math.sin(math.radians(theta))
    # 画面の端に到達したら反対側にループ
    point[0]=np.where(point[0] < 0,point[0] + h-1,point[0])
    point[0]=np.where(point[0] >=h,point[0] - h,point[0])
    point[1]=np.where(point[1]< 0,point[1] + w-1,point[1])
    point[1]=np.where(point[1] >=w,point[1] -w,point[1])
    #backmask[point[1]][point[0]]=[point[3],point[4],point[5]]
    
    x=point[0].astype(int)
    y=point[1].astype(int)
    values=point[3:6].T
    backmask[x,y]=values

    
    return backmask

def RandomWalkPointsMove(h,w,point):
     # 各ノイズ点をランダムな方向に移動
    backmask=np.zeros((h,w,3),dtype=np.uint8)
    if point_speed_max>0:
        kari0=np.random.randint(0,3,points.shape[1])
        kari0=(kari0-1)*point[2]
        kari1=np.random.randint(0,3,points.shape[1])
        kari1=(kari1-1)*point[2]
        point[0] = point[0]+kari0
        point[1] = point[1]+kari1
        
    # 画面の端に到達したら反対側にループ
    point[0]=np.where(point[0] < 0,point[0] + h-1,point[0])
    point[0]=np.where(point[0] >=h,point[0] - h,point[0])
    point[1]=np.where(point[1]< 0,point[1] + w-1,point[1])
    point[1]=np.where(point[1] >=w,point[1] -w,point[1])

    x=point[0].astype(int)
    y=point[1].astype(int)
    values=point[3:6].T
    backmask[x,y]=values
    return backmask

#ガウス分布に則った雨を動かす関数(入力:高さ(int),幅(int),ノイズ特性(numpy),)
def gaussrainMove(h,w,point):            #問題児
    if theta==90:
        cos=0
        sin=1
    elif theta==180:
        cos=-1
        sin=0
    elif theta==270:
        cos=0
        sin=-1
    else:
        cos=1
        sin=0
    #次のフレームを作成
    backmask=np.zeros((h,w,3),dtype=np.uint8)
    kari=np.zeros((1,point.shape[1]),dtype=float)
    kari[:]=point[2]
    point[0] =point[0]+kari*cos
    point[1] =point[1]+kari*sin
    # 画面の端に到達したら反対側にループ
    point[0]=np.where(point[0] < 0,point[0] + h-1,point[0])
    point[0]=np.where(point[0] >=h,point[0] - h,point[0])
    point[1]=np.where(point[1]< 0,point[1] + w-1,point[1])
    point[1]=np.where(point[1] >=w,point[1] -w,point[1])
    #backmask[point[1]][point[0]]=[point[3],point[4],point[5]]
    
    x=point[0].astype(int)
    y=point[1].astype(int)
    values=point[3:6].T
    backmask[x,y]=values

    
    return backmask

def randomMove(h,w,point):
    backmask=np.zeros((h,w,3),dtype=np.uint8)
    point[0]=np.random.randint(0, h-1, point[0].shape[0])
    point[1]=np.random.randint(0, w-1, point[1].shape[0])
    x=point[0].astype(int)
    y=point[1].astype(int)
    values=point[3:6].T
    backmask[x,y]=values

    return backmask




#動画処理の関数(入力:動画ファイル(video))(出力:映像終了真偽値(真偽値),フレーム画像(numpy))
def videoRead(video):
    ret,img=video.read()
    if not ret:
        sys.exit()

    if cv2.waitKey(1)==27:
        sys.exit()
    return ret,img

#映像とノイズを合わせる(入力:結合flag(boolean),雨flag(boolean),ノイズフレーム(numpy),動画フレーム(numpy),雨用輝度上昇値(int))(出力:結合後動画フレーム(numpy))
def imageConcat(concat,rain,mask,img,clear_level):
    buffer=np.where(mask[:,:,0]==0,0,1)
    buffer=np.where(mask[:,:,1]==0,buffer,1)
    buffer=np.where(mask[:,:,2]==0,buffer,1)
    noise_pixel_count=np.count_nonzero(buffer)/100
    if concat is True:
        if rain is True:
            image=np.where(mask==0,0,img)
            image=np.where(image>255-clear_level,255-clear_level,image)
            image=np.where(image==0,img,image+clear_level)
        else:
            
            image=np.zeros(img.shape,dtype=np.uint8)
            image[:,:,0]=np.where(buffer==0,img[:,:,0],mask[:,:,0])
            image[:,:,1]=np.where(buffer==0,img[:,:,1],mask[:,:,1])
            image[:,:,2]=np.where(buffer==0,img[:,:,2],mask[:,:,2])
    else :
        image=mask
    return image, noise_pixel_count

#画像を回転させる
def rotation(img,angle):
    if angle==90:
        img1 = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    elif angle==180:
        img1 = cv2.rotate(img, cv2.ROTATE_180)
    elif angle==270:
        img1= cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    else:
        img1=img
    return img1

#ノイズ成分出力(入力:ファイル名(string))
def writeFile1(string):
    f=open(string,'a')
    f.write('count='+str(count)+'\n')
    f.write('point_speed_min='+str(point_speed_min)+'\n')
    f.write('point_speed_max='+str(point_speed_max)+'\n')
    f.write('n='+str(n)+'\n')
    f.write('p='+str(p)+'\n')
    f.write('a='+str(a)+'\n')
    f.write('SideSlide='+str(SideSlide)+'\n')
    f.write('clear_level='+str(clear_level)+'\n')
    f.write('squear='+str(squear)+'\n')
    f.write('move='+str(move)+'\n')
    f.write('concat='+str(concat)+'\n')
    f.write('rain='+str(rain)+'\n')
    f.write('slide_mean='+str(slide_mean)+'\n')
    f.write('alide_sigma='+str(slide_sigma)+'\n')
    f.write('mean='+str(np.mean(points[2]))+'\n')
    f.write('var='+str(np.var(points[2]))+'\n')
    f.write('noisecount='+str(points.shape[1]/h)+'\n')
    f.close()

def writeFile2(string):
    f=open(string,'a')
    f.write('noise_average='+str(noise_pixel_count/6))
    f.close()

for for1 in range (1,2):
    noise_pixel_count=0
    
    #出力ファイル作成
    timely=str(int(time.time())%63072000)
    outfile='C:/Users/okaji/Desktop/out/'+fileOutOpen(move,timely,count,point_speed_min,point_speed_max,slide_mean,slide_sigma,clear_level,concat,rain)+'.avi'

    #読み込みファイルをひらく
    video=fileInOpen(infile)

    #読み込みファイルの属性を取得
    h,w,fps,frame_count=videoGet(video)

    #書き込みファイル指定
    rec=cv2.VideoWriter(outfile,cv2.VideoWriter_fourcc(*'RGBA'),fps,(w,h))

    #マスク範囲の指定
    maskhw=np.array([[0,h,0,w]],dtype=int)
    #maskhw=np.array([[0,h/4,0,w],[h*3/4,h,0,w],[0,h,0,w/3],[0,h,w*2/3,w]],dtype=int)

    #マスク範囲外用配列の作成
    maskRange=maskRangeMaker(h,w,maskhw)

    #ノイズ情報配列の作成
    points=pointsSet(move,h,w,count,point_speed_min,point_speed_max,slide_mean,slide_sigma)


    string1='C:/Users/okaji/Desktop/out/record/'+timely+'.csv'
    string2='C:/Users/okaji/Desktop/out/record/'+timely+'#2.csv'
    string3='C:/Users/okaji/Desktop/out/record/'+timely+'#3.csv'  
    string4='C:/Users/okaji/Desktop/out/record/'+timely+'#4.csv'    
    np.savetxt(string1,points,fmt='%.2e',delimiter=',')
    writeFile1(string2)
    np.savetxt(string3,noiseshape,delimiter=',')
    #----------------------------------------------以下while文----------------------------------------------------  
    #while True:
    
    for _ in range(fps*10):
        
        #つぎふれーむのよみとり
        ret,img=videoRead(video)
        
        #回転する
        img=rotation(img,angle)
        #ノイズフィルタの作成
        mask=pointMove(move,h,w,points)
        
        #ノイズサイズ変更
        mask=noisesize(mask,noiseshape)
        
        image,noisePixelCount=imageConcat(concat,rain,mask,img,clear_level)
        noise_pixel_count+=noisePixelCount
        #画像を表示
        cv2.imshow('image',image)
        #画像を保存
        rec.write(image)
    print(time.time())

    writeFile2(string4)
    rec.release()
    video.release()

