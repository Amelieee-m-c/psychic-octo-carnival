import torch

def count_parameters(model_path):
    """
    計算PyTorch模型的參數量 (支援一般模型和YOLOv8)
    
    Args:
        model_path: .pth 或 .pt 檔案路徑
    """
    print(f"\n正在載入模型: {model_path}\n")
    
    # 載入模型
    checkpoint = torch.load(model_path, map_location='cpu', weights_only=False)
    
    print(f"檔案類型: {type(checkpoint)}")
    
    # 如果是字典,顯示所有的 key
    if isinstance(checkpoint, dict):
        print(f"字典的 keys: {list(checkpoint.keys())}\n")
    
    # 處理不同的儲存格式
    state_dict = None
    
    if isinstance(checkpoint, dict):
        # 嘗試不同的 key 來找出 state_dict
        possible_keys = ['model', 'state_dict', 'model_state_dict', 'ema', 'model.state_dict']
        
        for key in possible_keys:
            if key in checkpoint:
                candidate = checkpoint[key]
                # 如果找到的是模型物件,嘗試取得其 state_dict
                if hasattr(candidate, 'state_dict'):
                    state_dict = candidate.state_dict()
                    print(f"從 '{key}' 取得 state_dict (模型物件)")
                    break
                elif hasattr(candidate, 'float'):
                    state_dict = candidate.float().state_dict()
                    print(f"從 '{key}' 取得 state_dict (模型物件)")
                    break
                elif isinstance(candidate, dict):
                    state_dict = candidate
                    print(f"使用 '{key}' 作為 state_dict")
                    break
        
        # 如果還是沒找到,使用整個 checkpoint
        if state_dict is None:
            state_dict = checkpoint
            print("使用整個 checkpoint 作為 state_dict")
    else:
        # 如果不是字典,可能是模型物件
        if hasattr(checkpoint, 'state_dict'):
            state_dict = checkpoint.state_dict()
            print("從模型物件取得 state_dict")
        else:
            state_dict = checkpoint
            print("直接使用載入的內容")
    
    # 計算總參數量
    total_params = 0
    layer_count = 0
    
    print("\n" + "=" * 80)
    print("模型參數詳細資訊")
    print("=" * 80)
    print(f"{'層名稱':<60} | {'參數數量':>15}")
    print("-" * 80)
    
    for name, param in state_dict.items():
        if isinstance(param, torch.Tensor):
            num_params = param.numel()
            total_params += num_params
            layer_count += 1
            
            # 顯示參數形狀
            shape_str = str(tuple(param.shape))
            print(f"{name:<60} | {num_params:>15,}")
    
    print("=" * 80)
    print(f"層數量: {layer_count}")
    print(f"總參數量: {total_params:,}")
    print(f"總參數量 (百萬): {total_params / 1e6:.2f}M")
    print(f"總參數量 (十億): {total_params / 1e9:.4f}B")
    
    # 估計模型大小
    model_size_mb = (total_params * 4) / (1024 ** 2)  # 假設 float32
    print(f"估計模型大小 (float32): {model_size_mb:.2f} MB")
    print("=" * 80 + "\n")
    
    return total_params

# 使用方式
if __name__ == "__main__":
    # YOLOv8 模型路徑
    model_path = "C:/Users/msp/Downloads/TongueDataset.v2i.yolov8/yolov8n.pt"
    
    try:
        total = count_parameters(model_path)
    except FileNotFoundError:
        print(f"錯誤: 找不到檔案 '{model_path}'")
        print("請修改 model_path 變數為您的實際檔案路徑")
    except Exception as e:
        print(f"錯誤: {e}")
        import traceback
        traceback.print_exc()
        print("\n提示:")
        print("- 確認檔案路徑是否正確")
        print("- 確認 PyTorch 版本是否相容")
        print("- YOLOv8 模型可能需要 ultralytics 套件")