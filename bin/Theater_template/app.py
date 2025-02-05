import os
from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

@app.route('/photos')
def photos():
    photo_folder = os.path.join(app.static_folder, 'photos')
    photos = [f'photos/{filename}' for filename in os.listdir(photo_folder)]
    return render_template('photos.html', photos=photos)

@app.route('/reviews')
def reviews():
    return render_template('reviews.html')

if __name__ == '__main__':
    app.run(debug=True)
