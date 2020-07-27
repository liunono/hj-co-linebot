import gspread
from oauth2client.service_account import ServiceAccountCredentials
     scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/drive']
     creds = ServiceAccountCredentials.from_json_keyfile_name("./creds.json", scope)
     client = gspread.authorize(creds)
     sheet = client.open("base").sheet1


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    input_text = event.message.text
    cell = sheet.find(input_text)
    row = cell.row
    cell.value=sheet.cell(row,2).value
    data = cell.value
    line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=data))