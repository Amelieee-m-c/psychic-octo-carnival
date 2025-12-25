import time

# 假設這是你從原始碼中拿到的 pool
pool = ["A", "B", "C", "D", "FLAG", "E", "F"] # 範例數據
target_item = "FLAG" # 你想抽到的東西

# 找出目標在 pool 裡的 index (有多個的話要都要找)
target_indices = [i for i, x in enumerate(pool) if x == target_item]

if not target_indices:
    print("Pool 裡找不到目標，請確認 pool 內容")
    exit()

pool_len = len(pool)
current_ts = int(time.time())

# 搜尋未來 1000 秒內的時間點
print(f"正在尋找可以抽到 {target_item} 的時間點...")

for offset in range(1000):
    test_ts = current_ts + offset
    
    # 模擬抽卡邏輯
    # 這裡要注意：如果你是一次抽 10 連 (cnt=10)，Flag 可能出現在第 1 抽到第 10 抽的任一位置
    cnt = 10 # 假設是十連抽，如果是單抽改成 1
    idx = test_ts % pool_len 
    
    found = False
    for pull_order in range(cnt):
        idx = (idx + 39) % pool_len
        if idx in target_indices:
            print(f"[!] 找到解了！")
            print(f"    時間戳: {test_ts}")
            print(f"    還有幾秒: {offset} 秒後")
            print(f"    出現在第 {pull_order + 1} 抽")
            found = True
            break
            
    if found:
        # 如果只想找最近的一個，可以在這裡 break
        # break 
        pass