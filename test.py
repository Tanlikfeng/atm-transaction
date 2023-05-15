import grpc
import atm_pb2
import atm_pb2_grpc
import pymongo
import random
import json
import time
import logging
import datetime

def run(data):
    # 建立與gRPC服務器的通道
    channel = grpc.insecure_channel('localhost:50051')

    # 建立gRPC客戶端
    stub = atm_pb2_grpc.BankServiceStub(channel)

    count = 0
    start = datetime.datetime.now()

    for i in range(0, len(data), 500):
        batch = transactions[i:i+500]
        requests = []
        print(type(requests))
        for item in batch:
            # print(type(item))
            request = atm_pb2.TransferRequest(
                from_account_id=item['from_account_id'],
                to_account_id=item['to_account_id'],
                amount=item['amount']
            )
            requests.append(request)
        
        futures = []
        for request in requests:
            future = stub.Transfer.future(request)
            futures.append(future)
        
        for future in futures:
            response = future.result()
            if response.success:
                count += 1
            else:
                print('Transaction failed: ', response.error)
        
        end = datetime.datetime.now()
        if (end - start).total_seconds() >= 1:
            print('Transactions processed in 1 second: ', count)
            break
    
    channel.close()


if __name__ == '__main__':
    logging.basicConfig()

    # 讀取交易紀錄 JSON 文件
    with open("transactions.json", "r") as f:
        transactions = json.load(f)

    # print(transactions)
    
    # 把交易记录 JSON 文件传到 run function
    for json_data in transactions:
        print(type(json_data))
        run(json_data)
        # count+=1
        # break

    
