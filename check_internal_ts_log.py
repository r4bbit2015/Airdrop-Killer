
import http
import json
import logging
import sys

import requests
import simplejson
import urllib3

#etherscan key
from setting import api_kyes


def read_address(file_name):
    data = []
    with open(file_name) as f:
        for line in f.readlines():
            line = line.replace('\n',"")
            data.append(line.replace("\t",""))
    return data


def check_interl_hash(hash):
    try:
        urls = f"https://api.etherscan.io/api?module=account&action=txlistinternal&txhash={hash}&apikey={api_kyes}"
        res = requests.get(urls)
        if res.status_code != 200:
            None
        res = json.loads(res.text)
        if res["status"] == "1":
            return res
        else:
            logging.error("History 0")
            logging.debug(res)
            return None
    except requests.exceptions.ProxyError:
        logging.error("ProxyError")
        return None
    except http.client.IncompleteRead:
        return None
    except http.client.RemoteDisconnected:
        return None
    except requests.exceptions.ProxyError:
        return None
    except urllib3.exceptions.MaxRetryError:
        logging.error("MaxRetryError")
        return None
    except requests.exceptions.SSLError:
        logging.error("SSLError")
        return None


def get_hash_address_lists(hash):
    to_address = []
    ts_hash = check_interl_hash(hash)['result']
    if ts_hash == None:
        print("get address error")
        return None
    for address in ts_hash:
        print(f"Hash内地址:{address['to']}")
        to_address.append(address['to'])
    return  to_address


def is_airdrop_address(address):
    urls = f"https://airdrop-api.hop.exchange/v1/airdrop/{address}"
    try:
        res = requests.get(urls)
        if res.status_code != 200:
            return None
        data = res.json()
        if 'totalTokens' not in data['data']:
            return False
        else:
            return True
    except simplejson.errors.JSONDecodeError:
        return None
    except json.decoder.JSONDecodeError:
        return None
    except http.client.RemoteDisconnected:
        return None
    except requests.exceptions.ProxyError:
        return None
    except urllib3.exceptions.MaxRetryError:
        return None
    except requests.exceptions.SSLError:
        return None

def main():
    file_name = sys.argv[1]
    save_name = sys.argv[2]
    print(f"ReadFileName:{file_name} SaveFileName{save_name}")
    address_hash_str = read_address(file_name)
    address_hash_dict = {}
    for add in address_hash_str:
        address = add[0:42]
        hash = add[42:]
        if address in address_hash_dict:
            address_hash_dict[address].append(hash)
        else:
            address_hash_dict[address] = [hash]

    print(address_hash_dict)
    count = 1
    for key in address_hash_dict:
        for tx_hash in address_hash_dict[key]:
            tx_hash = tx_hash.strip()
            print(f"[{count}] {key} Hash:{tx_hash}")
            hash_address_lists = get_hash_address_lists(tx_hash)
            if hash_address_lists == None:
                continue
            for address in hash_address_lists:
                if is_airdrop_address(address):
                    with open(save_name, 'a') as f:
                        f.writelines(f"{address}\n")
                        print(f"[{count}]{address}")
                else:
                    print(f"[{count}]{address}")
            with open(save_name, 'a') as f:
                f.writelines(f"{tx_hash}\n")
            count = count + 1


if __name__ == '__main__':
    main()
