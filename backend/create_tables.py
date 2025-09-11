from app import db, app

# Flaskアプリのコンテキスト内で実行
with app.app_context():
    db.create_all()
    print("全てのテーブルを作成しました！")
