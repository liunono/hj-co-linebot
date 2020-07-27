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
secretFileContentJson=json.load(open("../line_secret_key",'r',encoding="utf-8"))
server_url=secretFileContentJson.get("server_url")

# 設定Server啟用細節
app = Flask(__name__,static_url_path = "/images" , static_folder = "../images/")

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


import gspread
from oauth2client.service_account import ServiceAccountCredentials
     scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/drive']
     creds = ServiceAccountCredentials.from_json_keyfile_name("./creds.json", scope)
     client = gspread.authorize(creds)

@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    sheet = client.open("base").sheet1
    input_text = event.message.text
    cell = sheet.find(input_text)
    row = cell.row
    cell.value=sheet.cell(row,2).value
    data = cell.value
    line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=data))