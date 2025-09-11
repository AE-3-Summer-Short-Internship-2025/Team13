import requests
import json

# ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
# ご自身のアプリIDをここに貼り付けてください
APP_ID = '1088027222225008171' # 必ずご自身のIDに書き換えてください
# ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲

# 最も基本的なAPI（総合ランキング）のURL
TEST_URL = 'https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20240222'

params = {
    'applicationId': APP_ID,
    'format': 'json',
    'genreId': '0', # 総合ジャンル
}

print("--- API接続テストを開始します ---")
print(f"使用するID: {APP_ID}")

try:
    res = requests.get(TEST_URL, params=params)
    print(f"サーバーからの応答コード: {res.status_code}")
    res.raise_for_status() 
    
    result = res.json()
    item_name = result['Items'][0]['Item']['itemName']
    
    print("\n>>> テスト成功！ APIは正常に応答しました。")
    print("    このアプリIDは有効です。")
    print(f"    取得データ例: {item_name[:40]}...")

except requests.exceptions.HTTPError:
    print("\n>>> テスト失敗... APIからエラーが返されました。")
    print("    このアプリIDは現在利用できない状態です。")
    print("\n---考えられる原因---")
    print("1. Rakuten Developersサイトで、利用規約への再同意が必要になっている。")
    print("2. IDをコピーする際に、間違えている。")
    print("3. アプリが何らかの理由で無効化されている。")
    
    try:
        # サーバーからのエラー詳細を分かりやすく表示
        error_details = res.json()
        print("\n--- サーバーからのエラーメッセージ ---")
        print(json.dumps(error_details, indent=2, ensure_ascii=False))
        print("------------------------------------")
    except json.JSONDecodeError:
        pass

except Exception as e:
    print(f"\n>>> テスト失敗... 予期せぬエラーが発生しました: {e}")
