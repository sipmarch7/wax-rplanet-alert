import requests
import json
import time


print("The script is succesfully running , keep me on")
req_memo = "Win!!! New element has been opened."
ele = []

# txid = input("enter the txid: ")
# txid = '598659cd3e899476a00256a9a29e24d5054dddd848ac9626bac9ad43b95050e1'
def fetch_txid():
    url = 'https://api.waxsweden.org/v2/state/get_account?account=w.rplanet'
    response = requests.get(url)
    raw_data = json.loads(response.content)
    tx_id = raw_data['actions'][0]['trx_id']
    fetch_discovery(tx_id)

def fetch_discovery(txid):
    url = f'https://api.waxsweden.org/v2/history/get_transaction?id={txid}'

    response = requests.get(url)
    raw_data = json.loads(response.content)

    inventor_name = raw_data['actions'][0]['act']['data']['user']
    element_name  = raw_data['actions'][0]['act']['data']['str_symbol']
    memo = raw_data['actions'][1]['act']['data']['memo']
    print(1, memo)
    elements = raw_data['actions'][0]['act']['data']['elements']

    if memo == req_memo:
        print(f'Inventor is: {inventor_name}\nElement discovered is: {element_name}')
        for i in elements:
            ele.append(i[2:])
        print("the recipie is")
        print(ele)
        


    else:
        # print(f"{element_name} has already been discovered")
        pass

# fetch_txid()

while True:
    try:
        fetch_txid()
    except:
        pass
    time.sleep(5)