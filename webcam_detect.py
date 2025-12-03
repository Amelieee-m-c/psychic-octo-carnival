import cv2
import math
from ultralytics import YOLO

# ================= 設定區 =================
# 模型路徑 (請確認 best.pt 已經複製到這個資料夾)
MODEL_PATH = "best.pt"

# 距離判斷標準 (舌頭佔畫面面積的比例)
# 如果一直顯示太遠，請把這個數字調小 (例如 0.10)
# 如果一直顯示太近，請把這個數字調大 (例如 0.20)
SIZE_THRESHOLD = 0.15 

# 信心度門檻 (只顯示信心度大於 0.5 的結果，避免誤判)
CONF_THRESHOLD = 0.5
# =========================================

# 載入模型
try:
    print(f"正在載入模型: {MODEL_PATH} ...")
    model = YOLO(MODEL_PATH)
except Exception as e:
    print(f"❌ 找不到模型或載入失敗: {e}")
    print("⚠️  將暫時使用 yolov8n.pt 進行測試 (只會偵測人/物體)")
    model = YOLO("yolov8n.pt")

# 開啟攝影機
# 改用 MSMF 驅動，並嘗試 index 0
cap = cv2.VideoCapture(1, cv2.CAP_MSMF)

# 設定字體
FONT = cv2.FONT_HERSHEY_SIMPLEX

print("🟢 程式已啟動，按下 'q' 鍵離開")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("❌ 無法讀取鏡頭畫面")
        break

    # 1. ⭐ 優化：鏡像翻轉 (讓畫面像照鏡子一樣，方便對準)
    frame = cv2.flip(frame, 1)

    # 取得畫面總面積
    frame_height, frame_width = frame.shape[:2]
    frame_area = frame_height * frame_width

    # 2. ⭐ 優化：加入 conf 參數過濾低信心度的誤判
    results = model.predict(frame, verbose=False, conf=CONF_THRESHOLD)

    # 預設狀態 (未偵測到)
    status_text = "Searching..."
    status_color = (200, 200, 200) # 灰色

    for result in results:
        boxes = result.boxes
        for box in boxes:
            # 取得座標
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            # 計算舌頭框框面積
            box_w = x2 - x1
            box_h = y2 - y1
            box_area = box_w * box_h
            
            # 計算佔比
            ratio = box_area / frame_area

            # 3. ⭐ 優化：邏輯判斷 (太遠 vs OK)
            # OpenCV 不支援中文顯示，所以用英文代替，但用了顏色區分
            if ratio < SIZE_THRESHOLD:
                # ❌ 太遠 (紅色)
                color = (0, 0, 255) 
                # 這裡顯示數值，方便你除錯
                label = f"Too Far! ({ratio:.1%})"
                instruction = "MOVE CLOSER"
            else:
                # ✅ OK (綠色)
                color = (0, 255, 0)
                label = f"Good! ({ratio:.1%})"
                instruction = "HOLD STILL"

            # 畫出框框
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)

            # 畫出標籤背景
            cv2.rectangle(frame, (x1, y1 - 60), (x2, y1), color, -1)

            # 寫上狀態文字 (上方小字顯示比例)
            cv2.putText(frame, label, (x1 + 5, y1 - 35), FONT, 0.6, (255, 255, 255), 1)
            # 寫上指令文字 (下方大字)
            cv2.putText(frame, instruction, (x1 + 5, y1 - 10), FONT, 0.8, (255, 255, 255), 2)

    # 顯示畫面
    cv2.imshow("Tongue Diagnosis AI", frame)

    # 按下 'q' 退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()