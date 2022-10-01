import discord
import gspread
import datetime

# 必要モジュールのインポート
import os
from dotenv import load_dotenv

# .envファイルの内容を読み込見込む
load_dotenv()


from oauth2client.service_account import ServiceAccountCredentials
credentials_json = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
TOKEN = os.environ['TOKEN']
SPREADSHEET_KEY = os.environ['SPREADSHEET_KEY']

client = discord.Client(intents=discord.Intents.all())

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('GOOGLE_APPLICATION_CREDENTIALS', scope)

gc = gspread.authorize(credentials)
workbook = gc.open_by_key(SPREADSHEET_KEY)

def monthcheck():
    worksheet_list = workbook.worksheets()              #ワークシートの一覧を取得
    today = datetime.date.today().strftime('%Y%m')    #今日の日付を取得し文字列の形で記録する
    exist = False
    for current in worksheet_list :
        if current.title == today :
            exist = True                                #今月の分のシートがあればフラグを立てる
    if exist == False :                                 #今月の分のシートがなければここで作成する
         workbook.add_worksheet(title=today, rows = 100, cols = 4)      #余裕を持って行数は100行、幅は4行のシートを新規作成する
         newsheet = workbook.worksheet(today)           #作成したシートの初期値を設定する
         newsheet.update('A1','収入')
         newsheet.update('C1','支出')
    return workbook.worksheet(today)                #作成したシートを戻り値として返す。

def add_income(worksheet, name, amount):#引数で受け取ったシートに引数で受け取った収入を記録する関数
    lists = worksheet.get_all_values()  #シートの内容を配列で取得
    rows = len(lists) + 1               #入力されているデータの数を取得し、末端に書き込むときのインデックスとして利用する為+1する
    worksheet.update_cell(rows,1,name)  #引数で受け取った名前をセルに入力
    worksheet.update_cell(rows,2,amount)#引数で受け取った金額をセルに入力
    
def add_spending(worksheet, name, amount):#引数で受け取ったシートに引数で受け取った支出を記録する関数
    lists = worksheet.get_all_values()  #シートの内容を配列で取得
    rows = len(lists) + 1               #入力されているデータの数を取得し、末端に書き込むときのインデックスとして利用する為+1する
    worksheet.update_cell(rows,3,name)  #引数で受け取った名前をセルに入力
    worksheet.update_cell(rows,4,amount)#引数で受け取った金額をセルに入力
