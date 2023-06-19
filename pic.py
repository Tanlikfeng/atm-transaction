import matplotlib.pyplot as plt
from tabulate import tabulate

batch = [100, 300, 500, 1000, 5000, 10000, 50000, 100000]
tps = [
    306.32038105813,
    329.95226577107235,
    252.3368033389866,
    190.05888151121462,
    366.8349032042665,
    424.7093396014025,
    425.32260543847406,
    430.54957395244304,
]

plt.plot(batch, tps, marker="o")
# plt.bar(batch, tps)
plt.xlabel("Transaction per Second")
plt.ylabel("Batch")
plt.title("execution time")
# plt.grid(True)
plt.show()

# data = zip(batch, tps)
# table = tabulate(
#     data, headers=["Batch Size", "Transactions Per Second"], tablefmt="fancy_grid"
# )
# print(table)
