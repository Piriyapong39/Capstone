import gspread
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

key = os.getenv("key")

myscope = ['https://spreadsheets.google.com/feeds', 
                'https://www.googleapis.com/auth/drive']
mycred = ServiceAccountCredentials.from_json_keyfile_dict(key,myscope)
client = gspread.authorize(mycred)
sheet = client.open("esp32data")
worksheet = sheet.get_worksheet(0)
all_records = worksheet.get_all_records()
latest_data = all_records[-1]
client = MongoClient(os.getenv("MONGODB_URL"))
db = client.weather
collection = db.data
collection.insert_one(latest_data)
