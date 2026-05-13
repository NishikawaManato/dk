import sys
import cv2
import time
b=input("b:")
outfile='C:/Users/okaji/Desktop/video/new4/'+b+'.mp4'
#書き込みファイル指定
rec=cv2.VideoWriter(outfile,cv2.VideoWriter_fourcc(*'mp4v'),30,(1920,1080))
for _ in range(6):
    a=input("a:")
    infile='C:/Users/okaji/Desktop/video/new4/'+a+'.avi'
    text=input("Text:")
    fps=60
    #読み込みファイル指定
    video=cv2.VideoCapture(infile)
    if not video.isOpened():
        sys.exit('can not read image.')

    h,w=(int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)),int(video.get(cv2.CAP_PROP_FRAME_WIDTH)))

    frame_count=int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    

    for _ in range(60):
        #次のフレームを作成
        ret,img=video.read()
        ret,img=video.read()
        cv2.putText(img,text,(50,400),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),4)
        #画像を表示
        cv2.imshow('img',img)
    #画像を保存
        rec.write(img)
        if not ret:
            break
        if cv2.waitKey(20)==27:
            break
rec.release()
video.release()
