import os
import cv2
from tqdm import tqdm
from ultralytics import YOLO

# 模型路徑（訓練完成後自動生成）
MODEL_PATH = "runs/detect/tongue_detector5/weights/best.pt"

# 輸入與輸出資料夾
INPUT_FOLDER = "test/images"
OUTPUT_FOLDER = "tongue_ROI_only"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 載入模型
model = YOLO(MODEL_PATH)

for filename in tqdm(os.listdir(INPUT_FOLDER), desc="Detecting Tongues"):
    if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue

    img_path = os.path.join(INPUT_FOLDER, filename)
    img = cv2.imread(img_path)
    results = model(img)

    for i, box in enumerate(results[0].boxes.xyxy.cpu().numpy()):
        # 直接用模型偵測框裁切，不做擴展
        x1, y1, x2, y2 = map(int, box)
        roi = img[y1:y2, x1:x2]

        save_name = f"{os.path.splitext(filename)[0]}_roi_{i}.jpg"
        cv2.imwrite(os.path.join(OUTPUT_FOLDER, save_name), roi)

print(f"✅ 偵測與ROI擷取完成，輸出於：{OUTPUT_FOLDER}/")
