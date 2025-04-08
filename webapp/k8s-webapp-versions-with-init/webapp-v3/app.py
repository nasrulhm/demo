from flask import Flask, request
import psycopg2
import datetime

app = Flask(__name__)
conn = psycopg2.connect("dbname='appdb' user='appuser' host='db' password='secret'")
cursor = conn.cursor()

@app.route("/")
def log_access():
    try:
        now = datetime.datetime.now()
        cursor.execute("INSERT INTO access_logs (timestamp, ip) VALUES (%s, %s)", (now, request.remote_addr))
        conn.commit()
        return "Access logged!"
    except Exception as e:
        conn.rollback()  # <- important to reset bad transaction
        return f"Error logging access: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
