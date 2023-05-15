import grpc
import atm_pb2
import atm_pb2_grpc
import pymongo
import time
from concurrent import futures
import logging
from grpc.experimental import aio
import asyncio
import datetime

# 取得MongoDB Atlas的連線字串
# cloud database
# uri = "mongodb+srv://tanlikfeng:0983739382@cluster1.hgwyjvc.mongodb.net/?retryWrites=true&w=majority"

# local database
uri = "mongodb://localhost:27017/"

class BankService(atm_pb2_grpc.BankServiceServicer):

    def __init__(self):
        # 連接MongoDB Atlas
        client = pymongo.MongoClient(uri)
        db = client["mydatabase"]
        self.accounts = db["accounts"]

    async def Transfer(self, request, context: grpc.aio.ServicerContext):
        print(datetime.datetime.now()) 
        # print(request)
        # 檢查轉出帳戶是否存在
        from_account = self.accounts.find_one({"_id": request.from_account_id})
        if not from_account:
            return atm_pb2.TransferResponse(success=False, message=f"{request.amount}")

        # 檢查轉入帳戶是否存在
        to_account = self.accounts.find_one({"_id": request.to_account_id})
        if not to_account:
            return atm_pb2.TransferResponse(success=False, message=f"{request.amount}")

        # 檢查轉出金額是否足夠
        if from_account["balance"] < request.amount:
            return atm_pb2.TransferResponse(success=False, message=f"{request.amount}")

        # 更新帳戶餘額
        self.accounts.update_one({"_id": request.from_account_id}, {
                                 "$inc": {"balance": -request.amount}})
        self.accounts.update_one({"_id": request.to_account_id}, {
                                 "$inc": {"balance": request.amount}})

        return atm_pb2.TransferResponse(success=True, message=f"{request.amount}")


async def serve():
    # 建立gRPC服務器
    # server = aio.server(futures.ThreadPoolExecutor(max_workers=10))
    server = aio.server()

    # 註冊服務
    atm_pb2_grpc.add_BankServiceServicer_to_server(BankService(), server)

    # 監聽50051埠
    server.add_insecure_port("[::]:50051")

    # 啟動服務器
    await server.start()
    print("Server started on port 50051")

    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
