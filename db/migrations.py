"""تعریف و اجرای مهاجرت‌های پایگاه‌داده."""

from typing import Iterable
from psycopg2.extensions import connection

CREATE_TABLES_SQL: Iterable[str] = [
    """
    CREATE TABLE IF NOT EXISTS items (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT,
        unit TEXT,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """,
    # سایر جداول ...
]


def apply_migrations(conn: connection) -> None:
    """اجرای همه‌ی مهاجرت‌های تعریف‌شده."""
    with conn.cursor() as cur:
        for sql in CREATE_TABLES_SQL:
            cur.execute(sql)
    conn.commit()
