from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = 'links_data.json'

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

@app.route('/')
def home():
    return render_template('index.html')

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

@app.route('/delete_link/<username>/<int:index>')
def delete_link(username, index):
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    if username in data and 0 <= index < len(data[username]):
        data[username].pop(index)

    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

    return redirect(url_for('user_links', username=username))

@app.route('/confirm_links/<username>', methods=['POST'])
def confirm_links(username):
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    # توليد الرابط الفريد للمستخدم مع اسم المستخدم في الرابط
    bio_url = f"https://{request.host}/bio/{username}"

    return render_template('links.html', username=username, links=data[username], bio_url=bio_url)

@app.route('/bio/<username>')
def show_bio(username):
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    user_links = data.get(username, [])
    return render_template('bio.html', username=username, links=user_links)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
