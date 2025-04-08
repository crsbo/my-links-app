from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = 'links_data.json'

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

# الصفحة الرئيسية لإدخال اسم المستخدم فقط
@app.route('/')
def home():
    return render_template('index.html')

# صفحة إضافة الروابط مع اختيارين: إضافة رابط آخر أو تأكيد الروابط
@app.route('/add_links', methods=['POST'])
def add_links():
    username = request.form['username']
    return redirect(url_for('user_links', username=username))

@app.route('/add_links/<username>', methods=['GET', 'POST'])
def user_links(username):
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    if username not in data:
        data[username] = []

    if request.method == 'POST':
        title = request.form['title']
        url = request.form['url']
        data[username].append((title, url))
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f)

    return render_template('links.html', username=username, links=data[username])

# صفحة التأكيد لرؤية الرابط المجمع
@app.route('/confirm_links/<username>', methods=['POST'])
def confirm_links(username):
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    bio_url = url_for('show_bio', username=username, _external=True)
    return render_template('bio.html', username=username, links=data[username], bio_url=bio_url)

# صفحة عرض البروفايل مع اللينكات
@app.route('/bio/<username>')
def show_bio(username):
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    user_links = data.get(username, [])
    bio_url = url_for('show_bio', username=username, _external=True)
    return render_template('bio.html', username=username, links=user_links, bio_url=bio_url)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
