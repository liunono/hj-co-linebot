
# coding: utf-8

# In[ ]:


# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/drive']
# creds = ServiceAccountCredentials.from_json_keyfile_name("./creds.json", scope)
# client = gspread.authorize(creds)

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

# 辞書オブジェクト。認証に必要な情報をHerokuの環境変数から呼び出している
credential = {
                 "type": "service_account",
  "project_id": "linebot-284103",
  "private_key_id": "67e6698c309950fc7b3c8862c083ae300b765fe4",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCrbv4eQHX6Bxl+\n8PfKWdzKJTKBpeK5NSW4Kow3kFiLvT5EPU15o83UlglmnoomKFn+Lgf3gne+oMaZ\nPiTtxSrOl5L7pl0IEW+Fovy6knsBnpvS9+fNMXNjygl/HIms/MdB9CMoAeSBRxm0\nTGgHK8xKwpuoS6aEd4AGRVEjQzrMnyDA0IRIKPi9IM5NIx+uBT4p2KUkOV3bKtgW\n8PVJYTJTIRYuFc2jg0xgokwAZMh1m7H/c25vM/g8MobQYnNwLgayxY2axu37HtcA\nwds8ROBtrK/9lF+Swj5dEr3DnMow1zqxwrCYcCDw+15wbhF30hZqyasGUitDKEgb\nkCFFZQpxAgMBAAECggEACFdv3j829l3k0dJODk6p0Xy2nMwacHZbcd8BIF2Bz3fb\neSTN+aScqfLMfY2qjXGCcn2hJdwXcUM/spptX9Prka6aqGvHhFJb3bHo7/ebbGBg\nNudY5Dk7IwCETobwFIaet/D2CnbwHFG+OJGMsMei6sLWId3fefvaEwQJrwhxCp6B\np4APq+nFwXjE78gtxU73NX1h26tsvPpA8xzRP/tNRhDG2BGAipWHefQjrsrvN/By\nm+RGRiZDRSBXnOAB9yaPR1P/R4xFWbRGNnNu/O/kEvBJuW71W8+pD8fn6cvT0rLy\n+sBfSnnEHkpvsQPhwynN3s9WcArhHxTb6Kfh++x3eQKBgQDbyqiodVZ1JAD56oVD\nyZHNQjeVcXGa44vn+wEpOnhkV5exFEJ7BO4aq1bdf3fNDGaq74fzrnOvfswNqEHK\nm8vLWcwkrWpOuOYqgD4q9yepLlkBDcQhblOijF4mczeaLp4xUlwzWRhbs8QykSdr\nFbFr2FXd5fv098idN9xUSsUPOQKBgQDHrOnwjsKa8JOMnJGh2gQIRk0NKlfmaxfL\nPd0AtRU9GXd62VBCIA6pYCY9z0x+RBhGFYnoMxNcAXU5tXMCMAfDUbocd7+2+R4E\nj2T6Btjq4CCAm6VuN8cd1PufWxfb8b5lXc6B6nQC2UiiLWbW8tNI2m0Jt2/MRNpD\nuDfEr4cc+QKBgHQlO8sJdo6gYAOw8otH0UxuWYEXWblH1X7ZHVv0Efq0buyckCUC\nDfD56gVSfrRUgUyDF4yl+2wZzSrKZznx6lejNEWNfkfrXXXIHxIFWWgFnfL4m1Qv\nQPL8yiP3bsKDMAVQSHi59C1BacRvAC2OYRtkTrvb9LEW32R1SHEisc/BAoGAPK6r\nJgVs1QOaA9itVZ/ZK96Zmg+tSQRw5b52RLnDq57qtbYHcyEk84qZ9JzkZVcyfVIc\naCnlj0eOJaykOBz6rvxOcEpgRC4vVjlx+Z5NHAxjNFKZEwb2h3VrxwE7Hge40juQ\n/+CNwzPfpBHiOB7x4SkojBRocI7YOk5o/GhPypkCgYEApXu6l7NW6WJLXd/ebH1U\n2JPuu5RzV036ZtJXeqQX8cmxsiykhr9GkZIDsXzn3LCvHc419UhJuRrNjfnU//pS\n5Cbt2sIV7vvTH+9gWtGw2z9+GHmeYEgySGB0KcHPyEH819PMtlpr1TaM3SDOOUsV\nbSNvhdEapiv5ug4Spa6VEUI=\n-----END PRIVATE KEY-----\n",
  "client_email": "linebot@linebot-284103.iam.gserviceaccount.com",
  "client_id": "103853022194133886262",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": os.environ['SHEET_CLIENT_X509_CERT_URL']
}

credentials = ServiceAccountCredentials.from_json_keyfile_dict(credential, scope)

gc = gspread.authorize(credentials)

'''

整體功能描述

'''


# In[ ]:


'''

Application 主架構

'''

# 引用Web Server套件
from flask import Flask, request, abort

# 從linebot 套件包裡引用 LineBotApi 與 WebhookHandler 類別
from linebot import (
    LineBotApi, WebhookHandler
)

# 引用無效簽章錯誤
from linebot.exceptions import (
    InvalidSignatureError
)

# 載入json處理套件
import json

# 載入基礎設定檔
secretFileContentJson=json.load(open("./line_secret_key",'r',encoding='utf8'))
server_url=secretFileContentJson.get("server_url")

