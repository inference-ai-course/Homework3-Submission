import requests
import sys
import configparser


config = configparser.ConfigParser()
config.read('config.ini')
url = config['server']['url']

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <round> (where round is an integer of value 1, 2, 3, 4, or 5)")
else:
    round = sys.argv[1]
    file = {'file': open(f'input/input{round}.m4a', 'rb')}
    resp = requests.post(url=url, files=file) 
    print('done')
    file_path = f'result{round}.mp3'
    with open(file_path, 'wb') as f:
        f.write(resp.content)