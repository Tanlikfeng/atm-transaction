import asyncio
import grpc
import atm_pb2
import atm_pb2_grpc
import datetime

from concurrent import futures
from pymongo import MongoClient

class BankService(atm_pb2_grpc.BankServiceServicer):
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client['bank_B']
        self.accounts = self.db['accounts']

    async def Transfer(self, request, context):
        print(datetime.datetime.now())
        print(request)
        
        from_id = request.from_account_id
        to_id = request.to_account_id
        amount = request.amount
        
        from_id_exists = self.accounts.find_one({'_id': from_id}) is not None
        to_id_exists = self.accounts.find_one({'_id': to_id}) is not None

        if not from_id_exists or not to_id_exists:
            return atm_pb2.TransferResponse(success=False, message='Invalid account')
        
        from_account = self.accounts.find_one({'_id': from_id})
        from_balance = from_account['balance']

        if from_balance < amount:
            return atm_pb2.TransferResponse(success=False, message='Transaction failed')
        
        # to_account = self.collection.find_one({'_id': to_id})
        
        self.accounts.update_one({'_id': from_id}, {'$inc': {'balance': -amount}})
        self.accounts.update_one({'_id': to_id}, {'$inc': {'balance': amount}})
        
        response = atm_pb2.TransferResponse(success=True, message='Transfer succcessful')
        
        return response

async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    atm_pb2_grpc.add_BankServiceServicer_to_server(BankService(), server)
    server.add_insecure_port('[::]:50052')
    await server.start()
    print("Server started on port 50052")
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())
