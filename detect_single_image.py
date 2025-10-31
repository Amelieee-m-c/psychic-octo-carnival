import os
import cv2
from ultralytics import YOLO

# 🧩 修正 OMP 衝突與多線程問題（避免 Windows 下 OMP 錯誤）
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"

def main():
    # ✅ 模型路徑
    model_path = "runs/detect/tongue_detector5/weights/best.pt"
    model = YOLO(model_path)

    # ✅ 要處理的圖片
    image_path = "chi.png"

    # 檢查圖片是否存在
    if not os.path.exists(image_path):
        print(f"❌ 找不到圖片：{image_path}")
        return

    # ✅ 執行偵測（不顯示視窗，只取結果）
    results = model.predict(
        source=image_path,
        conf=0.5,    # 信心閾值
        save=False,
        show=False
    )

    # ✅ 讀取原始圖片
    img = cv2.imread(image_path)

    # 建立 ROI 輸出資料夾
    output_dir = "roi"
    os.makedirs(output_dir, exist_ok=True)

    # ✅ 逐一處理偵測框
    for i, result in enumerate(results):
        boxes = result.boxes  # 所有框
        if len(boxes) == 0:
            print("⚠️ 沒有偵測到舌頭，請檢查模型或信心閾值設定。")
            continue

        for j, box in enumerate(boxes):
            # 取得座標 (x1, y1, x2, y2)
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # ✅ 裁切 ROI
            roi = img[y1:y2, x1:x2]

            # ✅ 檢查最小尺寸（例如確保不小於 500x500）
            min_size = 500
            h, w = roi.shape[:2]
            
            '''
            if h < min_size or w < min_size:
                print(f"⚠️ ROI 太小 ({w}x{h})，略過。")
                continue
            '''

            # ✅ 儲存裁切後的圖片
            output_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(image_path))[0]}_roi{j+1}.jpg")
            cv2.imwrite(output_path, roi)
            print(f"✅ 已儲存：{output_path}")

if __name__ == "__main__":
    main()
