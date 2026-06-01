from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# buat database
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS contact (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT,
        pesan TEXT
    )
    ''')
    conn.close()

init_db()

# halaman utama
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/developer')
def developer():
    return render_template('developer.html')

# contact page + database
@app.route('/contact')
def contact():
    db = get_db()
    data = db.execute('SELECT * FROM contact').fetchall()
    db.close()
    return render_template('contact.html', data=data)

@app.route('/kirim', methods=['POST'])
def kirim():
    nama = request.form['nama']
    pesan = request.form['pesan']

    db = get_db()
    db.execute('INSERT INTO contact (nama, pesan) VALUES (?, ?)', (nama, pesan))
    db.commit()
    db.close()

    return redirect('/contact')

app.run(debug=True)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/product')
def product():
    return render_template('product.html')
