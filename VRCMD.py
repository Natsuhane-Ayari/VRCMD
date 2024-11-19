import pyperclip  # 用於操作剪貼簿
from pynput.keyboard import Controller, Key
from pythonosc.udp_client import SimpleUDPClient
import time

def printHelp():
    print("::kbd\t切換至自動按鍵模式")
    print("\t此模式將會使用 'Alt+Tab Ctrl+V' 自動將訊息傳入VRChat")
    print("\t(如果你希望你的朋友能聽見提示音，建議使用此選項)")
    print("::osc\t切換至OSC模式")
    print("\t此模式使用OSC將訊息傳入VRChat")
    print("\t(由於OSC的限制，使用OSC發送訊息，別人將無法聽見提示音)")
    print("::atb\t自動返回VRChat ※僅在OSC模式下可用 此功能預設關閉")
    print("\t啟用後 按下Enter鍵送出訊息後，立即使用Alt+Tab返回VRChat")
    print("\t此功能啟用狀態下，再輸入一次即關閉此功能")
    print("::exit\t退出程式")
    print("::help\t顯示此幫助")

def useKbd():
    keyboard = Controller()
    
    print("輸入訊息後按下 Enter 發送，輸入 '::exit' 退出程式。")
    print("請注意 上一個焦點視窗必須是VRChat，此程式會使用Alt+Tab")
    print("輸入 '::help' 查看更多選項")

    while True:
        # Step 1: 從命令行接收輸入
        message = input("> ")

        #指令切換
        if message.lower() == "::exit":
            break
        elif message.lower() == "::kbd":
            break
        elif message.lower() == "::osc":
            break
        elif message.lower() == "::help":
            printHelp()
            continue

        # Step 2: 複製訊息到剪貼簿
        pyperclip.copy(message)
        print(f"發送訊息: {message}")

        # Step 3: 模擬按下 Alt+Tab 切換到 VRChat
        keyboard.press(Key.alt_l)  # 按下左 Alt
        keyboard.press(Key.tab)   # 按下 Tab
        keyboard.release(Key.tab) # 釋放 Tab
        keyboard.release(Key.alt_l)  # 釋放 Alt
        time.sleep(0.3)  # 等待窗口切換完成

        keyboard.press('y')
        time.sleep(0.1)
        keyboard.release('y')
        time.sleep(0.2)
        

        # Step 4: 模擬 Ctrl+V 貼上訊息
        keyboard.press(Key.ctrl_l)  # 按下左 Ctrl
        keyboard.press('v')         # 按下 V
        keyboard.release('v')       # 釋放 V
        keyboard.release(Key.ctrl_l)  # 釋放 Ctrl
        time.sleep(0.2)  # 等待貼上完成

        # Step 5: 模擬按下 Enter 送出訊息
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        time.sleep(0.2)  # 等待送出完成

        # Step 6: 模擬按下 Esc 關閉聊天框
        keyboard.press(Key.esc)
        time.sleep(0.07)
        keyboard.release(Key.esc)
        print("訊息已送出")
    return message

def useOSC():
    # 配置 OSC 目標地址與埠號
    ip = "127.0.0.1"  # 本機地址
    port = 9000       # OSC 埠號
    input_address = "/chatbox/input"  # 輸入聊天訊息的 OSC 路徑
    send_flag_address = "/chatbox/typing"  # 送出訊息的 OSC 路徑 (flag)
    keyboard = Controller()
    autoback = False
    
    # 建立 OSC 客戶端
    client = SimpleUDPClient(ip, port)
    print(f"OSC Client 已連線至 {ip}:{port}")
    print("輸入訊息後按下 Enter 發送，輸入 '::exit' 退出程式。")
    print("輸入 '::help' 查看更多選項")
    
    while True:
        # 從使用者取得輸入
        message = input("> ")
        
        # 檢查是否需要退出
        if message.lower() == "::exit":
            break
        elif message.lower() == "::kbd":
            break
        elif message.lower() == "::osc":
            break
        elif message.lower() == "::atb":
            if autoback == False:
                print("自動返回VRChat 已開啟")
                print("請注意 上一個視窗焦點必須是VRChat")
            else:
                print("自動返回VRChat 已關閉")
            autoback = not autoback
            continue
        elif message.lower() == "::help":
            printHelp()
            continue
        
        # 發送訊息至聊天框
        client.send_message(input_address, [message, True])  # 第二個參數為 "進入文字框模式"
        
        # 發送 typing 標誌（模擬按下 Enter）
        client.send_message(send_flag_address, False)  # 關閉 typing 模式，表示送出訊息
        
        print(f"發送訊息: {message}")
        print("訊息已送出")
        if autoback == True:
            time.sleep(0.2)
            keyboard.press(Key.alt_l)  # 按下左 Alt
            keyboard.press(Key.tab)   # 按下 Tab
            keyboard.release(Key.tab) # 釋放 Tab
            keyboard.release(Key.alt_l)  # 釋放 Alt
    return message

def main():
    message = useKbd()

    while True:
        if message.lower() == "::kbd":
            print("已切換至自動按鍵模式")
            message = useKbd()
        elif message.lower() == "::osc":
            print("已切換至OSC模式")
            message = useOSC()
        elif message.lower() == "::exit":
            print("結束程式。")
            break


if __name__ == "__main__":
    main()
