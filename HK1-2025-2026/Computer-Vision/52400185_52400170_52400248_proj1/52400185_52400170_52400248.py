# 52400185 Văn Hà
# 52400170 Hoài Bảo
# 52400248 Minh Trí

import cv2
import numpy as np
from pathlib import Path
from itertools import combinations

# -------------------- Cấu hình mặc định "ngon" --------------------
ALPHA = 1.35            # hệ số trộn high-pass
LP_K   = 31             # kernel cho LP Averaging/Median/Gaussian (số lẻ)
LP_SIG = 7.0            # sigma Gaussian LP
HP_K   = 31             # kernel cho HP (Gaussian subtraction)
HP_SIG = 7.0            # sigma cho HP
STEPS  = 5              # số ảnh trong strip visualize

# -------------------- Helpers --------------------
def odd(k): return k if k % 2 == 1 else k + 1
def f01(img): return img.astype(np.float32)/255.0
def u8(imgf): imgf = np.clip(imgf,0,1); return (imgf*255.0+0.5).astype(np.uint8)

def resize_to(img, sizeWH):
    return cv2.resize(img, sizeWH, interpolation=cv2.INTER_AREA)

# Low-pass
def lp_averaging(img, k=LP_K):   return cv2.blur(img, (odd(k),odd(k)))
def lp_median(img, k=LP_K):      return cv2.medianBlur(img, odd(k))
def lp_gaussian(img, k=LP_K, s=LP_SIG):
    return cv2.GaussianBlur(img, (odd(k),odd(k)), s, s)
def lp_bilateral(img, d=15, sc=75, ss=75):
    return cv2.bilateralFilter(img, d, sc, ss)

# High-pass (Gaussian subtraction)
def hp_gauss_sub(img, k=HP_K, s=HP_SIG):
    low = lp_gaussian(img, k=k, s=s)
    return cv2.addWeighted(img, 1.0, low, -1.0, 0)

# Hybrid
def make_hybrid(A, B, lp_method="gauss", alpha=ALPHA,
                lp_kwargs=None, hp_kwargs=None):
    lp_kwargs = lp_kwargs or {}
    hp_kwargs = hp_kwargs or {}
    h,w = A.shape[:2]
    B = resize_to(B, (w,h))
    if lp_method == "avg":   A_lp = lp_averaging(A, **lp_kwargs)
    elif lp_method == "median": A_lp = lp_median(A, **lp_kwargs)
    elif lp_method == "gauss":  A_lp = lp_gaussian(A, **lp_kwargs)
    else: A_lp = lp_bilateral(A, **lp_kwargs)
    B_hp = hp_gauss_sub(B, **hp_kwargs)
    H = f01(A_lp) + alpha*f01(B_hp)
    return u8(H)

# Visualization strip
def downsample_strip(img_bgr, steps=STEPS, scale=0.5, gap=12):
    base = img_bgr.copy()
    h0,w0 = base.shape[:2]
    widths = [w0] + [int(w0*(scale**i)) for i in range(1,steps)]
    canvas = np.zeros((h0, sum(widths)+gap*(steps-1), 3), dtype=np.uint8)
    x=0; canvas[:,x:x+w0] = base; x += w0+gap
    curr = base
    for _ in range(1,steps):
        curr = cv2.resize(curr, (max(1,int(curr.shape[1]*scale)),
                                 max(1,int(curr.shape[0]*scale))),
                          interpolation=cv2.INTER_AREA)
        h,w = curr.shape[:2]; y=(h0-h)//2
        canvas[y:y+h, x:x+w] = curr; x += w+gap
    return canvas

# -------------------- Main --------------------
def main():
    root = Path(__file__).resolve().parent
    inp  = root/"input_images"
    out  = root/"output_images"
    vis  = root/"visualize"
    out.mkdir(exist_ok=True); vis.mkdir(exist_ok=True)

    # Đọc 3 ảnh
    paths = [inp/"input_images1.png", inp/"input_images2.png", inp/"input_images3.png"]
    imgs = []
    for p in paths:
        img = cv2.imread(str(p))
        if img is None:
            raise FileNotFoundError(f"Không đọc được ảnh: {p}")
        imgs.append(img)

    # 3 cặp: (1,2), (1,3), (2,3)
    idx_pairs = list(combinations(range(3), 2))
    for (i,j) in idx_pairs:
        A, B = imgs[i], imgs[j]
        pair_name = f"pair{i+1}-{j+1}"
        out_dir = out/pair_name
        out_dir.mkdir(parents=True, exist_ok=True)

        # Tham số mỗi phương pháp
        lp_params = {
            "avg": {"k": LP_K},
            "median": {"k": LP_K},
            "gauss": {"k": LP_K, "s": LP_SIG},
            "bilateral": {"d": 15, "sc": 75, "ss": 75},
        }
        hp_params = {"k": HP_K, "s": HP_SIG}

        hybrids = {}
        for method in ["avg","median","gauss","bilateral"]:
            H = make_hybrid(A, B, lp_method=method, alpha=ALPHA,
                            lp_kwargs=lp_params[method], hp_kwargs=hp_params)
            hybrids[method] = H
            cv2.imwrite(str(out_dir/f"{method}_hybrid.png"), H)

        # visualize từ hybrid Gaussian
        strip = downsample_strip(hybrids["gauss"], steps=STEPS, scale=0.5, gap=12)
        cv2.imwrite(str(vis/f"{pair_name}_visualization.png"), strip)

    print("Done! Xem kết quả trong 'output_images/' và 'visualize/'.")

if __name__ == "__main__":
    main()
