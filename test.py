import torch
print(torch.__version__)          # 確認版本
print(torch.version.cuda)         # CUDA 版本
print(torch.cuda.is_available())  # True 表示 GPU 可用
print(torch.cuda.device_count())  # 幾個 GPU
