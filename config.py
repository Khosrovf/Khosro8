"""پیکربندی و عملیات اولیه سیستم.

این ماژول شامل توابعی است که برای ایجاد و خواندن فایل پیکربندی، هش کردن رمز عبور و تبدیل تاریخ استفاده می‌شود. این توابع از کد اصلی منتقل شده‌اند تا ساختار ماژولار بهبود یابد.
"""

import os
import configparser
from passlib.context import CryptContext
import hashlib
from datetime import datetime
import jdatetime


# پیکربندی زمینه‌ی رمزگذاری
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def hash_password(password: str) -> str:
    """تولید هش رمز عبور با استفاده از bcrypt.

    Args:
        password: رمز عبور متنی.
    Returns:
        رشته‌ی هش شده.
    """
    return pwd_context.hash(password)



def verify_password(plain_password: str, hashed_password: str) -> bool:
    """بررسی صحت رمز عبور با استفاده از bcrypt.

    Args:
        plain_password: رمز خام وارد شده.
        hashed_password: رمز هش شده.
    Returns:
        True اگر رمز صحیح باشد، در غیر این صورت False.
    """
    return pwd_context.verify(plain_password, hashed_password)



def create_config_if_not_exists(config_path: str) -> None:
    """ایجاد فایل config.ini در صورت عدم وجود و تنظیم مقادیر پیش‌فرض.

    Args:
        config_path: مسیر فایل پیکربندی.
    """
    if not os.path.exists(config_path):
        config = configparser.ConfigParser()
        config['POSTGRES'] = {
            'host': 'localhost',
            'port': '5432',
            'database': 'inventory_db',
            'user': 'username',
            'password': 'password'
        }
        with open(config_path, 'w', encoding='utf-8') as f:
            config.write(f)



def to_shamsi(dt: datetime) -> str:
    """تبدیل تاریخ میلادی به جلالی به صورت رشته.

    Args:
        dt: تاریخ میلادی.
    Returns:
        تاریخ جلالی در قالب YYYY/MM/DD.
    """
    jdate = jdatetime.date.fromgregorian(date=dt.date())
    return f"{jdate.year:04d}/{jdate.month:02d}/{jdate.day:02d}"



def shamsi_to_gregorian(date_str: str) -> datetime:
    """تبدیل رشته‌ی تاریخ جلالی به شیء datetime میلادی.

    Args:
        date_str: رشته‌ی تاریخ جلالی (YYYY/MM/DD).
    Returns:
        شیء datetime میلادی.
    """
    parts = list(map(int, date_str.split('/')))
    jdate = jdatetime.date(year=parts[0], month=parts[1], day=parts[2])
    return jdate.togregorian()
