import pyautogui
import time
import pyperclip

def waterdepth():
    with open("D:/OneDrive/桌面/arduno/waterdepth.txt", "r") as file_Obj:
        r = file_Obj.readlines()
        return r[-1]
    
time.sleep(20)


v = 0
#無限迴圈
while 5 == 5:
    msg = int(waterdepth()[0:2])
    if msg <= 20:
        if v != 1:
            pyautogui.hotkey('alt', 'd')
            pyperclip.copy("https://maker.ifttt.com/trigger/simon/with/key/hmX-SxuKU4F_rKRcIw4BIRBbiy4gy-KU_a4d_fZK_Pd?value1=請離開,開始啟動減災措施")
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')
            v = 1
    elif msg <= 21:
        if v != 2:
            pyautogui.hotkey('alt', 'd')
            pyperclip.copy("https://maker.ifttt.com/trigger/simon/with/key/hmX-SxuKU4F_rKRcIw4BIRBbiy4gy-KU_a4d_fZK_Pd?value1=請注意淹水")
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')
            v = 2

    print(msg)
    time.sleep(10)