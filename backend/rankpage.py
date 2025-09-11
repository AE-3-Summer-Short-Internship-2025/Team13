import requests
import json
import time

# ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼

# 検索キーワード
SEARCH_KEYWORD = '防災'

def fetch_rakuten_products(keyword, sort_key):
    """
    指定されたキーワードとソート順で楽天の商品を検索し、辞書のリストとして返す関数
    """
    # 自身の楽天アプリIDに書き換えてください
    APP_ID = '1088027222225008171' 
# ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲

    # 20220601バージョンを使用
    SEARCH_URL = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601'
    params = {
        'applicationId': APP_ID,
        'format': 'json',
        'keyword': keyword,
        'sort': sort_key,
        'hits': 10
    }
    try:
        res = requests.get(SEARCH_URL, params=params)
        res.raise_for_status() # HTTPエラーが発生した際に例外を発生させる
        result = res.json()
        
        if not result.get('Items'):
            print(f"「{keyword}」に関する商品が見つかりませんでした。(ソート: {sort_key})")
            return None
            
        # pandasを使わずに必要な情報だけを抽出し、日本語キーを持つ辞書のリストを作成
        items_data = []
        for item in result['Items']:
            item_info = item['Item']
            items_data.append({
                '商品名': item_info.get('itemName'), 
                '価格': item_info.get('itemPrice'), 
                'ショップ名': item_info.get('shopName'), 
                '評価点': item_info.get('reviewAverage')
            })
        return items_data

    except requests.exceptions.RequestException as e:
        # エラーの詳細（JSONレスポンス）を表示するように改良
        error_details = ""
        try:
            error_details = e.response.json()
        except (ValueError, AttributeError):
            pass # JSONデコードに失敗した場合は何もしない
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
        f"【{SEARCH_KEYWORD}】新着商品（更新日時順） TOP10": "-updateTimestamp",
        f"【{SEARCH_KEYWORD}】評価順商品 TOP10": "-reviewAverage",
        f"【{SEARCH_KEYWORD}】価格が安い順 TOP10": "+itemPrice"
    }
    
    # 最終的なJSON出力を格納するための辞書
    final_output = {}

    for title, sort_param in lists_to_show.items():
        print(f"--- {title} を取得中 ---")
        
        products = fetch_rakuten_products(keyword=SEARCH_KEYWORD, sort_key=sort_param)
            
        if products is not None:
            # 新着順と価格順の場合は「評価点」キーを削除
            if sort_param in ["-updateTimestamp", "+itemPrice"]:
                for p in products:
                    if '評価点' in p:
                        del p['評価点']
            
            # 最終出力用の辞書に結果を格納
            final_output[title] = products
        else:
            final_output[title] = [] # 商品が取得できなかった場合は空のリストを格納
        
        # 楽天APIへの負荷を考慮し、1秒間待機
        time.sleep(1)

    # 全てのリストを取得した後、整形されたJSON形式で標準出力に表示
    print("\n" + "="*60)
    print("すべての結果をJSON形式で出力します。")
    print("="*60 + "\n")
    print(json.dumps(final_output, indent=2, ensure_ascii=False))
