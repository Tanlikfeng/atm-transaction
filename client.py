import asyncio
import grpc
import json
import time
import atm_pb2
import atm_pb2_grpc
import logging


async def send_transactions(stub_A, stub_B):
    with open("transactions.json") as f:
        transactions = json.load(f)

    total_transactions = len(transactions)
    batch_size = 1000  # 每批发送的交易数量
    batch = []
    # count = 0

    start_time = time.time()
    for i in range(0, total_transactions, batch_size):
        batch = transactions[i : i + batch_size]
        requests = []

        for transaction in batch:
            from_id = transaction["from_account_id"]
            to_id = transaction["to_account_id"]
            amount = transaction["amount"]

            request = atm_pb2.TransferRequest(
                from_account_id=from_id, to_account_id=to_id, amount=amount
            )
            requests.append(request)

        # python asyncio.gather是可以同時放入多個 coroutine
        # "*"將每一個coroutine object傳給asyncio.gather()
        responses_A = await asyncio.gather(
            *[stub_A.Transfer(request) for request in requests]
        )
        logging.info(f"Received response from server response_A: {responses_A}")

        # 統計成功執行的requests數量
        # count += len(responses_A)

        # responses_B = await asyncio.gather(
        #     *[stub_B.Transfer(request) for request in requests]
        # )
        # logging.info(f"Received response from server response_B: {responses_B}")
        # count += len(responses_B)

        # print(i)

    t = time.time() - start_time
    print(t)


async def main():
    channel_A = grpc.aio.insecure_channel("localhost:50051")
    stub_A = atm_pb2_grpc.BankServiceStub(channel_A)

    channel_B = grpc.aio.insecure_channel("localhost:50051")
    stub_B = atm_pb2_grpc.BankServiceStub(channel_B)

    await send_transactions(stub_A, stub_B)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="client.log", filemode="w")
    asyncio.run(main())
