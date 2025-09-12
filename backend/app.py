from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta, date
from flask_cors import CORS
from marshmallow import Schema, fields
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, Union
from flask_migrate import Migrate
import requests
import pandas as pd
import json
import time
import os

# .env 読み込み
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
CORS(app, origins=['http://localhost:5173'])

# DB接続設定
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:3306/{os.getenv('DB_NAME')}?charset=utf8mb4"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# SQLAlchemy 初期化
db = SQLAlchemy(app)
migrate = Migrate(app, db)


def create_response(
    data: Optional[dict] = None,
    message: Optional[str] = None,
    error: Optional[Union[str, dict]] = None,
    status_code: int = 200
):
    payload = {}
    if message is not None:
        payload["message"] = message
    if data is not None:
        payload["data"] = data
    if error is not None:
        payload["error"] = error if isinstance(error, dict) else {
            "message": str(error)}
    return jsonify(payload), status_code


# familiesテーブル
class Families(db.Model):
    __tablename__ = "families"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    family_name = db.Column(db.String(100), nullable=False)
    kids = db.Column(db.Integer, nullable=False)
    adults = db.Column(db.Integer, nullable=False)
    prefecture = db.Column(db.String(50))
    city_ward = db.Column(db.String(50))
    building = db.Column(db.String(50))
    postal_code = db.Column(db.Integer)  # int型に変更

    # リレーション
    users = db.relationship("Users", backref="family", lazy=True)


# usersテーブル
class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(16), unique=True)
    rakuten_id = db.Column(db.String(100), unique=True)

    # 外部キー
    family_id = db.Column(db.Integer, db.ForeignKey("families.id"))


