"""مدیریت اتصال و pool برای PostgreSQL.

این ماژول تابعی برای ایجاد یا برگرداندن یک connection pool فراهم می‌کند. در کد اصلی، class DB از psycopg2 pool استفاده می‌کرد. اینجا یک نمونه ساده ارائه می‌شود.
"""

import psycopg2
from psycopg2 import pool
from typing import Optional
import configparser
from pathlib import Path

_pool: Optional[pool.SimpleConnectionPool] = None


def get_connection_pool(config_path: str = "config.ini") -> pool.SimpleConnectionPool:
    """ایجاد pool اتصال به دیتابیس یا بازگرداندن نمونه موجود.

    Args:
        config_path: مسیر فایل پیکربندی که اطلاعات اتصال در بخش POSTGRES ذخیره شده است.
    Returns:
        pool.SimpleConnectionPool آماده استفاده.
    """
    global _pool
    if _pool is None:
        parser = configparser.ConfigParser()
        parser.read(config_path, encoding='utf-8')
        cfg = parser['POSTGRES']
        _pool = psycopg2.pool.SimpleConnectionPool(
            1,
            10,
            host=cfg.get('host'),
            port=cfg.get('port'),
            database=cfg.get('database'),
            user=cfg.get('user'),
            password=cfg.get('password'),
        )
    return _pool
