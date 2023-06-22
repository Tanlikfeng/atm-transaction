import asyncio
import grpc
import json
import time
import atm_pb2
import atm_pb2_grpc


# async def send_transactions(stub_A, stub_B):
async def send_transactions(stub_A):
    with open("transactions.json") as f:
        transactions = json.load(f)

    total_transactions = len(transactions)
    batch_size = 100000  # 每批发送的交易数量
    batch = []

    start = time.time()
    for i in range(0, total_transactions, batch_size):
        if i != 0:
            time.sleep(1)
        batch = transactions[i : i + batch_size]
        requests = []

        # for i, transaction in enumerate(transactions, 1):
        for transaction in batch:
            from_id = transaction["from_account_id"]
            to_id = transaction["to_account_id"]
            amount = transaction["amount"]

            request = atm_pb2.TransferRequest(
                from_account_id=from_id, to_account_id=to_id, amount=amount
            )
            requests.append(request)

        responses_A = await asyncio.gather(
            *[stub_A.Transfer(request) for request in requests]
        )
        count += len(responses_A)

        # responses_B = await asyncio.gather(
        #     *[stub_B.Transfer(request) for request in requests]
        # )
        # logging.info(f"Received response from server response_B: {responses_B}")
        # count += len(responses_B)

        # print(i)

    end = time.time()
    print(end - start)
    print(batch_size)
    tps = batch_size / (end - start)
    print(tps)


async def main():
    channel_A = grpc.aio.insecure_channel("localhost:50051")
    stub_A = atm_pb2_grpc.BankServiceStub(channel_A)

    # channel_B = grpc.aio.insecure_channel("localhost:50051")
    # stub_B = atm_pb2_grpc.BankServiceStub(channel_B)

    # await send_transactions(stub_A, stub_B)
    await send_transactions(stub_A)


if __name__ == "__main__":
    asyncio.run(main())