# itemsテーブル
class Items(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    item_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    smallImageUrls = db.Column(db.String(255))
    date_expiry = db.Column(db.DateTime)
    date_added = db.Column(db.DateTime)
    is_grocery = db.Column(db.Boolean, default=False)


# 有効期限チェック関数（未使用のためそのまま温存）
def check_expire(expiry_date, item_name):
    if expiry_date < date.today():
        return f"{item_name} は期限切れです"
    elif expiry_date <= date.today() + timedelta(days=7):
        return f"{item_name} は7日以内に期限切れになります"
    else:
        return None


@app.route("/db_check")
def db_check():
    try:
        result = db.session.execute(text("SELECT NOW();")).scalar()
        return jsonify({"message": "✅ データベース接続成功！", "now": str(result)})
    except Exception as e:
        return jsonify({"error": "❌ データベース接続失敗", "details": str(e)}), 500


class ItemSchema(Schema):
    item_code = fields.Str(
        required=True, validate=lambda x: len(x.strip()) > 0)


@app.route("/api/items")
def get_items():
    try:
        items = Items.query.all()
        return jsonify([
            {
                "id": i.id,
                "name": i.item_name,
                "quantity": i.quantity,
                "smallImageUrls": i.smallImageUrls,
                "date_expiry": i.date_expiry.isoformat() if i.date_expiry else None
            } for i in items
        ])
    except Exception as e:
        app.logger.exception("Error fetching items")
        return jsonify({"error": "データの取得に失敗しました"}), 500


@app.route("/api/fetch_and_add_item", methods=['POST'])
def fetch_and_add_item():
    try:
        # フロントから item_code を受け取る
        data = request.get_json(silent=True) or {}
        item_code = data.get("item_code")
        if not item_code:
            return jsonify({"error": "item_code is required"}), 400

        # 楽天API（キーワード検索）で商品取得
        REQUEST_URL = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601'
        APP_ID = '1009667447566505226'
        params = {
            'applicationId': APP_ID,
            'format': 'json',
            'keyword': f'JAN {item_code}'
        }

        res = requests.get(REQUEST_URL, params=params, timeout=10)
        res.raise_for_status()
        result = res.json()

        if not result.get("Items"):
            return jsonify({"error": "商品が見つかりません"}), 404

        items = [item['Item'] for item in result['Items']]
        df = pd.DataFrame(items)

        # 画像URLをカンマ区切りの文字列に変換
        df['smallImageUrl'] = df['smallImageUrls'].apply(
            lambda x: ','.join([d.get('imageUrl', '')for d in x]) if isinstance(x, list) else None
        )

        # 最初の1件だけ使う
        item = df.iloc[0]

        # DBに追加
        with db.session.begin():
            small_img = item['smallImageUrl'] if pd.notna(
                item['smallImageUrl']) else ''
            new_item = Items(
                item_name=str(item['itemName'])[:100],        # 長さ制限
                quantity=1,
                smallImageUrls=str(small_img)[:255],          # 長さ制限 + Noneガード
                date_added=datetime.now(),
                is_grocery=True
            )
            db.session.add(new_item)

        return create_response(
            data={"id": new_item.id},
            message="商品を追加しました"
        )

    except requests.RequestException as e:
        app.logger.exception("楽天API Error")
        return create_response(error="商品情報の取得に失敗しました", status_code=500)
    except Exception as e:
        app.logger.exception("Database Error")
        return create_response(error="データベースエラーが発生しました", status_code=500)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    build_dir = os.path.join(os.path.dirname(__file__), 'build')
    if path != "" and os.path.exists(os.path.join(build_dir, path)):
        return send_from_directory(build_dir, path)
    else:
        return send_from_directory(build_dir, 'index.html')


# ランキングページの処理
# ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼

# 検索キーワード
SEARCH_KEYWORD = '防災'


# keyword, sort_key
@app.route('/api/item_ranking', methods=['GET', 'POST'])
def fetch_rakuten_products():
    """
    指定されたキーワードとソート順で楽天の商品を検索し、辞書のリストとして返す関数
    """
    # 自身の楽天アプリIDに書き換えてください
    APP_ID = '1088027222225008171'
    # 20220601バージョンを使用
    SEARCH_URL = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601'
    data = request.get_json(silent=True) or {}
    keyword = data.get('keyword')
    sort_key = data.get('sort_key')
    params = {
        'applicationId': APP_ID,
        'format': 'json',
        'keyword': keyword,
        'sort': sort_key,
        'hits': 10
    }
    try:
        res = requests.get(SEARCH_URL, params=params, timeout=10)
        res.raise_for_status()  # HTTPエラーが発生した際に例外を発生させる
        result = res.json()

        if not result.get('Items'):
            return jsonify({'error': f"「{keyword}」に関する商品が見つかりませんでした。(ソート: {sort_key})"}), 400

        # pandasを使わずに必要な情報だけを抽出し、日本語キーを持つ辞書のリストを作成
        items_data = []
        # 画像URLをカンマ区切りの文字列に変換

        # for item in result['Items']:
        #     item_info = item['Item']
        #     items_data.append({
        #         '商品名': item_info.get('itemName'),
        #         '価格': item_info.get('itemPrice'),
        #         'ショップ名': item_info.get('shopName'),
        #         '評価点': item_info.get('reviewAverage'),
        #         '画像': [img['imageUrl'] for img in item_info.get('smallImageUrls', [])]
        #     })
        for item in result['Items']:
            item_info = item['Item']
            # smallImageUrls が空でなければ最初の画像を取得、なければ None
            image_url = None
            if item_info.get('smallImageUrls'):
                image_url = item_info['smallImageUrls'][0].get('imageUrl')

            items_data.append({
                '商品名': item_info.get('itemName'),
                '価格': item_info.get('itemPrice'),
                'ショップ名': item_info.get('shopName'),
                '評価点': item_info.get('reviewAverage'),
                '画像': item_info.get('smallImageUrls')
            })
        return jsonify(items_data)

    except requests.exceptions.RequestException as e:
        # エラーの詳細（JSONレスポンス）を表示するように改良
        error_details = ""
        try:
            error_details = e.response.json()  # type: ignore[attr-defined]
        except (ValueError, AttributeError):
            return jsonify({
                'error': 'HTTP Error from Rakuten API',
                'status_code': e.response.status_code,
                'details': error_details
            }), e.response.status_code
        print(f"通信エラーが発生しました (ソート: {sort_key}): {e}")
        if error_details:
            print(f"サーバーからのエラー詳細: {error_details}")
            return jsonify({'error': 'Communication Error', 'details': str(e)}), 500


def run_ranking_demo():
    """起動時の毎回実行を避けるため、環境変数 RUN_RAKUTEN_DEMO=1 のときだけ実行"""
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

        products = fetch_rakuten_products(
            keyword=SEARCH_KEYWORD, sort_key=sort_param)

        if products is not None:
            # 新着順と価格順の場合は「評価点」キーを削除
            if sort_param in ["-updateTimestamp", "+itemPrice"]:
                for p in products:
                    if '評価点' in p:
                        del p['評価点']

            # 最終出力用の辞書に結果を格納
            final_output[title] = products
        else:
            final_output[title] = []  # 商品が取得できなかった場合は空のリストを格納

        # 楽天APIへの負荷を考慮し、1秒間待機
        time.sleep(1)

    # 全てのリストを取得した後、整形されたJSON形式で標準出力に表示
    print("\n" + "=" * 60)
    print("すべての結果をJSON形式で出力します。")
    print("=" * 60 + "\n")
    print(json.dumps(final_output, indent=2, ensure_ascii=False))


# Mypage関連のルートを登録
def register_mypage_routes(app, Families, Users):
    # 統一エラーレスポンス
    def error_response(
        code: str,
        message: str,
        http_status: int,
        details: Optional[Union[dict, str]] = None
    ):
        payload = {"error": {"code": code, "message": message}}
        if details is not None:
            payload["error"]["details"] = details
        return jsonify(payload), http_status

    @app.get("/api/mypage/summary")
    def get_mypage_summary():
        """
        指定ユーザーのサマリーを返す（表示用の取得API）。
        クエリ: ?user_id=<int>（暫定。将来は認証でサーバ側特定に置換）
        """
        # 1) user_id の厳密検証（無効値は 400）
        raw_user_id = request.args.get("user_id", default="1")
        try:
            user_id = int(raw_user_id)
        except (ValueError, TypeError):
            return error_response(
                code="INVALID_USER_ID",
                message="user_id must be an integer",
                http_status=400,
                details={"received": raw_user_id}
            )

        try:
            # 2) ユーザー取得（無ければ 404）
            user = Users.query.get(user_id)
            if not user:
                return error_response(
                    code="USER_NOT_FOUND",
                    message="user not found",
                    http_status=404,
                    details={"user_id": user_id}
                )

            # 3) 家族情報取得＆人数
            family_id = user.family_id
            adult_num = 0
            child_num = 0
            if family_id is not None:
                family = Families.query.get(family_id)
                if family:
                    adult_num = family.adults or 0
                    child_num = family.kids or 0

            # 4) ユーザー名整形（姓 名）
            lastname = (user.lastname or "").strip()
            firstname = (user.firstname or "").strip()
            name = f"{lastname} {firstname}".strip()

            # 5) 正常レスポンス
            return jsonify({
                "name": name,
                "user_id": user.id,
                "family_id": user.family_id,
                "adult_num": adult_num,
                "child_num": child_num
            }), 200

        except SQLAlchemyError as e:
            return error_response(
                code="DB_ERROR",
                message="database error",
                http_status=500,
                details=str(e)
            )

        except Exception as e:
            return error_response(
                code="INTERNAL_ERROR",
                message="unexpected error",
                http_status=500,
                details=str(e)
            )


# ルート登録（定義後に呼び出し）
register_mypage_routes(app, Families, Users)

if __name__ == "__main__":
    # ランキングデモは環境変数で明示的に有効化した時だけ実行
    if os.getenv("RUN_RAKUTEN_DEMO") == "1":
        run_ranking_demo()

    # 初回起動時にテーブル作成
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=5000, debug=True)
