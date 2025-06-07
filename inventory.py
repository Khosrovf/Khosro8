import sqlite3
from datetime import datetime

DB_NAME = 'inventory.db'


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        category TEXT,
        unit TEXT,
        quantity REAL DEFAULT 0,
        price REAL,
        supplier TEXT,
        notes TEXT
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER,
        t_type TEXT,
        t_number TEXT,
        t_date TEXT,
        quantity REAL,
        notes TEXT,
        FOREIGN KEY(item_id) REFERENCES items(id)
    )''')
    conn.commit()
    conn.close()


def add_item():
    print('\nافزودن کالا')
    name = input('نام کالا: ')
    category = input('دسته‌بندی (مواد اولیه/محصول/مصرفی/دارایی): ')
    unit = input('واحد اندازه‌گیری: ')
    try:
        quantity = float(input('مقدار اولیه: '))
    except ValueError:
        quantity = 0
    try:
        price = float(input('قیمت واحد: '))
    except ValueError:
        price = 0
    supplier = input('تأمین‌کننده: ')
    notes = input('توضیحات: ')

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''INSERT INTO items (name, category, unit, quantity, price, supplier, notes)
                   VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (name, category, unit, quantity, price, supplier, notes))
    conn.commit()
    conn.close()
    print('کالا با موفقیت ثبت شد.')


def list_items():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('SELECT id, name, category, quantity, unit FROM items')
    rows = cur.fetchall()
    for row in rows:
        print(f"{row[0]} - {row[1]} ({row[2]}) موجودی: {row[3]} {row[4]}")
    conn.close()
    return rows


def select_item():
    rows = list_items()
    if not rows:
        print('هیچ کالایی وجود ندارد.')
        return None
    try:
        item_id = int(input('شناسه کالا را وارد کنید: '))
    except ValueError:
        print('ورودی نامعتبر')
        return None
    return item_id


def record_transaction(t_type):
    item_id = select_item()
    if not item_id:
        return
    try:
        quantity = float(input('مقدار: '))
    except ValueError:
        print('مقدار نامعتبر')
        return
    t_number = input('شماره تراکنش: ')
    notes = input('توضیحات: ')

    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''INSERT INTO transactions (item_id, t_type, t_number, t_date, quantity, notes)
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (item_id, t_type, t_number, date, quantity, notes))
    if t_type in ('ورود', 'برگشت'):
        cur.execute('UPDATE items SET quantity = quantity + ? WHERE id = ?', (quantity, item_id))
    else:
        cur.execute('UPDATE items SET quantity = quantity - ? WHERE id = ?', (quantity, item_id))
    conn.commit()
    conn.close()
    print('تراکنش ثبت شد.')


def report_inventory():
    print('\nگزارش موجودی')
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('SELECT id, name, category, quantity, unit FROM items')
    rows = cur.fetchall()
    for row in rows:
        print(f"{row[0]} - {row[1]} ({row[2]}) : {row[3]} {row[4]}")
    conn.close()


def report_transactions():
    print('\nگزارش تراکنش‌ها')
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''SELECT t.id, i.name, t.t_type, t.quantity, t.t_number, t.t_date, t.notes
                   FROM transactions t JOIN items i ON t.item_id = i.id
                   ORDER BY t.t_date DESC''')
    rows = cur.fetchall()
    for r in rows:
        print(f"{r[0]} - {r[1]} - {r[2]} - {r[3]} - شماره:{r[4]} - تاریخ:{r[5]} - {r[6]}")
    conn.close()


def main():
    init_db()
    while True:
        print('\nمدیریت انبار')
        print('1. افزودن کالا')
        print('2. ثبت ورود')
        print('3. ثبت خروج')
        print('4. ثبت برگشت')
        print('5. ثبت خروج دارایی')
        print('6. گزارش موجودی')
        print('7. گزارش تراکنش‌ها')
        print('0. خروج')
        choice = input('انتخاب: ')
        if choice == '1':
            add_item()
        elif choice == '2':
            record_transaction('ورود')
        elif choice == '3':
            record_transaction('خروج')
        elif choice == '4':
            record_transaction('برگشت')
        elif choice == '5':
            record_transaction('خروج دارایی')
        elif choice == '6':
            report_inventory()
        elif choice == '7':
            report_transactions()
        elif choice == '0':
            break
        else:
            print('انتخاب نامعتبر')


if __name__ == '__main__':
    main()
