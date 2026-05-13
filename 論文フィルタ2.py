import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

def compute_image_features(image_path):
    # 画像の読み込みと正規化
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"画像を読み込めませんでした: {image_path}")
    # 正規化（/ 255.0）を削除し、ローデータのまま計算します
    I = image.astype(np.float64)

    # ガウシアンフィルタの設定（7x7カーネル）
    kernel_size = (7, 7)
    sigma = 1.0 

    # 1. 局所平均フィールドと局所平均減算フィールド
    mu = cv2.GaussianBlur(I, kernel_size, sigma)
    I_minus_mu = I - mu

    # 2. 局所コントラストフィールド
    sigma_field = np.sqrt(cv2.GaussianBlur(I_minus_mu**2, kernel_size, sigma))

    # 3. 勾配フィールド (ラプラシアン)
    # 微小なノイズによる影響を抑えるため、事前に軽くぼかしを適用します
    blurred_I = cv2.GaussianBlur(I, (3, 3), 0.5)
    laplacian = cv2.Laplacian(blurred_I, cv2.CV_64F, ksize=3)

    # 4. MSCN係数
    e = 1e-8 # ゼロ除算防止
    mscn = I_minus_mu / (sigma_field + e)

    # 5. MSCN係数のペアワイズ積 (水平方向)
    mscn_H = np.zeros_like(mscn)
    mscn_H[:, :-1] = mscn[:, :-1] * mscn[:, 1:]

    return {
        "local_mean_subtracted": I_minus_mu,
        "local_contrast": sigma_field,
        "gradient_laplacian": laplacian,
        "mscn_coefficients": mscn,
        "mscn_horizontal_product": mscn_H
    }

def save_histogram(data_array, title, output_path):
    # ヒストグラムを描画して保存する補助関数
    plt.figure(figsize=(8, 6))
    
    # 2次元の画像配列を1次元配列に平坦化
    flat_data = data_array.flatten()
    
    # ヒストグラムの描画 (ビンの数を100に設定)
    plt.hist(flat_data, bins=100, color='gray', alpha=0.7)
    plt.title(title)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.grid(True, alpha=0.3)
    
    # 画像として保存して図を閉じる
    plt.savefig(output_path)
    plt.close()

def save_histograms(image_path, output_dir="output_histograms"):
    # 保存先のフォルダを作成
    os.makedirs(output_dir, exist_ok=True)
    
    # 特徴量の計算
    features = compute_image_features(image_path)
    
    # 元画像の読み込み（正規化なし）
    original_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if original_img is None:
        raise ValueError(f"画像を読み込めませんでした: {image_path}")

    # 各特徴量のヒストグラムを作成して保存
    save_histogram(original_img, "a) Original Image", os.path.join(output_dir, "a_original_hist.png"))
    save_histogram(features["local_mean_subtracted"], "b) Local Mean Subtracted", os.path.join(output_dir, "b_mean_subtracted_hist.png"))
    save_histogram(features["local_contrast"], "c) Local Contrast", os.path.join(output_dir, "c_local_contrast_hist.png"))
    save_histogram(features["gradient_laplacian"], "d) Gradient (Laplacian)", os.path.join(output_dir, "d_gradient_hist.png"))
    save_histogram(features["mscn_coefficients"], "e) MSCN Coefficients", os.path.join(output_dir, "e_mscn_hist.png"))
    save_histogram(features["mscn_horizontal_product"], "f) Product of MSCN", os.path.join(output_dir, "f_mscn_product_hist.png"))

    print(f"すべてのヒストグラム画像を {output_dir} フォルダ内に保存しました。")

# 実行部分（テストしたい画像のパスに書き換えてください）
if __name__ == "__main__":
    image_file = "report_f.png"
    output_dir="output_histograms_f"
    save_histograms(image_file, output_dir)
    print("コードの準備が完了しました。画像パスを指定して実行してください。")