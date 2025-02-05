from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
import string
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shortlinks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class ShortLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2048), nullable=False)
    short_id = db.Column(db.String(6), unique=True, nullable=False)
    clicks = db.Column(db.Integer, default=0)

def generate_short_id():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=6))

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('original_url')

    if not original_url:
        return jsonify({"error": "Missing 'original_url' in request"}), 400

    existing_link = ShortLink.query.filter_by(original_url=original_url).first()
    if existing_link:
        short_url = request.host_url + existing_link.short_id
        return jsonify({"original_url": original_url, "short_url": short_url})

    short_id = generate_short_id()
    while ShortLink.query.filter_by(short_id=short_id).first():
        short_id = generate_short_id()

    new_link = ShortLink(original_url=original_url, short_id=short_id)
    db.session.add(new_link)
    db.session.commit()

    short_url = request.host_url + short_id
    return jsonify({"original_url": original_url, "short_url": short_url})

@app.route('/<short_id>', methods=['GET'])
def redirect_to_original(short_id):
    link = ShortLink.query.filter_by(short_id=short_id).first()

    if link is None:
        return jsonify({"error": "Short URL not found"}), 404

    link.clicks += 1
    db.session.commit()

    return redirect(link.original_url)

@app.route('/stats/<short_id>', methods=['GET'])
def get_stats(short_id):
    link = ShortLink.query.filter_by(short_id=short_id).first()
    if link is None:
        print(f"DEBUG: No link found for short_id={short_id}")  # Лог для проверки
        return jsonify({"error": "Short URL not found"}), 404

    print(f"DEBUG: Found link {link.original_url} with {link.clicks} clicks")  # Лог результата
    return jsonify({
        "original_url": link.original_url,
        "short_id": link.short_id,
        "clicks": link.clicks
    })


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
