import sqlite3
import os
from datetime import datetime

# Path database
DB_PATH = os.path.join(os.path.dirname(__file__), 'citra_abadi.db')

def get_connection():
    """Buat koneksi ke SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # hasil query bisa diakses seperti dict
    return conn

def init_db():
    """Buat tabel-tabel yang dibutuhkan jika belum ada."""
    conn = get_connection()
    cursor = conn.cursor()

    # Tabel ulasan / review dari form kontak
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ulasan (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            nama      TEXT    NOT NULL,
            email     TEXT    NOT NULL,
            pesan     TEXT    NOT NULL,
            tanggal   TEXT    NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database siap: citra_abadi.db")

def save_review(nama: str, email: str, pesan: str):
    """Simpan ulasan baru ke database."""
    conn = get_connection()
    cursor = conn.cursor()
    tanggal = datetime.now().strftime('%d %B %Y, %H:%M')

    cursor.execute(
        'INSERT INTO ulasan (nama, email, pesan, tanggal) VALUES (?, ?, ?, ?)',
        (nama, email, pesan, tanggal)
    )
    conn.commit()
    conn.close()

def get_all_reviews():
    """Ambil semua ulasan, diurutkan dari terbaru."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ulasan ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()

    # Ubah ke list of dict agar mudah dipakai di template / JSON
    return [dict(row) for row in rows]
