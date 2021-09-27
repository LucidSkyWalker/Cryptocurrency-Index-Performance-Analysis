import requests 
from bs4 import BeautifulSoup
import json

# %% Create data from coinmarketcap.com
url = 'https://coinmarketcap.com/de/historical/20210926/' # This URL can be exchanged with the newest one. (can be found on https://coinmarketcap.com/de/historical/)
website = requests.get(url)
results = BeautifulSoup(website.content, 'html.parser')
script = results.find_all('script')[4]
result = '{\"cryptocurrency\"'+str(script).split('\"cryptocurrency\"')[1].split('\"rank\":200')[0] + '\"rank\":200}]}}}'
y = json.loads(result)
json.dump(y, open("2022.json",'w'))
