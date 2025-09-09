from flask import Flask
from dotenv import load_dotenv
import os
from pathlib import Path
import mysql.connector


env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

print("DB_NAME:", os.getenv("DB_NAME"))  # ← team13_db と表示されるか確認


app = Flask(__name__)



@app.route("/")
def index():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    cursor = conn.cursor()
    cursor.execute("SELECT NOW();")
    result = cursor.fetchone()
    conn.close()
    return f"MySQL connected! Now: {result}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
