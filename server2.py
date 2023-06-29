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
        # await asyncio.sleep(1)

        from_id = request.from_account_id
        to_id = request.to_account_id
        amount = request.amount

        logging.info(f"Received request from client: {from_id, to_id, amount}")

        from_account = self.accounts_A.find_one_and_update(
            {"_id": from_id, "balance": {"$gte": amount}},
            {"$inc": {"balance": -amount}},
        )
        to_account = self.accounts_B.find_one_and_update(
            {"_id": to_id}, {"$inc": {"balance": amount}}
        )

        if not from_account or not to_account:
            return atm_pb2.TransferResponse(success=False, message="Invalid account")

        return atm_pb2.TransferResponse(success=True, message="Transfer successful")


async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    atm_pb2_grpc.add_BankServiceServicer_to_server(BankService(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    logging.info("Server started on port 50051")
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="server2.log", filemode="w")
    asyncio.run(serve())
