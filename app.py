from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a random secret key for session management

DATA_FILE = 'links_data.json'
MESSAGES_FILE = 'messages.json'

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

if not os.path.exists(MESSAGES_FILE):
    with open(MESSAGES_FILE, 'w') as f:
        f.write('')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('user_links', username=session['username']))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_links', methods=['POST'])
def add_links():
    username = session.get('username')
    return redirect(url_for('user_links', username=username))

@app.route('/add_links/<username>', methods=['GET', 'POST'])
def user_links(username):
    if 'username' not in session or session['username'] != username:
        return redirect(url_for('login'))

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

    bio_url = f"https://{request.host}/bio/{username}"

    return render_template('links.html', username=username, links=data[username], bio_url=bio_url)

@app.route('/bio/<username>')
def show_bio(username):
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    user_links = data.get(username, [])
    return render_template('bio.html', username=username, links=user_links)

@app.route('/send_message/<username>', methods=['POST'])
def send_message(username):
    message = request.form['message']
    with open(MESSAGES_FILE, 'a') as f:
        json.dump({"to": username, "message": message}, f)
        f.write('\n')
    return redirect(url_for('show_bio', username=username))

@app.route('/view_messages/<username>')
def view_messages(username):
    messages = []
    with open(MESSAGES_FILE, 'r') as f:
        for line in f:
            msg = json.loads(line)
            if msg["to"] == username:
                messages.append(msg["message"])
    return render_template('messages.html', username=username, messages=messages)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
