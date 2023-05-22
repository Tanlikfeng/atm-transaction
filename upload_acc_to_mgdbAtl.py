import pymongo
import json

# 載入JSON檔案
with open("accounts.json", "r") as f:
    data = json.load(f)

# 取得MongoDB Atlas的連線字串
# 請將下面的 <username>, <password>, <cluster-name> 和 <database-name> 替換成你的資料庫相對應的值
# cloud database
# uri = "mongodb+srv://tanlikfeng:0983739382@cluster1.hgwyjvc.mongodb.net/?retryWrites=true&w=majority"
# local database
uri_A = "mongodb://localhost:27017/"
uri_B = "mongodb://localhost:27019/"

# 建立MonAgoDB的客戶端
client_A = pymongo.MongoClient(uri_A)
client_B = pymongo.MongoClient(uri_B)

# 取得要存取的資料庫和集合
db_A = client_A["bank_A"]
collection_A = db_A["accounts"]

db_B = client_B["bank_B"]
collection_B = db_B["accounts"]

# 删除全部账户
output = collection_A.delete_many({})
print(output.deleted_count, " documents deleted.")

output = collection_B.delete_many({})
print(output.deleted_count, " documents deleted.")

# 將每個帳戶插入到集合中
for account in data["accounts"]:
    collection_A.insert_one(account)

for account in data["accounts"]:
    collection_B.insert_one(account)

# 關閉MongoDB客戶端
client_A.close()
client_B.close()
