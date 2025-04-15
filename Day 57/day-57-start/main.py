from flask import Flask, render_template
import random
from datetime import datetime
import requests

app = Flask(__name__)
AGIFY_URL = "https://api.agify.io"
GENDERIZE_URL = "https://api.genderize.io"
BLOG_URL = "https://api.npoint.io/c790b4d5cab58020d391"

@app.route('/')
def home():
    random_number = random.randint(1, 10)
    year = datetime.now().year
    return render_template("index.html", random_number=random_number, year=year, name="Max Radmacher")

@app.route('/guess/<name>')
def guess(name):
    gender = requests.get(url=GENDERIZE_URL, params={'name': name}).json()['gender']
    age = requests.get(url=AGIFY_URL, params={'name': name}).json()['age']
    return render_template('guess.html', name=name.capitalize(), gender = gender, age = age)

@app.route('/blog/<int:num>')
def get_blog(num):
    print(num)
    blogs = requests.get(url=BLOG_URL).json()
    return render_template('blog.html', posts=blogs)

if __name__ == "__main__":
    app.run(debug=True)


