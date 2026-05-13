import sys
import cv2
a=input("a:")
infile='C:/Users/okaji/Desktop/data/'+a+'.MP4'
outfile='C:/Users/okaji/Desktop/data/'+a+'.avi'
fps=60
#読み込みファイル指定
video=cv2.VideoCapture(infile)
if not video.isOpened():
    sys.exit('can not read image.')

h,w=(int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)),int(video.get(cv2.CAP_PROP_FRAME_WIDTH)))

frame_count=int(video.get(cv2.CAP_PROP_FRAME_COUNT))

#書き込みファイル指定
rec=cv2.VideoWriter(outfile,0,fps,(w,h))




for _ in range(frame_count):
    #次のフレームを作成
    ret,img=video.read()

    #画像を表示
    cv2.imshow('img',img)

#画像を保存
    rec.write(img)
    if not ret:
        break
    if cv2.waitKey(20)==27:
        break

