from flask import Flask, render_template, request, redirect
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

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']
    link = request.form['link']

    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    if username not in data:
        data[username] = []

    data[username].append(link)

    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

    return redirect(f'/bio/{username}')

@app.route('/bio/<username>')
def show_bio(username):
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    user_links = data.get(username, [])

    return render_template('bio.html', username=username, links=user_links)

if __name__ == '__main__':
    app.run(debug=True)

