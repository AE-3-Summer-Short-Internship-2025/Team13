from flask import Flask, jsonify, request, session, make_response
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, date
from flask_cors import CORS
from flask_migrate import Migrate
import requests
import pandas as pd
import re
from marshmallow import Schema, fields, ValidationError
# from rankpage import fetch_rakuten_products

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


# 有効期限チェック関数
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
        result = db.session.execute("SELECT NOW();").scalar()
        return jsonify({"message": "データベース接続成功！", "now": str(result)})
    except Exception as e:
        return jsonify({"error": "データベース接続失敗", "details": str(e)}), 500


class ItemSchema(Schema):
    item_code = fields.Str(required=True, validate=lambda x: len(x.strip()) > 0)

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
        app.logger.error(f"Error fetching items: {str(e)}")
        return jsonify({"error": "データの取得に失敗しました"}), 500
    
@app.route("/api/fetch_and_add_item", methods=['POST'])
def fetch_and_add_item():
    schema = ItemSchema()
    try:
        # フロントから item_code を受け取る
        data = request.get_json()
        item_code = data.get("item_code")
        if not item_code:
            return jsonify({"error": "item_code is required"}), 400

        # 楽天API（キーワード検索）で商品取得
        REQUEST_URL = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601'
        APP_ID = '1009667447566505226'
        params = {
            'applicationId': APP_ID,
            'format': 'json',
            # 'keyword': item_code
            # 'keyword': item_code
            'keyword': 10000953
        }

        res = requests.get(REQUEST_URL, params=params)
        result = res.json()

        if not result.get("Items"):
            return jsonify({"error": "商品が見つかりません"}), 404

        items = [item['Item'] for item in result['Items']]
        df = pd.DataFrame(items)

        # 画像URLをカンマ区切りの文字列に変換
        df['smallImageUrl'] = df['smallImageUrls'].apply(
            lambda x: ','.join([d['imageUrl'] for d in x]) if isinstance(x, list) else None
        )

        # def extract_expiry(text):
        #     if pd.isna(text):
        #         return None
        #     patterns = [
        #         (r"賞味期限\s*[:：]?\s*(\d{4}年\d{1,2}月\d{1,2}日)", 'raw'),
        #         (r"賞味期限\s*[:：]?\s*(\d{4}年\d{1,2}月)", 'raw'),
        #         (r"賞味期限\s*(\d+)\s*[年ヶ月日]", 'digit'),
        #         (r"(\d+)\s*[年ヶ月日]保存", 'digit'),
        #         (r"保存期間\s*(\d+)\s*[年ヶ月日]", 'digit'),
        #         (r"保存可能\s*(\d+)\s*[年ヶ月日]", 'digit'),
        #         (r"長期保存\s*(\d+)\s*[年ヶ月日]?", 'digit'),
        #         (r"製造日より\s*(\d+)\s*[年ヶ月日]保存可能", 'digit'),
        #     ]
        #     for pattern, mode in patterns:
        #         match = re.search(pattern, text)
        #         if match:
        #             return match.group(1) if mode == 'raw' else int(match.group(1))
        #     return None

        # df['date_expiry'] = df['itemCaption'].apply(extract_expiry)

        # 最初の1件だけ使う
        item = df.iloc[0]
        # expiry = item['date_expiry']
        # if isinstance(expiry, int):
        #     expiry = datetime.now() + timedelta(days=expiry * 365)
        # elif isinstance(expiry, str):
        #     try:
        #         expiry = pd.to_datetime(expiry)
        #     except:
        #         expiry = None

        # DBに追加
        # トランザクション処理の改善
        with db.session.begin():
            new_item = Items(
                item_name=item['itemName'][:100],  # 長さ制限
                quantity=1,
                smallImageUrls=item['smallImageUrl'][:255],  # 長さ制限
                date_added=datetime.now(),
                is_grocery=True
            )
            db.session.add(new_item)
            # commitは自動的に行われる

            
        return create_response(
            data={"id": new_item.id}, 
            message="商品を追加しました"
        )
        
    except requests.RequestException as e:
        app.logger.error(f"楽天API Error: {str(e)}")
        return create_response(error="商品情報の取得に失敗しました", status_code=500)
    except Exception as e:
        app.logger.error(f"Database Error: {str(e)}")
        return create_response(error="データベースエラーが発生しました", status_code=500)

# @app.route("/api/ranking", methods=["POST"])
# def get_ranking():
#     data = request.get_json()
#     keyword = data.get("keyword")
#     sort_key = data.get("sort")

#     if not keyword or not sort_key:
#         return jsonify({"error": "キーワードとソート順が必要です"}), 400

#     df = fetch_rakuten_products(keyword, sort_key)

#     if df is None or df.empty:
#         return jsonify({"error": "商品が見つかりませんでした"}), 404

#     # DataFrameをJSON形式に変換
#     result = df.to_dict(orient="records")
#     return jsonify(result)
def create_response(data=None, message=None, error=None, status_code=200):
    response = {}
    if data is not None:
        response['data'] = data
    if message:
        response['message'] = message
    if error:
        response['error'] = error
    return jsonify(response), status_code

# 使用例



if __name__ == "__main__":
    # 初回起動時にテーブル作成
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=5000, debug=True)
