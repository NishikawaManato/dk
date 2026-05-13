import sys
import cv2

infile='./out/sinslide_noise.mp4'
outfile='./out/fpss.mp4'
fps=10
#読み込みファイル指定
video=cv2.VideoCapture(infile)
if not video.isOpened():
    sys.exit('can not read image.')

h,w=(int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)),int(video.get(cv2.CAP_PROP_FRAME_WIDTH)))

frame_count=int(video.get(cv2.CAP_PROP_FRAME_COUNT))

#書き込みファイル指定
rec=cv2.VideoWriter(outfile,cv2.VideoWriter_fourcc(*'mp4v'),fps,(w,h))
for _ in range(frame_count):
    #次のフレームを作成
    ret,img=video.read()
#画像を保存
    rec.write(img)
    if not ret:
        break
    if cv2.waitKey(20)==27:
        break
