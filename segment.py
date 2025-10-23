import cv2
import numpy as np
import argparse
import os
import time

HMIN_GREEN_DEFAULT = 35
HMIN_BLUE_DEFAULT = 90
HMAX_GREEN_DEFAULT = 85
HMAX_BLUE_DEFAULT = 130
SMIN_DEFAULT = 50
VMIN_DEFAULT = 50
SMAX_DEFAULT = 255
VMAX_DEFAULT = 255

def segment_hsv(img, target, hmin, hmax, smin, smax, vmin, vmax):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    smin_value, vmin_value, smax_value, vmax_value = validateParams(smin, smax, vmin, vmax)
    if target == 'green':
        if hmin is not None:
            hmin_value = hmin
        else:
            hmin_value = HMIN_GREEN_DEFAULT
        if hmax is not None:
            hmax_value = hmax
        else:
            hmax_value = HMAX_GREEN_DEFAULT

        lower = np.array([hmin_value, smin_value, vmin_value])
        upper = np.array([hmax_value, smax_value, vmax_value])
        
    elif target == 'blue':
        if hmin is not None:
            hmin_value = hmin
        else:
            hmin_value = HMIN_BLUE_DEFAULT
        if hmax is not None:
            hmax_value = hmax
        else:
            hmax_value = HMAX_BLUE_DEFAULT

        lower = np.array([hmin_value, smin_value, vmin_value])
        upper = np.array([hmax_value, smax_value, vmax_value])
    else:
        raise ValueError("Target must be 'green' or 'blue'")
    
    mask = cv2.inRange(hsv, lower, upper)
    return mask

def validateParams(smin, smax, vmin, vmax):
    if smin is not None:
        smin_value = smin
    else:
        smin_value = SMIN_DEFAULT
        
    if smax is not None:
        smax_value = smax
    else:
        smax_value = SMAX_DEFAULT
        
    if vmin is not None:
        vmin_value = vmin
    else:
        vmin_value = VMIN_DEFAULT
        
    if vmax is not None:
        vmax_value = vmax
    else:
        vmax_value = VMAX_DEFAULT
    return smin_value, vmin_value, smax_value, vmax_value

def segment_kmeans(img, k, target):
    Z = img.reshape((-1, 3))
    Z = np.float32(Z)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(Z, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    centers[labels.flatten()].reshape(img.shape)
    if target == 'green':
        ref_color = np.array([0, 255, 0])
    else:
        ref_color = np.array([255, 0, 0])
    distances = np.linalg.norm(centers - ref_color, axis=1)
    target_cluster = np.argmin(distances)
    mask = (labels.flatten() == target_cluster).astype(np.uint8) * 255
    mask = mask.reshape((img.shape[0], img.shape[1]))
    return mask

def overlay_mask(img, mask):
    overlay = img.copy()
    overlay[mask > 0] = [0, 255, 0]
    blended = cv2.addWeighted(img, 0.7, overlay, 0.3, 0)
    return blended

def main():
    parser = argparse.ArgumentParser(description="Segmentação com OpenCV")
    parser.add_argument("--input", required=False, help="Caminho da imagem")
    parser.add_argument("--webcam", action="store_true", help="Usar webcam")
    parser.add_argument("--method", choices=["hsv", "kmeans"], required=True)
    parser.add_argument("--target", choices=["green", "blue"], required=True)
    parser.add_argument("--k", type=int, default=7)
    parser.add_argument("--hmin", type=int)
    parser.add_argument("--hmax", type=int)
    parser.add_argument("--smin", type=int)
    parser.add_argument("--smax", type=int)
    parser.add_argument("--vmin", type=int)
    parser.add_argument("--vmax", type=int)
    args = parser.parse_args()
    os.makedirs("outputs", exist_ok=True)
    if args.webcam:
        cap = cv2.VideoCapture(0)
        ret, img = cap.read()
        cap.release()
        if not ret:
            print("Erro ao capturar da webcam.")
            return
    else:
        img = cv2.imread(args.input)
        if img is None:
            print("Erro ao carregar imagem.")
            return
    start = time.time()
    if args.method == "hsv":
        mask = segment_hsv(img, args.target, args.hmin, args.hmax, args.smin, args.smax, args.vmin, args.vmax)
    else:
        mask = segment_kmeans(img, args.k, args.target)
    overlay = overlay_mask(img, mask)
    elapsed = time.time() - start
    percent = np.sum(mask > 0) / mask.size * 100
    print(f"Tempo: {elapsed:.2f}s | Pixels segmentados: {percent:.2f}%")
    base_name = os.path.splitext(os.path.basename(args.input or 'webcam'))[0]
    cv2.imwrite(f"outputs/{base_name}_mask.png", mask)
    cv2.imwrite(f"outputs/{base_name}_overlay.png", overlay)
    print("Resultados salvos em outputs/")

if __name__ == "__main__":
    main()
