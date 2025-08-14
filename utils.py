"""توابع کمکی عمومی برای پروژه.

این ماژول مجموعه‌ای از توابع کمکی را شامل می‌شود که در بخش‌های مختلف برنامه مورد استفاده قرار می‌گیرند، مثل:
* خروجی گرفتن از جدول‌های PyQt به فایل اکسل
* پشتیبان‌گیری و بازیابی پایگاه‌داده PostgreSQL
* ساخت PDF فاکتور

برای سادگی، پیاده‌سازی کامل توابع از کد اصلی منتقل شده و در صورت نیاز می‌توانید جزییات بیشتری اضافه کنید.
"""

import os
import subprocess
from typing import List
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .config import to_shamsi


def export_table_to_excel(headers: List[str], data: List[List], path: str) -> None:
    """خروجی گرفتن داده‌ها به فایل اکسل.

    Args:
        headers: لیست عناوین ستون‌ها.
        data: لیست سطرهای داده.
        path: مسیر فایل خروجی.
    """
    df = pd.DataFrame(data, columns=headers)
    df.to_excel(path, index=False)


def backup_database(db_name: str, user: str, password: str, host: str, port: str, backup_path: str) -> None:
    """پشتیبان‌گیری از پایگاه‌داده PostgreSQL.

    Args:
        db_name: نام دیتابیس.
        user: نام کاربری دیتابیس.
        password: رمز کاربر.
        host: آدرس میزبان.
        port: درگاه اتصال.
        backup_path: مسیر ذخیره فایل backup (فرمت .dump).
    Note:
        این تابع نیازمند وجود ابزار `pg_dump` در سیستم است.
    """
    command = [
        'pg_dump',
        f'--dbname=postgresql://{user}:{password}@{host}:{port}/{db_name}',
        '-Fc',  # custom format
        '-f', backup_path,
    ]
    subprocess.run(command, check=True)


def restore_database(db_name: str, user: str, password: str, host: str, port: str, backup_path: str) -> None:
    """بازیابی پایگاه‌داده PostgreSQL از فایل پشتیبان.

    Args:
        db_name: نام دیتابیس مقصد.
        user: نام کاربری.
        password: رمز عبور.
        host: میزبان.
        port: درگاه.
        backup_path: مسیر فایل backup.
    Note:
        این تابع نیازمند وجود ابزار `pg_restore` است. دیتابیس مقصد باید قبل از بازیابی ایجاد شده باشد.
    """
    command = [
        'pg_restore',
        f'--dbname=postgresql://{user}:{password}@{host}:{port}/{db_name}',
        '--clean',
        backup_path,
    ]
    subprocess.run(command, check=True)


def create_invoice_pdf(pdf_path: str, items: List[dict], title: str = "فاکتور") -> None:
    """ساخت فاکتور PDF ساده برای فهرست اقلام.

    Args:
        pdf_path: مسیر فایل خروجی PDF.
        items: لیستی از دیکشنری‌ها شامل اطلاعات کالاها (مثلا name, quantity, price).
        title: عنوان فاکتور.
    Note:
        این پیاده‌سازی ساده فقط به‌عنوان نمونه آورده شده است. نسخه اصلی شامل جزئیات بیشتری (فونت فارسی، جدول‌بندی و...) است.
    """
    c = canvas.Canvas(pdf_path, pagesize=landscape(A4))
    width, height = landscape(A4)
    c.setFont("Helvetica", 14)
    c.drawString(30, height - 50, title)
    c.setFont("Helvetica", 10)
    y = height - 80
    for item in items:
        row = f"{item.get('name', '')} \t {item.get('quantity', '')} \t {item.get('price', '')}"
        c.drawString(30, y, row)
        y -= 20
    c.save()
