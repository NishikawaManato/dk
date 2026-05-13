import numpy as np
import cv2
import os

def compute_image_features(image_path):
    # 1. 画像の読み込みと正規化
    # グレースケールで読み込み、画素値を0.0〜1.0に正規化します [cite: 87]
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("画像を読み込めませんでした。")
    I = image.astype(np.float64) / 255.0

    # ガウシアンフィルタのパラメータ設定
    # K=L=3による7x7のカーネルで、3標準偏差までサンプリングするという論文の記述に基づきます [cite: 91, 92]
    kernel_size = (7, 7)
    sigma = 1.0 

    # 2. 局所平均フィールドと局所平均減算フィールド (Local Mean Subtracted Field)
    # ガウシアンフィルタで局所平均(μ)を計算し、元の画像から引きます [cite: 88, 89, 100, 101]
    mu = cv2.GaussianBlur(I, kernel_size, sigma)
    I_minus_mu = I - mu

    # 3. 局所コントラストフィールド (Local Contrast Field)
    # (I - μ)^2 にガウシアンフィルタをかけ、その平方根をとることで局所的な分散（標準偏差）を計算します [cite: 102, 103, 104]
    sigma_field = np.sqrt(cv2.GaussianBlur(I_minus_mu**2, kernel_size, sigma))

    # 4. 勾配フィールド (Gradient field)
    # 最も特徴を抽出できると記載されているラプラシアン演算子（二次微分）を適用します [cite: 105, 107, 108]
    laplacian = cv2.Laplacian(I, cv2.CV_64F)

    # 5. MSCN係数 (Mean Subtracted Contrast Normalized Coefficients)
    # 局所平均減算フィールドを局所コントラストフィールドで割って正規化します [cite: 109, 111]
    # eはゼロ除算を防ぐための小さな定数です [cite: 113]
    e = 1e-8 
    mscn = I_minus_mu / (sigma_field + e)

    # 6. MSCN係数のペアワイズ積 (水平方向)
    # 隣接する係数同士の積を計算します [cite: 116, 117, 118]
    # 画像サイズを維持するため、右端は0埋めまたはスライスで対応します
    mscn_H = np.zeros_like(mscn)
    mscn_H[:, :-1] = mscn[:, :-1] * mscn[:, 1:]

    # 抽出された5つの特徴量（フィールド）を辞書形式で返します
    return {
        "local_mean_subtracted": I_minus_mu,
        "local_contrast": sigma_field,
        "gradient_laplacian": laplacian,
        "mscn_coefficients": mscn,
        "mscn_horizontal_product": mscn_H
    }



def show_filter_results_cv2(image_path):
    # 先ほどの関数で5つの特徴量を計算
    features = compute_image_features(image_path)
    
    # 元画像の読み込み
    original_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if original_img is None:
        raise ValueError("画像を読み込めませんでした。")
    
    # cv2.imshow用に0.0〜1.0の範囲に正規化する補助関数
    def normalize_for_display(img_array):
        min_val = np.min(img_array)
        max_val = np.max(img_array)
        if max_val - min_val == 0:
            return np.zeros_like(img_array, dtype=np.float32)
        normalized = (img_array - min_val) / (max_val - min_val)
        return normalized.astype(np.float32)

    # 各画像を正規化
    # 元画像も0.0-1.0のfloat型に合わせます
    img_a = original_img.astype(np.float32) / 255.0
    img_b = normalize_for_display(features["local_mean_subtracted"])
    img_c = normalize_for_display(features["local_contrast"])
    img_d = normalize_for_display(features["gradient_laplacian"])
    img_e = normalize_for_display(features["mscn_coefficients"])
    img_f = normalize_for_display(features["mscn_horizontal_product"])

    # 論文の図に合わせてテキストを描画する補助関数
    def add_label(img, text):
        # 画像に黒いテキストと白い縁取りを描画して見やすくします
        labeled_img = img.copy()
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (10, 30)
        fontScale = 1.0
        thickness = 2
        # 白い縁取り
        cv2.putText(labeled_img, text, org, font, fontScale, (1.0, 1.0, 1.0), thickness + 2, cv2.LINE_AA)
        # 黒い文字
        cv2.putText(labeled_img, text, org, font, fontScale, (0.0, 0.0, 0.0), thickness, cv2.LINE_AA)
        return labeled_img
    def prepare_mean_subtracted_for_saving(field_array):
        # 1. データのばらつき（標準偏差）を計算
        std = np.std(field_array)
        
        # 2. 標準偏差の3倍を上限・下限として設定（データの大部分をカバーしつつ外れ値をカット）
        limit = 3.0 * std
        if limit == 0:
            return np.full_like(field_array, 128, dtype=np.uint8)
            
        # 3. limit の範囲内にデータを収める（クリッピング）
        clipped = np.clip(field_array, -limit, limit)
        
        # 4. -limit〜+limit の範囲を -127〜+127 にスケーリング
        scaled = (clipped / limit) * 127.0
        
        # 5. 128を足すことで、0.0 だった部分を中間のグレー(128)にする
        result = scaled + 128.0
        
        return result.astype(np.uint8)
    # ラベルの追加
    img_a = add_label(img_a, "a) Original")
    img_b = prepare_mean_subtracted_for_saving(features["local_mean_subtracted"])
    img_c = add_label(img_c, "c) Local Contrast")
    img_d = add_label(img_d, "d) Gradient")
    img_e = add_label(img_e, "e) MSCN")
    img_f = add_label(img_f, "f) MSCN Product")

    # 画像を水平（横）に連結して行を作成
    row1 = cv2.hconcat([img_a, img_b, img_c])
    row2 = cv2.hconcat([img_d, img_e, img_f])

    # 2つの行を垂直（縦）に連結
    combined_image = cv2.vconcat([row1, row2])

    # 画像が大きすぎる場合は画面に収まるようにリサイズ（必要に応じて調整してください）
    display_size = (1200, 800)
    combined_image = cv2.resize(combined_image, display_size)

    # ウィンドウに表示
    cv2.imshow("Filter Results", combined_image)
    cv2.imwrite('report_out.jpg', combined_image)
    # キーボードの何らかのキーが押されるまで待機
    print("ウィンドウを選択し、何かキーを押すと閉じます。")
    cv2.waitKey(0)
    cv2.destroyAllWindows()



