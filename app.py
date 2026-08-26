"""Tiny demo app with an intentional SQL injection, for testing CodeQL +
the gs-agentic remediation pipeline. Do not use this pattern in real code.
"""
import sqlite3


def get_user(conn: sqlite3.Connection, username: str):
    # Intentionally vulnerable: user input concatenated into the query
    # instead of using a parameterized query. CodeQL rule: py/sql-injection.
    query = "SELECT id, username, email FROM users WHERE username = '" + username + "'"
    cursor = conn.execute(query)
    return cursor.fetchone()


def init_db() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, email TEXT)")
    conn.execute("INSERT INTO users (username, email) VALUES ('alice', 'alice@example.com')")
    conn.commit()
    return conn


if __name__ == "__main__":
    connection = init_db()
    print(get_user(connection, "alice"))
