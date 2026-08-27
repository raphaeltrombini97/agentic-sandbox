"""Tiny demo app with an intentional SQL injection, for testing CodeQL +
the gs-agentic remediation pipeline. Do not use this pattern in real code.
"""
import sqlite3

from flask import Flask, request

app = Flask(__name__)


def get_user(conn: sqlite3.Connection, username: str):
    query = "SELECT id, username, email FROM users WHERE username = ?"
    cursor = conn.execute(query, (username,))
    return cursor.fetchone()


def init_db() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, email TEXT)")
    conn.execute("INSERT INTO users (username, email) VALUES ('alice', 'alice@example.com')")
    conn.commit()
    return conn


@app.route("/user")
def user_lookup():
    # Untrusted source: query string reaches get_user() unsanitized, which is
    # what lets CodeQL's py/sql-injection query trace an actual taint flow.
    conn = init_db()
    username = request.args.get("username", "")
    row = get_user(conn, username)
    return {"row": row}


if __name__ == "__main__":
    connection = init_db()
    print(get_user(connection, "alice"))
