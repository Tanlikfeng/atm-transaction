import asyncio
import grpc
import atm_pb2
import atm_pb2_grpc
import datetime
import logging

from concurrent import futures
from pymongo import MongoClient


class BankService(atm_pb2_grpc.BankServiceServicer):
    def __init__(self):
        self.client_A = MongoClient("mongodb://localhost:27017")
        self.client_B = MongoClient("mongodb://localhost:27019")

        self.db_A = self.client_A["bank_A"]
        self.accounts_A = self.db_A["accounts"]

        self.db_B = self.client_B["bank_B"]
        self.accounts_B = self.db_B["accounts"]

    async def Transfer(self, request, context):
        print(datetime.datetime.now())
        print(request)

        from_id = request.from_account_id
        to_id = request.to_account_id
        amount = request.amount

        # check id whether exist or not
        from_id_exists = self.accounts_A.find_one({"_id": from_id}) is not None
        to_id_exists = self.accounts_B.find_one({"_id": to_id}) is not None

        if not from_id_exists or not to_id_exists:
            return atm_pb2.TransferResponse(success=False, message="Invalid account")

        from_account = self.accounts_A.find_one({"_id": from_id})
        from_balance = from_account["balance"]

        # check balance
        if from_balance < amount:
            return atm_pb2.TransferResponse(success=False, message="Transaction failed")

        # to_account = self.collection.find_one({'_id': to_id})

        # do transaction
        self.accounts_A.update_one({"_id": from_id}, {"$inc": {"balance": -amount}})
        self.accounts_B.update_one({"_id": to_id}, {"$inc": {"balance": amount}})

        response = atm_pb2.TransferResponse(
            success=True, message="Transfer succcessful"
        )

        return response


async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    atm_pb2_grpc.add_BankServiceServicer_to_server(BankService(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    logging.info("Server started on port 50051")
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
