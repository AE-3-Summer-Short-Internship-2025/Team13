from flask import Flask, jsonify, request, session, make_response
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, date
from flask_cors import CORS
from flask_migrate import Migrate

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
    item_url = db.Column(db.String(255))
    date_expiry = db.Column(db.DateTime)
    date_added = db.Column(db.DateTime)


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
    return jsonify([{"id": item.id, "item_name": item.item_name, "quantity": item.quantity} for item in items])


@app.route("/api/items")
def get_items():
    items = Items.query.all()
    return jsonify([{"id": i.id, "name": i.item_name, "quantity": i.quantity, 'date_expiry': i.date_expiry} for i in items])


if __name__ == "__main__":
    # 初回起動時にテーブル作成
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=5000, debug=True)
