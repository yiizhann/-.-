import requests
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# 建立 headless 瀏覽器並擷取網站畫面
def capture():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1280,720')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.get("https://hiosha.osha.gov.tw/content/info/heat1.aspx")
    time.sleep(5)
    driver.save_screenshot("heat.png")
    driver.quit()

# 傳送圖片到 LINE 群組
def push():
    token = os.getenv("CHANNEL_ACCESS_TOKEN")
    group_id = os.getenv("GROUP_ID")
    now = datetime.datetime.now().strftime("%m/%d %H:%M")
    text = f"{now} 熱危害：第？級 請人員注意。"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 先發文字
    requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json={
        "to": group_id,
        "messages": [{"type": "text", "text": text}]
    })

    # 再發圖片
    with open("heat.png", "rb") as f:
        image_data = f.read()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    requests.post(
        "https://api-data.line.me/v2/bot/message/push",
        headers=headers,
        files={
            "message": (None, "當前熱危害圖"),
            "imageFile": ("heat.png", image_data, "image/png")
        }
    )

if __name__ == "__main__":
    import os
    capture()
    push()
