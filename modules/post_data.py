"""Запостить в таблицу и сохранить логи"""

import datetime
from settings.settings import DOC_SHEET_ID
from google.oauth2 import service_account
from googleapiclient.discovery import build


def write_logg(string):
    with open('logs/log.log', 'a', encoding='utf-8') as file:
        file.write(string)


class Post_to_document:
    __SPREADSHEET_ID = DOC_SHEET_ID
    __SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    __SERVICE_ACCOUNT_FILE = 'settings/key.json'

    def __init__(self, body):
        self.__SPREADSHEET_ID = Post_to_document.__SPREADSHEET_ID
        self.__SCOPES = Post_to_document.__SCOPES
        self.__SERVICE_ACCOUNT_FILE = Post_to_document.__SERVICE_ACCOUNT_FILE
        self.body = body
        self.credentials = service_account.Credentials.from_service_account_file(
            self.__SERVICE_ACCOUNT_FILE, scopes=self.__SCOPES)
        self.service = build('sheets', 'v4', credentials=self.credentials)
        self.sheet = self.service.spreadsheets()
        self.timestamp = datetime.datetime.now()
        self.add_data()

    def add_data(self):
        try:
            response_main = self.service.spreadsheets().values().append(spreadsheetId=self.__SPREADSHEET_ID,
                                                                        range="B1",
                                                                        valueInputOption="USER_ENTERED",
                                                                        insertDataOption="OVERWRITE",
                                                                        body={"range": "B1",
                                                                              "values": self.body}).execute()

            if response_main['updates']['updatedRows'] == 1:
                write_logg(f'{self.timestamp} | Добавлена запись: {self.body[0][0:7] + self.body[0][12:]}' + '\n')
                return True
            else:
                write_logg(f'{self.timestamp} | Запись не добавлена: {self.body[0][0:7] + self.body[0][12:]}' + '\n')
                return False
        except Exception:
            write_logg(f'{self.timestamp} | Error in {__name__} | Запись не добавлена: {self.body[0][0:7] + self.body[0][12:]}' + '\n')
            return False
