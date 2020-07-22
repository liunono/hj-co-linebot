
from __future__ import print_function
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

Gets valid user credentials from storage.
If nothing has been stored, or if the stored credentials are invalid,
the OAuth2 flow is completed to obtain the new credentials.
Returns:
Credentials, the obtained credential.

def getCredentials():

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheet api'

try:
import argparse
flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
flags = None
 
 # 授權目錄
credential_dir = '.credentials'
 
    # 取得授權紀錄
if not os.path.exists(credential_dir):
os.makedirs(credential_dir)
credential_path = os.path.join(credential_dir, 'sheets.googleapis.com-python-quickstart.json')
store = Storage(credential_path)
credentials = store.get()
 
# 判斷是否有授權紀錄或是受全是否失效，若沒有或失效則重新或取授權並儲存授權
if not credentials or credentials.invalid:
clientsecret_path = os.path.join(credential_dir, CLIENT_SECRET_FILE)
flow = client.flow_from_clientsecrets(clientsecret_path, SCOPES)
flow.user_agent = APPLICATION_NAME
if flags:
credentials = tools.run_flow(flow, store, flags)
else: # Needed only for compatibility with Python 2.6
credentials = tools.run(flow, store)
print('Storing credentials to' + credential_path)
return credentials'

def getSheetValue(spreadsheetId, rangeName):

# 建立 Google Sheet API 連線
credentials = getCredentials()
http = credentials.authorize(httplib2.Http())
discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?' 'version=v4')
service = discovery.build('sheets','v4',http=http, discoveryServiceUrl=discoveryUrl)
 
    # 取的 Sheet 資料
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values',[])
 
    return values
 
 
if __name__ == '__main__':
    spreadsheetId = '12gUhV2vRseS37F2pzVsY1ujepIQEJh0CnOW6wyhFkx0'
    rangeName = 'sheet1!A1:E'
    values = getSheetValue(spreadsheetId,rangeName)
 
    if not values:
        print('No data found.')
    else:
        for row in values:
            # Print columns A and E, which correspond to indices 0 to 4.
            print('%s, %s, %s, %s, %s' % (row[0], row[1], row[2], row[3], row[4]))