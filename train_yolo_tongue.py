import os

# 🧩 修正 OMP 衝突與多線程問題
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"

from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO("yolov8n.pt")  # 使用輕量模型開始訓練

    model.train(
        data="data.yaml",
        epochs=50,
        imgsz=640,
        batch=8,          # 建議先用小一點，降低記憶體壓力
        name="tongue_detector5",  # 重新命名新的訓練結果
        workers=0,        # Windows 請設為 0 避免 spawn 問題
        device=0 if os.system("nvidia-smi >nul 2>&1") == 0 else "cpu",  # 自動偵測GPU
    )
