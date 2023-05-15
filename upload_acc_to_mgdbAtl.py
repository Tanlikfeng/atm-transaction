import pymongo
import json

# 載入JSON檔案
with open('accounts.json', 'r') as f:
    data = json.load(f)

# 取得MongoDB Atlas的連線字串
# 請將下面的 <username>, <password>, <cluster-name> 和 <database-name> 替換成你的資料庫相對應的值
# cloud database
# uri = "mongodb+srv://tanlikfeng:0983739382@cluster1.hgwyjvc.mongodb.net/?retryWrites=true&w=majority"
# local database
uri = "mongodb://localhost:27017/"

# 建立MongoDB的客戶端
client = pymongo.MongoClient(uri)

# 取得要存取的資料庫和集合
db = client['mydatabase']
collection = db['accounts']

# 删除全部账户
output = collection.delete_many({})
print(output.deleted_count, " documents deleted.")

# 將每個帳戶插入到集合中
for account in data['accounts']:
    collection.insert_one(account)

# 關閉MongoDB客戶端
client.close()
