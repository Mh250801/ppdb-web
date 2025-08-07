from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        no_hp = request.form['no_hp']
        alamat = request.form['alamat']
        gelombang = request.form['gelombang']
        username = request.form['username']
        password = request.form['password']

        # Simpan data ke file.csv
        with open('file.csv', mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([nama, email, no_hp, alamat, gelombang])

        # Simpan username dan password ke file1.csv
        with open('file1.csv', mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([username, password])

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        username_input = request.form['username']
        password_input = request.form['password']

        with open('file1.csv', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == username_input and row[1] == password_input:
                    return redirect(url_for('dashboard'))
            error = 'Username atau Password salah!'
    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

if __name__ == '__main__':
    # Buat file jika belum ada
    if not os.path.exists('file.csv'):
        with open('file.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Nama', 'Email', 'No HP', 'Alamat', 'Gelombang'])

    if not os.path.exists('file1.csv'):
        with open('file1.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Username', 'Password'])

    app.run(debug=True)
