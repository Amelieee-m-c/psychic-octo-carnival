from pwn import *
import re

# 修改 Port 為 29060
host = '203.145.203.94'
port = 29060

r = remote(host, port)

# 讀掉開頭的標題 (如果有)
try:
    # 先讀一行看看，避免標題卡住
    header = r.recvline(timeout=2).decode()
    print(f"Header: {header.strip()}")
except:
    pass

print("[*] Starting the game...")

try:
    while True:
        # 讀取到問號或冒號為止，這樣比較通用
        # 為了保險，我們讀取 '?'，如果卡住可以改成讀取 ':' 或其他符號
        prompt = r.recvuntil(['?', ':', '...']).decode()
        
        # 顯示當前收到的訊息 (除錯用，如果刷太快可以註解掉)
        # print(f"Prompt: {prompt}")

        # 檢查是否出現 Flag
        if "CTF{" in prompt or "flag" in prompt.lower():
            print("\n[+] Flag Found! ==========================")
            print(prompt)
            # 把它讀完確保完整顯示
            print(r.recvall(timeout=2).decode())
            break

        # 正則表達式提取數字
        # 這裡同時支援 "I say 123" 和 "我說 123" 的格式
        # \d+ 表示抓取連續數字
        match = re.search(r'(\d+)', prompt)
        
        if match:
            # 為了避免抓到題目開頭的 "1." 或 "No.1"，我們通常抓最後一個出現的數字
            # 但這題很單純，通常只有一個數字。
            # 如果發現抓錯，可以改用 r'say (\d+)' 來定位
            number = match.group(1)
            
            # 這裡把 print 註解掉可以跑更快
            # print(f"Sending: {number}")
            
            r.sendline(number.encode())
        else:
            print(f"[-] No number found in: {prompt}")
            # 如果格式變了，這裡會印出來讓你知道
            break

except EOFError:
    print("\n[*] Connection closed. (Check above if flag was printed)")
    r.interactive()
except Exception as e:
    print(f"Error: {e}")