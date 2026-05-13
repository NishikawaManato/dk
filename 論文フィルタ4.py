import numpy as np
import cv2

def extract_image_quality_features(image_path):
    """
    画像から品質劣化認識のための20個の特徴量を抽出する関数
    
    Args:
        image_path (str): 入力画像のパス
        
    Returns:
        list: 20個の特徴量を含むリスト。画像の読み込みに失敗した場合はNone。
    """
    # 画像をグレースケールで読み込み、輝度値を0.0から1.0の範囲に正規化 [cite: 87]
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("画像の読み込みに失敗しました。")
        return None
    
    I = img.astype(np.float32) / 255.0

    # 1. 局所平均フィールド (mu)
    # 7x7のガウシアンフィルタを使用 [cite: 89, 91, 92]
    # 標準偏差はフィルタサイズから適切に設定されるように自動(0)を指定
    mu = cv2.GaussianBlur(I, (7, 7), 0)

    # 2. 局所平均減算フィールド (I - mu) [cite: 101]
    I_mu = I - mu

    # 3. 局所コントラストフィールド (sigma) [cite: 103]
    # (I - mu)^2 にガウシアンフィルタをかけ、その平方根をとる
    sigma = np.sqrt(cv2.GaussianBlur(I_mu**2, (7, 7), 0))

    # 4. 勾配フィールド (ラプラシアン) [cite: 107, 108]
    # ラプラシアン演算子を使用して2次導関数の和を求める
    laplacian = cv2.Laplacian(I, cv2.CV_32F)

    # 5. MSCN係数 [cite: 111, 113]
    # ゼロ除算を防ぐための小さな定数 e を加算
    e = 1e-8
    mscn = I_mu / (sigma + e)

    # 6. MSCN係数のペア積 (水平方向) [cite: 117, 118]
    # 水平方向（列方向）に隣接する画素の積を計算
    mscn_horizontal = mscn[:, :-1] * mscn[:, 1:]

    # --- 統計量の計算関数 ---
    def calculate_statistics(field, split_pos_neg=True):
        """
        与えられたフィールドの平均と分散を計算する
        split_pos_negがTrueの場合は、正の値と負の値に分けて計算する
        """
        if not split_pos_neg:
            # 分割しない場合（I, sigma 用） [cite: 135]
            return [np.mean(field), np.var(field)]
        else:
            # 正負で分割する場合 [cite: 131, 134]
            pos_mask = field >= 0
            neg_mask = field < 0
            
            pos_vals = field[pos_mask]
            neg_vals = field[neg_mask]
            
            # 要素が存在しない場合のゼロ除算エラーを防ぐ
            mu_pos = np.mean(pos_vals) if len(pos_vals) > 0 else 0.0
            var_pos = np.var(pos_vals) if len(pos_vals) > 0 else 0.0
            
            mu_neg = np.mean(neg_vals) if len(neg_vals) > 0 else 0.0
            var_neg = np.var(neg_vals) if len(neg_vals) > 0 else 0.0
            
            return [mu_pos, var_pos, mu_neg, var_neg]

    # --- 特徴量ベクトルの構築 ---
    features = []
    
    # 1. グレースケール画像 (2個)
    features.extend(calculate_statistics(I, split_pos_neg=False))
    
    # 2. 局所平均減算フィールド (4個)
    features.extend(calculate_statistics(I_mu, split_pos_neg=True))
    
    # 3. 局所コントラストフィールド (2個)
    features.extend(calculate_statistics(sigma, split_pos_neg=False))
    
    # 4. 勾配フィールド (ラプラシアン) (4個)
    features.extend(calculate_statistics(laplacian, split_pos_neg=True))
    
    # 5. MSCN係数 (4個)
    features.extend(calculate_statistics(mscn, split_pos_neg=True))
    
    # 6. MSCN係数のペア積 (4個)
    features.extend(calculate_statistics(mscn_horizontal, split_pos_neg=True))

    return features

# --- 使用例 ---
if __name__ == "__main__":
    # 読み込みたい外部画像のファイル名やパスを指定してください
    image_path = 'report_f.png'

    
    # 特徴量の抽出を実行
    feature_vector = extract_image_quality_features(image_path)
    
    if feature_vector:
        print(f"抽出された特徴量の数: {len(feature_vector)}")
        print("特徴量ベクトル:")
        for i, val in enumerate(feature_vector):
            print(f"{val:.6f}")