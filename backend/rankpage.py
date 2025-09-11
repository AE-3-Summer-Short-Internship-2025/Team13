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
            
        # 必要な情報だけを抽出し、日本語キーを持つ辞書のリストを作成
        items_data = []
        for item in result['Items']:
            item_info = item['Item']
            items_data.append({
                '商品名': item_info.get('itemName'), 
                '価格': item_info.get('itemPrice'), 
                'ショップ名': item_info.get('shopName'), 
                '評価点': item_info.get('reviewAverage'),
                'itemUrl': item_info.get('itemUrl'), # 商品ページURL
                'itemCode': item_info.get('itemCode') # itemCodeも念のため残します
            })
        return items_data

    except requests.exceptions.RequestException as e:
        error_details = ""
        try:
            error_details = e.response.json()
        except (ValueError, AttributeError):
            pass 
        print(f"通信エラーが発生しました (ソート: {sort_key}): {e}")
        if error_details:
            print(f"サーバーからのエラー詳細: {error_details}")
        return None

# --- メインの処理（デモ機能付き） ---
if __name__ == "__main__":
    print(f"キーワード「{SEARCH_KEYWORD}」の各種TOP10リストを取得します...\n")
    
    lists_to_show = {
        f"【{SEARCH_KEYWORD}】売れ筋商品 TOP10": "standard",
        f"【{SEARCH_KEYWORD}】新着商品（更新日時順） TOP10": "-updateTimestamp",
        f"【{SEARCH_KEYWORD}】評価順商品 TOP10": "-reviewAverage",
        f"【{SEARCH_KEYWORD}】価格が安い順 TOP10": "+itemPrice"
    }
    
    all_results = {}
    
    # 1. 全てのリストを取得して保存
    for i, (title, sort_param) in enumerate(lists_to_show.items()):
        print(f"--- ({i+1}) {title} を取得中 ---")
        products = fetch_rakuten_products(keyword=SEARCH_KEYWORD, sort_key=sort_param)
        
        if products:
            # 表示用に情報を整形
            for rank, p in enumerate(products):
                print(f"  {rank+1:2d}. {p['商品名']} (価格: {p['価格']}円)")
            all_results[i+1] = {"title": title, "products": products}
        else:
            all_results[i+1] = {"title": title, "products": []}
        
        print("\n" + "="*60 + "\n")
        time.sleep(1)

    # 2. ユーザーに商品を選択させる
    while True:
        try:
            list_num_str = input("商品ページを見たいリストの番号を入力してください (例: 1) (終了するには'q'を入力): ")
            if list_num_str.lower() == 'q':
                break
            list_num = int(list_num_str)

            item_num_str = input(f"リスト({list_num})から商品番号を入力してください (例: 3) (終了するには'q'を入力): ")
            if item_num_str.lower() == 'q':
                break
            item_num = int(item_num_str)

            # 選択された商品情報を取得
            selected_list = all_results.get(list_num)
            if not selected_list or not selected_list["products"] or not (0 < item_num <= len(selected_list["products"])):
                print("無効な番号です。もう一度入力してください。")
                continue

            selected_item = selected_list["products"][item_num - 1]
            
            product_url = selected_item.get('itemUrl')
            
            if product_url:
                print("\n--- 選択された商品 ---")
                print(f"商品名: {selected_item['商品名']}")
                print("\n以下のURLをブラウザで開くと、商品ページにアクセスできます。")
                print(f"URL: {product_url}\n")
            else:
                print("エラー: この商品のURLが取得できませんでした。")

        except ValueError:
            print("無効な入力です。半角数字で入力してください。")
        except (KeyboardInterrupt, EOFError):
            break
            
    print("\nプログラムを終了します。")

