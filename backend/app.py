from flask import Flask, jsonify, request, session, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column, ForeignKey, DateTime, func, MetaData
#リレーション用
from sqlalchemy.orm import relationship, sessionmaker
from pathlib import Path
import mysql.connector
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta,date

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)




app = Flask(__name__)

#dbエンジンの作成
engine = create_engine("mysql+pymysql://AZteam13:Team13pass@54.64.250.189:3306/team13_db?charset=utf8mb4", echo=True, future=True)
# engine = create_engine("mysql+mysqlconnector://AZteam13:Team13pass@54.64.250.189:3306/team13_db?charset=UTF-8", echo=True, future=True)

#モデルクラス作成
Base = declarative_base()

#命名規則の設定(予約キー)
metadata = MetaData(naming_convention={
    "fk" : "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "uq" : "uq_%(table_name)s_%(column_0_name)s",
    "ck" : "ck_%(table_name)s_%(constraint_name)s",
    "fk" : "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})


db = SQLAlchemy(app,metadata=metadata)



#Baseクラスの拡張

#familiesテーブル
class Families(Base):
    __tablename__ = 'families'
    id = Column(Integer, primary_key=True, autoincrement=True)
    family_name = Column(String(100), nullable=False)
    kids = Column(Integer, nullable=False)
    adults = Column(Integer, nullable=False)
    prefecture = Column(String(50))
    city_ward = Column(String(50))
    building = Column(String(50))
    #int型に変更
    postal_code = Column(Integer)
    #1対多のリレーション設定
    users = relationship("Users", backref="families")



#usersテーブル
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    phone = Column(String(16), unique=True)
    rakuten_id = Column(String(100), unique=True)
    #外部キー
    family_id = Column(Integer, ForeignKey('families.id'))
    
#itemsテーブル
class Items(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    item_name = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    date_expiry = Column(DateTime)
    date_added = Column(DateTime)

#metadataは，DBの様々な情報を保持しているオブジェクト
Base.metadata.create_all(engine)
    
SessionClass = sessionmaker(engine)
session = SessionClass()

# def check_expire(expiry_date,item_name):
#     if expiry_date < date.today():
#         expired_items = item_name
#         return expired_items
#     elif expiry_date <= date.today(): + timedelta(days=7):
#         expiring_items = item_name
#         return expiring_items
#     else:
#         return None
    
def check_expire(expiry_date, item_name):
    if expiry_date < date.today():
        return f"{item_name} は期限切れです"
    elif expiry_date <= date.today() + timedelta(days=7):
        return f"{item_name} は7日以内に期限切れになります"
    else:
        return None

@app.route("/")
def index():
    # conn = mysql.connector.connect(
    #     host=os.getenv("DB_HOST"),
    #     user=os.getenv("DB_USER"),
    #     password=os.getenv("DB_PASSWORD"),
    #     database=os.getenv("DB_NAME")
    # )
    famililys = session.query(Families).all()
    users = session.query(Users).all()
    items = session.query(Items).all()
    expired_items = session.query(Items).filter(Items.date_expiry < datetime.now()).all()
    return jsonify({"status": "ok"})


# @app.route('/api/users', methods=['GET', 'POST'])
# def users():
#     if request.method == 'GET':
#         # データベースからユーザーを取得するロジックを実装
#         pass
#     elif request.method == 'POST':
#         # データベースに新しいユーザーを作成するロジックを実装
#         pass


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)


