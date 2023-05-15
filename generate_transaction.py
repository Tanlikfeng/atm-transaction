import random
import json

# 產生20筆交易紀錄
transactions = []
for i in range(100000):
    # 隨機選擇兩個帳戶
    account_ids = random.sample(range(1, 100001), 2)
    from_account_id = account_ids[0]
    to_account_id = account_ids[1]

    # 隨機產生交易金額
    # amount = round(random.randrange(100, 1000), 2)
    amount = 100

    # 加入交易紀錄
    transaction = {
        "from_account_id": from_account_id,
        "to_account_id": to_account_id,
        "amount": amount
    }
    transactions.append(transaction)

# 將交易紀錄存到JSON檔案中
with open('transactions.json', 'w') as f:
    json.dump(transactions, f)