# 設定Server啟用細節
app = Flask(__name__,static_url_path = "/素材" , static_folder = "./素材/")

# 生成實體物件
line_bot_api = LineBotApi(secretFileContentJson.get("channel_access_token"))
handler = WebhookHandler(secretFileContentJson.get("secret_key"))

# 啟動server對外接口，使Line能丟消息進來
@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'
    
    
@app.route('/')
def hello():
    return 'Hello World!'


# In[ ]:


'''

消息判斷器

讀取指定的json檔案後，把json解析成不同格式的SendMessage

讀取檔案，
把內容轉換成json
將json轉換成消息
放回array中，並把array傳出。

'''

# 引用會用到的套件
from linebot.models import (
    ImagemapSendMessage,TextSendMessage,ImageSendMessage,LocationSendMessage,FlexSendMessage,VideoSendMessage
)

from linebot.models.template import (
    ButtonsTemplate,CarouselTemplate,ConfirmTemplate,ImageCarouselTemplate
    
)

from linebot.models.template import *

def detect_json_array_to_new_message_array(fileName):
    
    #開啟檔案，轉成json
    with open(fileName,encoding='utf8') as f:
        jsonArray = json.load(f)
    
    # 解析json
    returnArray = []
    for jsonObject in jsonArray:

        # 讀取其用來判斷的元件
        message_type = jsonObject.get('type')
        
        # 轉換
        if message_type == 'text':
            returnArray.append(TextSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'imagemap':
            returnArray.append(ImagemapSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'template':
            returnArray.append(TemplateSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'image':
            returnArray.append(ImageSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'sticker':
            returnArray.append(StickerSendMessage.new_from_json_dict(jsonObject))  
        elif message_type == 'audio':
            returnArray.append(AudioSendMessage.new_from_json_dict(jsonObject))  
        elif message_type == 'location':
            returnArray.append(LocationSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'flex':
            returnArray.append(FlexSendMessage.new_from_json_dict(jsonObject))  
        elif message_type == 'video':
            returnArray.append(VideoSendMessage.new_from_json_dict(jsonObject))    


    # 回傳
    return returnArray


# In[ ]:


'''

handler處理關注消息

用戶關注時，讀取 素材 -> 關注 -> reply.json

將其轉換成可寄發的消息，傳回給Line

'''

# 引用套件
from linebot.models import (
    FollowEvent
)

# 關注事件處理
@handler.add(FollowEvent)
def process_follow_event(event):
    
    # 讀取並轉換
    result_message_array =[]
    replyJsonPath = "素材/啟動呆呆婷/reply.json"
    result_message_array = detect_json_array_to_new_message_array(replyJsonPath)

    # 消息發送
    line_bot_api.reply_message(
        event.reply_token,
        result_message_array
    )


# In[ ]:


'''

handler處理文字消息

收到用戶回應的文字消息，
按文字消息內容，往素材資料夾中，找尋以該內容命名的資料夾，讀取裡面的reply.json

轉譯json後，將消息回傳給用戶

'''

# 引用套件
from linebot.models import (
    MessageEvent, TextMessage
)

# 文字消息處理
@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    sheet = gc.open("base").sheet1
    input_text = event.message.text
    try:
        cell = sheet.find(input_text)
        row = cell.row
        cell.value=sheet.cell(row,2).value
        data = cell.value
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=data))
    except gspread.exceptions.CellNotFound:
        result_array = process_text_message(event)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=data))

def process_text_message(event):
    replyJsonPath = "素材/" + event.message.text + "/reply.json"
    result_message_array = detect_json_array_to_new_message_array(replyJsonPath)
    line_bot_api.reply_message(event.reply_token,result_message_array)


# In[ ]:


'''

handler處理Postback Event

載入功能選單與啟動特殊功能

解析postback的data，並按照data欄位判斷處理

現有三個欄位
menu, folder, tag

若folder欄位有值，則
    讀取其reply.json，轉譯成消息，並發送

若menu欄位有值，則
    讀取其rich_menu_id，並取得用戶id，將用戶與選單綁定
    讀取其reply.json，轉譯成消息，並發送

'''
from linebot.models import (
    PostbackEvent
)

from urllib.parse import parse_qs 

@handler.add(PostbackEvent)
def process_postback_event(event):
    


    query_string_dict = parse_qs(event.postback.data)
    
    print(query_string_dict)
    if 'folder' in query_string_dict:
    
        result_message_array =[]

        replyJsonPath = '素材/'+query_string_dict.get('folder')[0]+"/reply.json"
        result_message_array = detect_json_array_to_new_message_array(replyJsonPath)
  
        line_bot_api.reply_message(
            event.reply_token,
            result_message_array
        )
    elif 'menu' in query_string_dict:
 
        linkRichMenuId = open("素材/"+query_string_dict.get('menu')[0]+'/rich_menu_id', 'r').read()
        line_bot_api.link_rich_menu_to_user(event.source.user_id,linkRichMenuId)
        
        replyJsonPath = '素材/'+query_string_dict.get('menu')[0]+"/reply.json"
        result_message_array = detect_json_array_to_new_message_array(replyJsonPath)
  
        line_bot_api.reply_message(
            event.reply_token,
            result_message_array
        )


# In[ ]:


'''

Application 運行（開發版）

'''
# if __name__ == "__main__":
#     app.run(host='0.0.0.0')


# In[ ]:


'''

Application 運行（heroku版）

'''

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])

