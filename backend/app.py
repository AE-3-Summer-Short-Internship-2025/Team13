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


@app.route("/")
def index():
    items = Items.query.all()
    return jsonify([{"id": item.id, "item_name": item.item_name, "quantity": item.quantity,             "item_url": item.smallImageUrls} for item in items])


@app.route("/api/items")
def get_items():
    items = Items.query.all()
    return jsonify([
        {
            "id": i.id,
            "name": i.item_name,
            "quantity": i.quantity,
            "smallImageUrls": i.smallImageUrls 
        } for i in items
    ])
    
@app.route("/api/fetch_and_add_item", methods=["POST"])
def fetch_and_add_item():
    data = request.get_json()
    jan_code = data.get("itemCode")  # 数字だけ（JANコード）

    if not jan_code:
        return jsonify({"error": "itemCode is required"}), 400

    # 楽天API（キーワード検索）で商品取得
    REQUEST_URL = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601'
    APP_ID = '1009667447566505226'
    params = {
        'applicationId': APP_ID,
        'format': 'json',
        'keyword': jan_code,
    }

    try:
        res = requests.get(REQUEST_URL, params=params)
        result = res.json()

        if not result.get("Items"):
            return jsonify({"error": "商品が見つかりません"}), 404

        items = [item['Item'] for item in result['Items']]
        df = pd.DataFrame(items)

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

        new_item = Items(
            owner_id=1,
            item_name=item['itemName'],
            quantity=1,
            smallImageUrls=item['smallImageUrl'],
            # date_expiry=expiry,
            date_added=datetime.now(),
            is_grocery=True
        )

        db.session.add(new_item)
        db.session.commit()

        return jsonify({"message": "Item added", "id": new_item.id})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    # 初回起動時にテーブル作成
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=5000, debug=True)
