
import http
import json
import requests
import simplejson
import urllib3
#api_keys for your etherscan key
from setting import api_kyes

'''
0x074eba014c09d577ef1d83652ae6506217ec3078
https://etherscan.io/tx/0xca798e649219b222b6e66fa7d443a64ddfaa7214585f64c59ef273151215fc8d
'''

def load_address_info(file_name):
    """

    :param file_name:
    :return: {'hash',['address']}
    """
    address_info = {}
    tmp_address_lists = []

    with open(file_name) as f:
        for line in f.readlines():
            line = line.strip("\n")
            line = line.strip("")
            if line[0:4] == "http" and line[0:4] !="noau" and len(line)>=90:
                ts_hash = line[-66:]
                address_info[ts_hash] = tmp_address_lists
                print(f"Add{ts_hash} to Key ")
                #重置list
                tmp_address_lists = []
                #判断是否为地址
            elif line[0:2] == "0x":
                address = line
                tmp_address_lists.append(address)
                print(f"Add:{address} To List.")
                #noau -> 不是自动化生成的，不需要检测内部交易哈希地址
            else:
                print(f"{line} 不是地址，不添加")

    # print(address_info)
    return address_info


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
            print("History 0")
            print(res)
            return None
    except requests.exceptions.ProxyError:
        print("ProxyError")
        return None
    except http.client.IncompleteRead:
        print("IncompleteRead")
        return None
    except http.client.RemoteDisconnected:
        print("RemoteDisconnected")
        return None
    except urllib3.exceptions.MaxRetryError:
        print("MaxRetryError")
        return None
    except requests.exceptions.SSLError:
        print("SSLError")
        return None


def get_airdrop_number(address):
    """

    :param address:
    :return: airdrop_numbers
    """
    urls = f"https://airdrop-api.hop.exchange/v1/airdrop/{address}"
    try:
        res = requests.get(urls)
        if res.status_code != 200:
            return None
        data = res.json()
        # print(data['data'])
        if 'totalTokens'  in data['data']:
            return float(data['data']['totalTokens']) / 10 ** 18
        else:
            return None
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
    file_name = "3-address_hash_info.txt"
    address_info_dicts = load_address_info(file_name)
    airdrop_sum = 0
    address_count = 0
    for ts_hash in address_info_dicts:
        for address in address_info_dicts[ts_hash]:
            airdrop_num = get_airdrop_number(address)
            if airdrop_num == None:
                address_info_dicts[ts_hash].remove(address)
                print(f"{address} Invalid ")
                continue
            print(f"{address}:{airdrop_num}")
            save_name = "validation_address-part1.txt"
            with open(save_name, 'a') as f:
                print(f"{address} WriteFile{save_name}")
                f.writelines(f"{address}\n")
            airdrop_sum = airdrop_num + airdrop_sum
            address_count = address_count + 1
        with open(save_name, 'a') as f:
            f.writelines(f"{ts_hash}\n")
            print(f"ts_Hash{ts_hash}")
    print(f"AddressCount：{address_count} AirdropSum：{airdrop_sum}")




if __name__ == '__main__':
    main()
