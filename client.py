import grpc
import atm_pb2
import atm_pb2_grpc
import pymongo
import random
import json
import time
import logging
import datetime
import asyncio

# 建立與gRPC服務器的通道
# channel = grpc.insecure_channel('localhost:50051')

# 建立gRPC客戶端
# stub = atm_pb2_grpc.BankServiceStub(channel)

count = 0


async def trans(item, start):
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = atm_pb2_grpc.BankServiceStub(channel)

        # 将JSON数据转换为protobuf消息对象
        request = atm_pb2.TransferRequest()
        # print(request)

        request.from_account_id = item['from_account_id']
        request.to_account_id = item['to_account_id']
        request.amount = count

        response = await stub.Transfer(request)
        # future = stub.Transfer.future(request)
        # response = future
        # await asyncio.sleep(5)
        # feature = response.result()
        print(response)
        # if feature.success:
        #     print('success')
        #     print(datetime.datetime.now() - start)
        #     # count += 1
        # else:
        #     print('Unsuccess')
        #     print(datetime.datetime.now() - start)
        #     # count += 1

        if response.success:
            print('Success')
            print(datetime.datetime.now() - start)
        else:
            print('Unsuccess')
            print(datetime.datetime.now() - start)


async def run(data):
    # for i in range(0, len(data), 5):
    start = datetime.datetime.now()
    asyncio.run(trans(data, start))
    end = datetime.datetime.now()
    # print(count / (end - start).microseconds)


if __name__ == '__main__':
    logging.basicConfig()

    # 讀取交易紀錄 JSON 文件
    with open("transactions.json", "r") as f:
        transactions = json.load(f)

    # print(type(transactions))

    # 把交易记录 JSON 文件传到 run function
    start = datetime.datetime.now()
    for json_data in transactions:
        asyncio.run(trans(json_data, datetime.datetime.now()))
        count += 1
    #     # break
    asyncio.run(run(transactions))
    print(datetime.datetime.now() - start)