def save_filter_results(image_path, output_dir="output_images"):
    # 保存先のフォルダを作成（存在しない場合のみ）
    os.makedirs(output_dir, exist_ok=True)
    
    # 先ほどの関数で5つの特徴量を計算
    features = compute_image_features(image_path)
    
    # 元画像の読み込み
    original_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if original_img is None:
        raise ValueError("画像を読み込めませんでした。")

    # 画像として保存するために 0〜255 の8ビット整数(uint8)に変換する補助関数
    def prepare_for_saving(img_array):
        min_val = np.min(img_array)
        max_val = np.max(img_array)
        if max_val - min_val == 0:
            return np.zeros_like(img_array, dtype=np.uint8)
        
        # 0.0〜1.0に正規化
        normalized = (img_array - min_val) / (max_val - min_val)
        
        # 0〜255にスケールアップしてuint8型に変換
        return (normalized * 255.0).astype(np.uint8)
    # save_filter_results 関数の中の prepare_for_saving の下に以下を追加します

    def prepare_laplacian_for_saving(lap_array):
        # 1. エッジの強さを強調するため絶対値をとる
        abs_lap = np.abs(lap_array)
        
        # 2. 上位1%の極端な外れ値の境界線を計算する（99パーセンタイル）
        p99 = np.percentile(abs_lap, 99.0)
        if p99 == 0:
            return np.zeros_like(abs_lap, dtype=np.uint8)
            
        # 3. p99より大きい値をp99に丸める（外れ値のカット）
        clipped = np.clip(abs_lap, 0, p99)
        
        # 4. 0〜255にスケールアップ
        return (clipped / p99 * 255.0).astype(np.uint8)

    # ---------------------------------------------------------
    # そして、各特徴量を変換する部分で、dの勾配フィールド（ラプラシアン）
    # だけ、今作った専用の関数を使うように書き換えます

    # img_d = prepare_for_saving(features["gradient_laplacian"]) # 修正前
     # 修正後
    # 各特徴量を保存用の形式に変換
    img_b = prepare_for_saving(features["local_mean_subtracted"])
    img_c = prepare_for_saving(features["local_contrast"])
    img_d = prepare_laplacian_for_saving(features["gradient_laplacian"])
    img_e = prepare_for_saving(features["mscn_coefficients"])
    img_f = prepare_for_saving(features["mscn_horizontal_product"])

    # 各画像を保存 (os.path.joinを使って指定したフォルダ内に保存します)
    cv2.imwrite(os.path.join(output_dir, "a_original.jpg"), original_img)
    cv2.imwrite(os.path.join(output_dir, "b_mean_subtracted.jpg"), img_b)
    cv2.imwrite(os.path.join(output_dir, "c_local_contrast.jpg"), img_c)
    cv2.imwrite(os.path.join(output_dir, "d_gradient.jpg"), img_d)
    cv2.imwrite(os.path.join(output_dir, "e_mscn.jpg"), img_e)
    cv2.imwrite(os.path.join(output_dir, "f_mscn_product.jpg"), img_f)

    print(f"すべての画像を {output_dir} フォルダ内に保存しました。")

# 実行例（実際の画像パスを指定して呼び出します）
save_filter_results("img_3040.jpeg")