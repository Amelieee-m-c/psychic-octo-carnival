import pandas as pd

# 讀取 results.csv
df = pd.read_csv("C:/Users/msp/Downloads/TongueDataset.v2i.yolov8/runs/detect/tongue_detector5/results.csv")

# 要分析的欄位
metrics = [
    "metrics/precision(B)",
    "metrics/recall(B)",
    "metrics/mAP50(B)",
    "metrics/mAP50-95(B)"
]

# 最後一個 epoch 的結果
last_epoch = df.iloc[-1][metrics]

# 各指標最大值與對應 epoch
max_metrics = {}
max_epochs = {}

for m in metrics:
    max_metrics[m] = df[m].max()
    max_epochs[m] = df.loc[df[m].idxmax(), "epoch"]

print("📊 YOLOv8 訓練結果分析")
print("=" * 40)
print("👉 最後一個 Epoch 成績：")
for k, v in last_epoch.items():
    print(f"  {k}: {v:.4f}")

print("\n👉 各指標最高成績：")
for k in metrics:
    print(f"  {k}: {max_metrics[k]:.4f}  (出現在第 {int(max_epochs[k])} epoch)")

# 若想輸出成 CSV 檔
output = pd.DataFrame({
    "Metric": metrics,
    "Last_Epoch": last_epoch.values,
    "Max_Value": [max_metrics[m] for m in metrics],
    "At_Epoch": [max_epochs[m] for m in metrics]
})
output.to_csv("metrics_summary.csv", index=False)
print("\n✅ 結果已輸出到 metrics_summary.csv")
