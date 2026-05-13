import cv2
import sys

img=cv2.imread("C:/Users/okaji/Desktop/pro/tool/input/input.png")

if img is None:
    sys.exit('Can not read image.')

# グレースケールに変換
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# グレースケール画像を保�?
cv2.imwrite('C:/Users/okaji/Desktop/pro/tool/output/output.png', gray_image)

# 表示?��任意�?
cv2.imshow('Gray Image', gray_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
