import json

accounts = []
for i in range(1, 100001):
    item = {
        "id": i,
        "balance": 1000
    }
    accounts.append(item)
    
data = {"accounts": accounts}

with open("accounts.json", "w") as f:
    json.dump(data, f)
