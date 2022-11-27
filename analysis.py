import pandas as pd
import numpy as np
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import reddit
from datetime import date
import datetime

limit = 30

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'market_cap_min':'0',
  'market_cap_max': '30000000',
  'limit':'5000'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '-6acc-4e81-8051-e2aa57f25161',
}



session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

for x in data["data"]:
  x["market_cap"] = x["quote"]["USD"]["market_cap"]
  x["volume"] = x["quote"]["USD"]["volume_24h"]

df_data = pd.DataFrame.from_dict(data["data"])

df_data = df_data[["id","name","symbol","cmc_rank","market_cap","date_added","volume"]]


df_data.date_added.fillna(value="2019-01-01", inplace=True)
date_list = df_data['date_added'].to_list()
now = datetime.datetime.now()
date_today = date(now.year,now.month,now.day)
days_passed_list = [  (date_today - date(int(x[0:4]),int(x[5:7]),int(x[8:10]) ) ).days for x in date_list]
df_data["days_passed"] = days_passed_list
df_data = df_data[df_data["days_passed"] <300]
df_data = df_data[df_data["market_cap"]>0]

df_data['id'] = df_data['id'].astype(int)
df_data['volume'] = df_data['volume'].astype(int)

df_data = df_data.sort_values(by=['volume'],ascending=False)

df_data.to_parquet(r'C:\Users\Hilmi\Desktop\Output\output.parquet')
df_data.to_excel(r'C:\Users\Hilmi\Desktop\Output\output.xlsx', index = False, header=True)

print("Finished")
