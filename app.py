from flask import Flask, render_template, request, redirect, url_for, session
import csv
import os

app = Flask(__name__)
app.secret_key = 'rahasia_muchlis'

USER_DATA_FILE = 'file.csv'
PASS_DATA_FILE = 'file1.csv'

# Fungsi bantu untuk menyimpan data
def simpan_data(file, data):
    with open(file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def baca_data(file):
    if not os.path.exists(file):
        return []
    with open(file, 'r') as f:
        reader = csv.reader(f)
        return list(reader)

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nama = request.form['nama']
        username = request.form['username']
        password = request.form['password']
        kelas = request.form['kelas']
        alamat = request.form['alamat']
        email = request.form['email']

        simpan_data(USER_DATA_FILE, [nama, username, kelas, alamat, email])
        simpan_data(PASS_DATA_FILE, [username, password])
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_input = request.form['username']
        password_input = request.form['password']
        users = baca_data(PASS_DATA_FILE)
        for user in users:
            if user[0] == username_input and user[1] == password_input:
                session['username'] = username_input
                return redirect(url_for('index'))
        return render_template('login.html', error='Username atau Password salah!')
    return render_template('login.html')

@app.route('/index')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    data = baca_data(USER_DATA_FILE)
    return render_template('index.html', data=data, username=session['username'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
