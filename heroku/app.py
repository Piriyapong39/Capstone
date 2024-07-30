from flask import Flask, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os


load_dotenv()
MONGODB_DATABASE = os.getenv("MONGO_URL")
app = Flask(__name__)
client = MongoClient(MONGODB_DATABASE)
db = client.weather

@app.route("/", methods=["GET"])
def dataforesp():
    collection = db.data
    lastest_data = collection.find_one({}, {"Temperature": 1,"Humidity": 1,"Status": 1, "HumidityADJ": 1, "_id": 0}, sort=[('_id', -1)])
    return jsonify(lastest_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
