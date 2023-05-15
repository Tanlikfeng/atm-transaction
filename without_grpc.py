import pymongo
from pymongo import MongoClient
import time
import json

uri = "mongodb+srv://tanlikfeng:0983739382@cluster1.hgwyjvc.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(uri)
db = client["mydatabase"]
accounts = db["accounts"]

if __name__ == "__main__":

    # 讀取交易紀錄 JSON 文件
    with open("transactions.json", "r") as f:
        transactions = json.load(f)

    start = time.time()

    # 把交易记录 JSON 文件传到 run function
    for json_data in transactions:
        
        # json文件的id
        from_id = json_data['from_account_id']
        # 从db里找看有没有和json文件的id一样的
        from_result = accounts.find_one({"_id": from_id})
        if from_result is None:
            print(f'Invalid from account: {from_id}')
            continue
        
        # json文件的id
        to_id = json_data['to_account_id']
        # 从db里找看有没有和json文件的id一样的
        to_result = accounts.find_one({"_id": to_id})
        if to_result is None:
            print(f'Invalid to account: {to_id}')
        
        # 如果from_id的balance >= amount
        json_amount = json_data['amount']
        db_balance = from_result.get("balance")
        print("json: ",json_amount)
        print("db: ",db_balance)
        if db_balance >= json_amount:
            accounts.update_one({"_id": from_id}, {"$inc": {"balance": -json_amount}})
            accounts.update_one({"_id": to_id}, {"$inc": {"balance": json_amount}})
        else:
            print(f"Insufficient balance.")

    end = time.time()

    duration = end - start

    print(duration)
