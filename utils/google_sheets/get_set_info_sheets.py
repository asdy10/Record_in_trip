import httplib2
import googleapiclient
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from data.config import GOOGLE_API, TABLE_ID


def update_table(arr, ranges):
    # ranges = 'Действие!A1:AS10000'
    serv_acc = ServiceAccountCredentials.from_json_keyfile_name(
        GOOGLE_API,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = serv_acc.authorize(httplib2.Http())
    table_connect = googleapiclient.discovery.build('sheets', 'v4', http=httpAuth, cache_discovery=False)

    r = table_connect.spreadsheets().values().batchUpdate(
        spreadsheetId=TABLE_ID,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": ranges,
                 "values": arr},
            ]}
    ).execute()


def paint_table(listname, pos):
    serv_acc = ServiceAccountCredentials.from_json_keyfile_name(
        GOOGLE_API,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = serv_acc.authorize(httplib2.Http())
    table_connect = googleapiclient.discovery.build('sheets', 'v4', http=httpAuth, cache_discovery=False)
    batch_update_spreadsheet_request_body = {
        "requests":
            [
                {
                    "repeatCell":
                        {
                            "cell":
                                {
                                    "userEnteredFormat":
                                        {
                                            # "horizontalAlignment": 'CENTER',
                                            "backgroundColor": {
                                                "red": 0,
                                                "green": 1,
                                                "blue": 1,
                                                #"alpha": 1
                                            },
                                            "textFormat":
                                                {

                                                    "fontSize": 12,
                                                    "fontFamily": 'Times New Roman'

                                                }
                                        }
                                },
                            "range":
                                {
                                    "sheetId": listname,
                                    "startRowIndex": pos-1,
                                    "endRowIndex": pos,
                                    "startColumnIndex": 1,
                                    "endColumnIndex": 2
                                },
                            "fields": "userEnteredFormat"
                        }
                }
            ]
    }

    request = table_connect.spreadsheets().batchUpdate(spreadsheetId=TABLE_ID, body=batch_update_spreadsheet_request_body)
    response = request.execute()
    print(response)


def clear_table(ranges):
    # ranges = 'Действие!A1:AS10000'
    serv_acc = ServiceAccountCredentials.from_json_keyfile_name(
        GOOGLE_API,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = serv_acc.authorize(httplib2.Http())
    table_connect = googleapiclient.discovery.build('sheets', 'v4', http=httpAuth, cache_discovery=False)

    table_connect.spreadsheets().values().clear(spreadsheetId=TABLE_ID, range=ranges, body={}).execute()


def get_table(ranges):
    # ranges = 'Действие!A1:AS10000'
    serv_acc = ServiceAccountCredentials.from_json_keyfile_name(
        GOOGLE_API,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = serv_acc.authorize(httplib2.Http())
    table_connect = googleapiclient.discovery.build('sheets', 'v4', http=httpAuth, cache_discovery=False)
    iiiiiiii = table_connect.spreadsheets().values().batchGet(spreadsheetId=TABLE_ID, ranges=ranges,
                                                              valueRenderOption='FORMATTED_VALUE',
                                                              dateTimeRenderOption='FORMATTED_STRING').execute()
    result = iiiiiiii['valueRanges'][0]['values']

    # iiiiiiii = table_connect.spreadsheets().get(spreadsheetId=TABLE_ID, ranges=ranges,
    #
    #                                             includeGridData=True).execute()
    # # result = iiiiiiii['valueRanges'][0]['values']
    # res = iiiiiiii['sheets'][0]['data'][0]['rowData']
    # for i in res:
    #     print(i)
    #     #{'backgroundColor': {'green': 1, 'blue': 1}
    # #print(iiiiiiii)
    return result
