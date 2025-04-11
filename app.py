from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# مسار قاعدة البيانات (سيتم استخدامه على Railway)
DATABASE = 'database.db'

# الاتصال بقاعدة البيانات
def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

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
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    
    if user is None:
        return redirect(url_for('home'))

    user_id = user[0]

    if request.method == 'POST':
        title = request.form['title']
        url = request.form['url']
        cursor.execute("INSERT INTO links (user_id, title, url) VALUES (?, ?, ?)", (user_id, title, url))
        conn.commit()

    cursor.execute("SELECT title, url FROM links WHERE user_id=?", (user_id,))
    links = cursor.fetchall()

    return render_template('links.html', username=username, links=links)

@app.route('/delete_link/<username>/<int:index>')
def delete_link(username, index):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username=?", (username,))
    user = cursor.fetchone()

    if user is None:
        return redirect(url_for('home'))

    user_id = user[0]
    cursor.execute("DELETE FROM links WHERE user_id=? AND id=?", (user_id, index))
    conn.commit()

    return redirect(url_for('user_links', username=username))

@app.route('/bio/<username>')
def show_bio(username):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username=?", (username,))
    user = cursor.fetchone()

    if user is None:
        return redirect(url_for('home'))

    user_id = user[0]
    cursor.execute("SELECT title, url FROM links WHERE user_id=?", (user_id,))
    links = cursor.fetchall()

    return render_template('bio.html', username=username, links=links)

@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        anonymous_sender = request.form['anonymous_sender']
        message = request.form['message']
        username = request.form['username']

        # الحصول على user_id من قاعدة البيانات
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=?", (username,))
        user = cursor.fetchone()

        if user is None:
            return redirect(url_for('home'))

        user_id = user[0]
        cursor.execute("INSERT INTO messages (user_id, message, anonymous_sender) VALUES (?, ?, ?)", (user_id, message, anonymous_sender))
        conn.commit()

        return redirect(url_for('home'))

    return render_template('send_message.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
