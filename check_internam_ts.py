
import http
import json
import logging
import sys
import time

import requests
import urllib3

# Your Etherscan ApiKey
from setting import api_kyes
''
multiSender_contract = ["0xcec8f07014d889442d7cf3b477b8f72f8179ea09","0xd152f549545093347a162dce210e7293f1452150"]
def get_all_address():
    urls = "https://raw.githubusercontent.com/hop-protocol/hop-airdrop/master/src/data/eligibleAddresses.txt?token=GHSAT0AAAAAABH3XLL7B2HXRO5VHMIYZURSYTUCDMQ"
    res = requests.get(urls)
    # print()
    address_lists = res.text.split('\n')
    # print(len(address_lists))
    #32806
    return address_lists

def get_internal_history(address):
    try:
        urls = f"https://api.etherscan.io/api?module=account&action=txlistinternal&address={address}&startblock=0&endblock=999999990&sort=asc&apikey={api_kyes}"
        res = requests.get(urls)
        res = json.loads(res.text)
        if res["status"] == "1":
            return res
        else:
            logging.error("History Zero")
            logging.debug(res)
            return None
    except requests.exceptions.ProxyError:
        logging.error("Proxy error")
        return None
    except http.client.IncompleteRead:
        return None
    except http.client.RemoteDisconnected:
        return None
    except requests.exceptions.ProxyError:
        return None
    except urllib3.exceptions.MaxRetryError:
        logging.error("Proxy Error ")
        return None
    except requests.exceptions.SSLError:
        logging.error("Max retries exceeded with url")
        return None

def main():
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    count = start
    print(f"Start:{start} End:{end}")
    address_lists = get_all_address()
    address_lists = address_lists[start:end]
    for address in address_lists:
        all_ts = get_internal_history(address)
        time.sleep(1)
        if all_ts == None:
            continue
        for ts in all_ts['result']:
            from_addr = ts['from']
            to_addr = ts['to']
            for contract in  multiSender_contract:
                if from_addr == contract or to_addr == contract:
                    print(f" {address} Hash:{ts['hash']}")
                    # with open("internal_ts.txt", 'a') as f:
                    with open(f"internal_ts-{start}-{end}.txt", 'a') as f:
                        f.writelines(f"{address}     {ts['hash']}"+ "\n")
                    continue
        print(f"[{count}] Address:{address}")
        count = count + 1

if __name__ == '__main__':
    main()
