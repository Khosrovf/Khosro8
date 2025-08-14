"""کلاس DB برای تعامل با دیتابیس.

این کلاس نمونه‌ای ساده از پیاده‌سازی کلاس DB در کد اصلی است. متدهای بیشتر را می‌توانید بر اساس نیاز از فایل اصلی منتقل کنید.
"""

from typing import Any, Dict, List, Optional
from psycopg2.extensions import connection

from ..config import create_config_if_not_exists
from ..utils import export_table_to_excel
from ..enums import TransactionStatus, TransactionType
from .connection import get_connection_pool
from .migrations import apply_migrations


class DB:
    def __init__(self, config_path: str = "config.ini") -> None:
        create_config_if_not_exists(config_path)
        self.pool = get_connection_pool(config_path)
        with self.pool.getconn() as conn:
            apply_migrations(conn)

    def get_connection(self) -> connection:
        return self.pool.getconn()

    def release_connection(self, conn: connection) -> None:
        self.pool.putconn(conn)

    def add_item(self, name: str, category: str, unit: str) -> int:
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO items (name, category, unit) VALUES (%s, %s, %s) RETURNING id",
                    (name, category, unit),
                )
                item_id = cur.fetchone()[0]
            conn.commit()
            return item_id
        finally:
            self.release_connection(conn)

    def list_items(self) -> List[Dict[str, Any]]:
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name, category, unit, created_at FROM items")
                rows = cur.fetchall()
            result = [
                {
                    "id": row[0],
                    "name": row[1],
                    "category": row[2],
                    "unit": row[3],
                    "created_at": row[4],
                }
                for row in rows
            ]
            return result
        finally:
            self.release_connection(conn)

    # سایر متدها باید از فایل اصلی به اینجا منتقل شوند.
