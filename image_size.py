import cv2

# 画像の読み込み
image = cv2.imread("C:/Users/okaji/Desktop/pro/tool/input/input.jpg")  # 'input.jpg' は対象の画像ファイル名に置き換えてください

# 新しいサイズを指定（幅, 高さ）
new_width = 120
new_height = 160

# 画像のリサイズ
resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

# リサイズ後の画像を保存
cv2.imwrite('C:/Users/okaji/Desktop/pro/tool/output/resized_image.jpg', resized_image)
