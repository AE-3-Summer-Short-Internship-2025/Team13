import requests
import pandas as pd
import time

# ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
APP_ID = '1088027222225008171' 
# ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲

# ご指定の通り、20220601バージョンを使用
SEARCH_URL = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601'

SEARCH_KEYWORD = '防災'

def fetch_rakuten_products(keyword, sort_key):
    """
    指定されたキーワードとソート順で楽天の商品を検索し、DataFrameとして返す関数
    """
    params = {
        'applicationId': APP_ID,
        'format': 'json',
        'keyword': keyword,
        'sort': sort_key,
        'hits': 10
    }
    try:
        res = requests.get(SEARCH_URL, params=params)
        res.raise_for_status()
        result = res.json()
        
        if not result.get('Items'):
            print(f"「{keyword}」に関する商品が見つかりませんでした。(ソート: {sort_key})")
            return None
            
        items_data = [item['Item'] for item in result['Items']]
        df = pd.DataFrame(items_data)
        
        columns_to_keep = {
            'itemName': '商品名', 
            'itemPrice': '価格', 
            'shopName': 'ショップ名', 
            'reviewAverage': '評価点'
        }
        
        exist_cols = [col for col in columns_to_keep.keys() if col in df.columns]
        return df[exist_cols].rename(columns=columns_to_keep)

    except requests.exceptions.RequestException as e:
        # エラーの詳細（JSONレスポンス）を表示するように改良
        error_details = ""
        try:
            error_details = e.response.json()
        except:
            pass
        print(f"通信エラーが発生しました (ソート: {sort_key}): {e}")
        if error_details:
            print(f"サーバーからのエラー詳細: {error_details}")
        return None

# --- メインの処理 ---
if __name__ == "__main__":
    print(f"キーワード「{SEARCH_KEYWORD}」の各種TOP10リストを取得します...\n")
    
    # 表示したいリストの種類を定義
    lists_to_show = {
        f"【{SEARCH_KEYWORD}】売れ筋商品 TOP10": "standard",
        # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓ 【修正点】 ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
        f"【{SEARCH_KEYWORD}】新着商品（更新日時順） TOP10": "-updateTimestamp",
        # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑ 【修正点】 ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
        f"【{SEARCH_KEYWORD}】評価順商品 TOP10": "-reviewAverage",
        f"【{SEARCH_KEYWORD}】価格が安い順 TOP10": "+itemPrice"
    }
    
    for title, sort_param in lists_to_show.items():
        print(f"--- {title} ---")
        
        df = fetch_rakuten_products(keyword=SEARCH_KEYWORD, sort_key=sort_param)
            
        if df is not None:
            df.index = df.index + 1
            
            # 「評価点」カラムが不要なリストを修正
            if sort_param in ["-updateTimestamp", "+itemPrice"] and "評価点" in df.columns:
                print(df.drop(columns=['評価点']).to_string())
            else:
                print(df.to_string())
        
        print("\n" + "="*60 + "\n")
        
        time.sleep(1)