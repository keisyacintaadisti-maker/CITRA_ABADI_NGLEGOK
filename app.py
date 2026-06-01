from flask import Flask, render_template, request, jsonify, send_from_directory
from database import init_db, save_review, get_all_reviews
import os

app = Flask(__name__, template_folder='templates', static_folder='assets')

# Inisialisasi database saat pertama run
init_db()

# ===== Static assets (CSS, JS, img) =====
@app.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory('assets', filename)

# ===== Halaman-halaman =====
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/contact')
def contact():
    reviews = get_all_reviews()
    return render_template('contact.html', reviews=reviews)

@app.route('/developer')
def developer():
    return render_template('developer.html')

# ===== API Ulasan =====
@app.route('/api/review', methods=['POST'])
def submit_review():
    data  = request.get_json()
    nama  = data.get('nama',  '').strip()
    email = data.get('email', '').strip()
    pesan = data.get('pesan', '').strip()

    if not nama or not email or not pesan:
        return jsonify({'success': False, 'message': 'Semua field harus diisi!'}), 400

    save_review(nama, email, pesan)
    return jsonify({'success': True, 'message': 'Ulasan berhasil dikirim, terima kasih!'})

@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    return jsonify(get_all_reviews())

if __name__ == '__main__':
    app.run(debug=True)
