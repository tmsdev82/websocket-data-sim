import asyncio
import websockets
import threading
import time
import random
import json
from loguru import logger
from datetime import datetime

coins = ["btc", "eth", "doge", "ada", "xrp", "dot", "bch", "link", "ltc","xlm", "sol", "etc", "vet", "matic", "eos",
"theta", "trx", "neo", "xmr", "dai", "shib", "xtz", "klay", "mkr", "mota", "algo", "cake", "btt", "avax", "rune", "luna", "comp", "leo",
"tel", "chz", "dcr", "xem", "hot", "zec", "yfi", "waves", "cel", "enj", "sushi", "tfuel", "snx", "mana", "zil", "stx", "pax", "nexo",
"bat,", "near", "qtum", "btg", "rev", "omg", "nano", "ont", "dgb", "grt","one", "zrx", "bnt", "okb", "ftm", "rvn","celo","mdx",
"crv", "flow", "skl", "ren", "vgx", "iost", "ar", "lsk", "qnt", "rsr", "1inch", "xvg", "wrx", "dent", "rebtc", "ckb", "reef",
"snt", "btmx", "vtho", "xvs", "glm", "storj", "cfx", "gnosis", "celr", "oxt", "prom", "x", "y", "z", "xys", "test"]

exchanges = ["hitbtc", "binance", "coinbase", "kraken", "kucoin", "cex.io", "changelly", "coinmama"]

logger.debug(f"number of coins: {len(coins)}")

def gen_data():
    logger.info("Generating data...")
    time.sleep(0.1)
    start = time.time()

    data_set = []
    for exchange in exchanges:
        for coin_name in coins:
            random_val = random.randint(1, 1000)
            random_vol = random.randint(1, 1000)
            random_bid = random.randint(1, 1000)
            random_ask = random.randint(1, 1000)
            random_amount = random.randint(1, 1000)
            random_high = random.randint(1, 1000)
            random_low = random.randint(1, 1000)
            random_average_hourly_value = random.randint(1, 1000)
            update_datetime = datetime.utcnow()

            data = {
                "id": f"k_{exchange}_{coin_name}", 
                "name": coin_name, 
                "value": random_val, 
                "exchange": exchange,
                "volume": random_vol,
                "bid": random_bid,
                "ask": random_ask,
                "amount": random_amount,
                "high": random_high,
                "low": random_low,
                "average_hourly_value": random_average_hourly_value,
                "last_update": str(update_datetime)
            }

            data_set.append(data)
    delta = time.time() - start
    logger.debug(f"data generation took {delta:.06f} seconds.")
    return json.dumps(data_set)

async def send(client, data):
    await client.send(data)

async def handler(client, path):
    # Register.
    logger.info("Websocket Client Connected.", client)
    clients.append(client)
    while True:
        try:
            logger.debug("ping", client)
            pong_waiter = await client.ping()
            await pong_waiter
            logger.debug("pong", client)
            time.sleep(3)
        except Exception as e:
            clients.remove(client)
            logger.info("Websocket Client Disconnected", client)
            break

clients = []
start_server = websockets.serve(handler, "localhost", 5555)

asyncio.get_event_loop().run_until_complete(start_server)
mythread = threading.Thread(target = asyncio.get_event_loop().run_forever)
mythread.start()

logger.info("Socket Server Running. Starting main loop.")

while True:
    data = str(gen_data())
    message_clients = clients.copy()
    for client in message_clients:
        logger.info("Sending", data, "to", client)
        try:
            asyncio.run(send(client, data))
        except:
            # Clients might have disconnected during the messaging process,
            # just ignore that, they will have been removed already.
            pass

            