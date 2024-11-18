from pythonosc.udp_client import SimpleUDPClient

def main():
    # 配置 OSC 目標地址與埠號
    ip = "127.0.0.1"  # 本機地址
    port = 9000       # OSC 埠號
    input_address = "/chatbox/input"  # 輸入聊天訊息的 OSC 路徑
    send_flag_address = "/chatbox/typing"  # 送出訊息的 OSC 路徑 (flag)
    
    # 建立 OSC 客戶端
    client = SimpleUDPClient(ip, port)
    print(f"OSC Client 已連線至 {ip}:{port}")
    print("輸入訊息後按下 Enter 發送，輸入 'exit' 退出程式。")
    
    while True:
        # 從使用者取得輸入
        message = input("> ")
        
        # 檢查是否需要退出
        if message.lower() == "exit":
            print("結束程式。")
            break
        
        # 發送訊息至聊天框
        client.send_message(input_address, [message, True])  # 第二個參數為 "進入文字框模式"
        
        # 發送 typing 標誌（模擬按下 Enter）
        client.send_message(send_flag_address, False)  # 關閉 typing 模式，表示送出訊息
        
        print(f"訊息已發送: {message}")

if __name__ == "__main__":
    main()
