# atm-transaction

- 問題

  - client.py: 有兩個 stub (stub_A,stub_B), 其實是不是用一個 stub 就好了? 因爲我發現如果有兩個 stub 他會重複執行 transaction?
  - server.py: Transfer function 裏面有一個 await asyncio.sleep(1), 它不會影響執行時間嗎? 我有問 chatgpt 他説不會影響執行時間但是我實際去執行發現好像執行時間會變更久一些?
  - 我要怎樣測 server 是一次處理完才傳回去給 client, 還是做一筆傳一筆?
  - client & server 的 print 我都換成輸出到 log file, 好像會降低執行時間.

- compile time (client 傳 10 萬筆到 server):

  - TPS = transaction 數量 / 執行時間

  - server 直接 return 并沒有沒有經過 database

    - sleep: 41 秒, tps: 2402
    - no sleep: 40 秒, tps: 2454

  - server2.py: find and update together

    - sleep: 126 秒, tps: 790
    - no sleep: 114 秒, tps: 693

  - server.py: seperate find and update
    - sleep: 274 秒, tps: 364
    - no sleep: 224 秒, tps: 445
  - request and response message, insert into log file (559.2175543308258 秒)
