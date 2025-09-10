import requests
import pandas as pd
import webbrowser

# ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
APP_ID = '1009667447566505226' # サンプルID
# ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲

# 楽天商品ランキングAPIのURL
RANKING_URL = 'https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20220601'

def get_rakuten_ranking(genre_id='0'):
    """
    楽天のジャンル別ランキングを取得して、pandas DataFrameとして返す関数
    genre_id: 楽天のジャンルID (0は総合ランキング)
    """
    params = {
        'applicationId': APP_ID,
        'format': 'json',
        'genreId': genre_id,
    }

    try:
        res = requests.get(RANKING_URL, params=params)
        # ステータスコードが200以外の場合はエラーメッセージを表示
        if res.status_code != 200:
            print(f"エラー: APIリクエストに失敗しました (ステータスコード: {res.status_code})")
            print(f"レスポンス: {res.text}")
            return None

        result = res.json()

        # 'Items'キーが存在するかチェック
        if 'Items' not in result:
            print("エラー: レスポンスに 'Items' が見つかりませんでした。")
            print(f"APIからのレスポンス: {result}")
            return None

        # 商品情報を抽出
        items_data = [item['Item'] for item in result['Items']]
        df = pd.DataFrame(items_data)

        # 必要なカラムだけを選択し、カラム名を日本語にリネーム
        columns_to_keep = {
            'rank': 'ランキング',
            'itemName': '商品名',
            'itemPrice': '価格',
            'shopName': 'ショップ名',
            'itemCode': '商品コード' # カゴ追加URL生成に必要
        }
        df = df[list(columns_to_keep.keys())]
        df = df.rename(columns=columns_to_keep)

        return df

    except requests.exceptions.RequestException as e:
        print(f"通信エラーが発生しました: {e}")
        return None
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
        return None

def generate_add_to_cart_url(item_code):
    """
    商品コードから「買い物かごへ追加」のURLを生成する関数
    """
    # itemCodeは "shopCode:itemNumber" の形式なので分割する
    try:
        shop_code, item_number = item_code.split(':')
        base_url = "https://basket.step.rakuten.co.jp/rms/mall/bs/cartadd/set"
        # URLのパラメータを組み立てる
        cart_url = f"{base_url}?shop_id={shop_code}&item_id={item_number}&units=1"
        return cart_url
    except ValueError:
        print("エラー: itemCodeの形式が正しくありません。")
        return None

# --- メインの処理 ---
if __name__ == "__main__":
    # 例として「パソコン・周辺機器」ジャンル(ID: 100227)のランキングを取得
    # ジャンルID一覧: https://webservice.rakuten.co.jp/explorer/api/IchibaItem/Genre/Search/
    # 0 を指定すると総合ランキングになります。
    target_genre_id = '100227'
    print(f"ジャンルID: {target_genre_id} の人気商品ランキングを取得します...")

    ranking_df = get_rakuten_ranking(target_genre_id)

    if ranking_df is not None:
        # ランキングを表示 (インデックスを1から始める)
        ranking_df.index = ranking_df.index + 1
        print("\n--- 楽天 人気商品ランキング ---")
        print(ranking_df[['ランキング', '商品名', '価格', 'ショップ名']].to_string())
        print("---------------------------\n")

        while True:
            try:
                prompt = "買い物かごに追加したい商品の番号（左端の数字）を入力してください (終了する場合は 'q' または 'exit'): "
                user_input = input(prompt)

                if user_input.lower() in ['q', 'exit']:
                    print("プログラムを終了します。")
                    break

                item_index = int(user_input)

                # 入力された番号がランキングの範囲内かチェック
                if item_index not in ranking_df.index:
                    print(f"エラー: 1から{len(ranking_df)}までの数字を入力してください。")
                    continue

                # ユーザーが選んだ商品の情報を取得
                selected_item = ranking_df.loc[item_index]
                item_code = selected_item['商品コード']

                print(f"\n選択した商品: {selected_item['商品名']}")

                # 買い物かごに追加するURLを生成
                cart_url = generate_add_to_cart_url(item_code)

                if cart_url:
                    print(f"以下のURLをブラウザで開きます:\n{cart_url}")
                    # ブラウザでURLを自動的に開く
                    webbrowser.open(cart_url)
                    print("ブラウザで買い物かごのページを開きました。内容を確認してください。\n")

            except ValueError:
                print("エラー: 有効な数字を入力してください。")
            except Exception as e:
                print(f"エラーが発生しました: {e}")
