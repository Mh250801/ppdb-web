from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)

@app.route('/')
def index():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        alamat = request.form['alamat']
        username = request.form['username']
        password = request.form['password']

        # Simpan ke file.csv (data siswa)
        with open('file.csv', mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([nama, email, alamat])

        # Simpan ke file1.csv (akun)
        with open('file1.csv', mode='a', newline='', encoding='utf-8') as f1:
            writer = csv.writer(f1)
            writer.writerow([username, password])

        return redirect('/login')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            with open('file1.csv', mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row == [username, password]:
                        return f"<h2>Login berhasil! Selamat datang, {username}.</h2>"
        except FileNotFoundError:
            return "<h2>Data akun belum tersedia.</h2>"

        return "<h2>Login gagal! Username atau password salah.</h2>"
    
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
