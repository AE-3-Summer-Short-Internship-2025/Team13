# 楽天 Rakuten Team13🔴

> This is the app for managing your emergency food and other supplies. Fully integrated with Rakuten API.

## チームメンバー

- Ishida Haruka: バックエンド💾
- Uemura Oura: バックエンド💾
- Nakada Takamizu: バックエンド💾
- Prajeeyachat Zachariah: フロントエンド🎨
- Yoshida Takahiro: フロントエンド🎨

---

## 技術スタック (THE STACK)

- フロントエンド: React
- バックエンド: Flask (パイソン)
- データベース: MySQL

---

## セットアップ方法 (How to set up)

このプロジェクトを自分のPCで動かすための手順です。

### 1. プロジェクトをクローン (Clone the Project)

まず、このリポジトリを自分のPCにコピーします。

```bash
git clone https://github.com/AE-3-Summer-Short-Internship-2025/Team13.git
cd (backend | database | frontend)
```

### 2. データベースの準備 (Database Setup)

ローカルのMySQLサーバーにデータベースとテーブルを作成します。

```bash
# 1. MySQLにログイン
mysql -u root -p

# 2. データベースを作成
CREATE DATABASE [好きなデータベース名] CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

# 3. ログインし直して、SQLファイルを実行
mysql -u root -p [作成したデータベース名] < database/schema.sql
```

### 3. バックエンドの準備 (Backend Setup)

Flaskサーバーを動かすための準備です。

```bash
# /backend ディレクトリに移動
cd backend

# 仮想環境を作成して有効化 (Windows/Macでコマンドが少し違います)
python -m venv venv
# Mac/Linux: source venv/bin/activate
# Windows: venv\Scripts\activate
```

### 4. フロントエンドの準備 (Frontend Setup)

Reactアプリを動かすための準備です。

```bash
# 必要なライブラリをインストール
pip install -r requirements.txt
# /frontend ディレクトリに移動
cd ../frontend

# 必要なライブラリをインストール
npm install
```

---

## 実行方法 (How to Run)

重要: バックエンドとフロントエンドは、それぞれ別のターミナルで実行してください。

### ターミナル1: バックエンドサーバーの起動

```bash
# /backend ディレクトリにいることを確認
# 仮想環境が有効化されていることを確認 ( (venv) が行の先頭に表示されている)
flask run

# これで http://127.0.0.1:5000 でバックエンドが起動します
```

### ターミナル2: フロントエンドサーバーの起動

```bash
# /frontend ディレクトリにいることを確認
npm start

# これで http://localhost:3000 がブラウザで自動的に開きます
```
