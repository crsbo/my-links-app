import sqlite3

# الاتصال بقاعدة البيانات (إذا لم توجد سيتم إنشاؤها)
conn = sqlite3.connect('database.db')

# إنشاء كائن لتنفيذ الاستعلامات
cursor = conn.cursor()

# إنشاء جدول المستخدمين
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
''')

# إنشاء جدول الروابط
cursor.execute('''
CREATE TABLE IF NOT EXISTS links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
''')

# إنشاء جدول الرسائل
cursor.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    anonymous_sender TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
''')

# حفظ التغييرات وإغلاق الاتصال
conn.commit()
conn.close()

print("تم إنشاء قاعدة البيانات بنجاح!")
