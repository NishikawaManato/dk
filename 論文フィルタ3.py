import cv2

def blur_area(image_path, output_path, x, y, w, h, blur_strength=221):
    # 画像の読み込み
    img = cv2.imread(image_path)
    
    if img is None:
        print("画像が見つかりません")
        return

    # ぼかしをかけたい範囲（ROI）を抽出
    roi = img[y:y+h, x:x+w]

    # ガウスぼかしを適用 (ksizeは奇数である必要があります)
    # blur_strengthを大きくするほど、ぼかしが強くなります
    ksize = blur_strength if blur_strength % 2 != 0 else blur_strength + 1
    blurred_roi = cv2.GaussianBlur(roi, (ksize, ksize), 0)

    # 元の画像にぼかした部分を書き戻す
    img[y:y+h, x:x+w] = blurred_roi

    # 結果を保存
    cv2.imwrite(output_path, img)
    print(f"保存完了: {output_path}")

blur_area('member.jpg', 'output_blur.jpg', 300, 150, 100, 100,10)
# 設定: (画像パス, 出力パス, X座標, Y座標, 幅, 高さ)
# 数値はピクセル単位で指定してください
for i in range(1,10):
    blur_area('output_blur.jpg', 'output_blur.jpg', 1500+150*i, 1500+130*i, 100, 100,200)