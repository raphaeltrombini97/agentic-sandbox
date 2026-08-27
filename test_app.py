from app import get_user, init_db


def test_get_user_returns_alice():
    conn = init_db()
    row = get_user(conn, "alice")
    assert row is not None
    assert row[1] == "alice"


def test_get_user_treats_input_as_username():
    conn = init_db()

    row = get_user(conn, "' OR 1=1 --")

    assert row is None
