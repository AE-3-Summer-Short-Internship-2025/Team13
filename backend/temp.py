import requests
import pandas as pd

REQUEST_URL = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601'
APP_ID = '1009667447566505226'

#必要なパラメータを辞書型で定義
params = {
    'applicationId': APP_ID,
    'format':'json',
    'keyword':'モバイルバッテリー',
    'minPrice':10000
}

res = requests.get(REQUEST_URL,params)

res.status_code

result = res.json()

Items = result['Items']

len(Items)

pd.DataFrame(Items)[:3]

items = [item['Item'] for item in Items]

items[0]

df = pd.DataFrame(items)
df[:3]

#カラムを表示
df.columns

columns = ['itemName', 'itemPrice', 'affiliateRate', 'catchcopy', 'itemCaption', 'itemCode', 'itemUrl', 'reviewAverage', 'reviewCount','shopCode', 'shopName', 'shopUrl']

df = df[columns]