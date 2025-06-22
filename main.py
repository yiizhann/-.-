import os
import requests
from datetime import datetime
from linebot import LineBotApi
from linebot.models import FlexSendMessage
from PIL import Image
from io import BytesIO

# 設定參數
token_url = "http://goat.pakka.ai:8008/wbgt?token=47fc5150d1ae4f1290bf43e9d4746b5e"
img_url = "http://goat.pakka.ai:8008/wbgt"

# 環境變數
channel_access_token = os.getenv("CHANNEL_ACCESS_TOKEN")
group_id = os.getenv("GROUP_ID")
line_bot_api = LineBotApi(channel_access_token)

# 擷取等級
level = "未知"
try:
    r = requests.get(token_url, timeout=10)
    if r.ok:
        data = r.text.strip()
        level = data.split(":")[-1].strip()
except Exception as e:
    level = "無法取得"

# 擷取圖片並裁切
try:
    screenshot = requests.get(img_url, timeout=10)
    img = Image.open(BytesIO(screenshot.content))
    crop_box = (345, 260, 930, 580)
    cropped_img = img.crop(crop_box)
    cropped_img.save("heat_index.png")
except Exception as e:
    print("圖片擷取錯誤", e)

# 時間字串
now = datetime.now()
time_str = now.strftime("%m/%d %H:%M")

# Flex Message
flex_message = FlexSendMessage(
    alt_text="熱危害警示",
    contents={
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": f"{time_str} 熱危害：{level}", "size": "lg", "weight": "bold", "color": "#d32f2f"},
                {"type": "image", "url": "https://github.com/yiizhann/-.-/raw/main/heat_index.png", "size": "full", "aspectMode": "cover"}
            ]
        }
    }
)

# 推送
try:
    line_bot_api.push_message(group_id, flex_message)
except Exception as e:
    print("推送錯誤：", e)
