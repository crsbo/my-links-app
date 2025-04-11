from flask import Flask, render_template, request, redirect, url_for
import os
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

# دالة لفتح قاعدة البيانات
def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

# التأكد من أن قاعدة البيانات موجودة
def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY)''')
    c.execute('''CREATE TABLE IF NOT EXISTS links (username TEXT, title TEXT, url TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages (username TEXT, message TEXT)''')
    conn.commit()
    conn.close()

# تهيئة قاعدة البيانات عند تشغيل السيرفر
init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_links', methods=['POST'])
def add_links():
    username = request.form['username']
    return redirect(url_for('user_links', username=username))

@app.route('/add_links/<username>', methods=['GET', 'POST'])
def user_links(username):
    conn = get_db()
    c = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        url = request.form['url']
        c.execute('INSERT INTO links (username, title, url) VALUES (?, ?, ?)', (username, title, url))
        conn.commit()

    c.execute('SELECT title, url FROM links WHERE username = ?', (username,))
    links = c.fetchall()
    conn.close()

    return render_template('links.html', username=username, links=links)

@app.route('/delete_link/<username>/<int:index>')
def delete_link(username, index):
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM links WHERE username = ? AND rowid = ?', (username, index + 1))
    conn.commit()
    conn.close()
    return redirect(url_for('user_links', username=username))

@app.route('/send_message/<username>', methods=['POST'])
def send_message(username):
    message = request.form['message']
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO messages (username, message) VALUES (?, ?)', (username, message))
    conn.commit()
    conn.close()
    return redirect(url_for('show_bio', username=username))

@app.route('/view_messages/<username>')
def view_messages(username):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT message FROM messages WHERE username = ?', (username,))
    messages = c.fetchall()
    conn.close()
    return render_template('messages.html', username=username, messages=messages)

@app.route('/confirm_links/<username>', methods=['POST'])
def confirm_links(username):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT title, url FROM links WHERE username = ?', (username,))
    links = c.fetchall()
    conn.close()
    
    bio_url = f"https://{request.host}/bio/{username}"
    return render_template('links.html', username=username, links=links, bio_url=bio_url)

@app.route('/bio/<username>')
def show_bio(username):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT title, url FROM links WHERE username = ?', (username,))
    links = c.fetchall()
    conn.close()
    return render_template('bio.html', username=username, links=links)

if __name__ == '__main__':
    app.run(debug=True)
