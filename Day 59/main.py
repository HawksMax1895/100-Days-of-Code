import requests
from flask import Flask, render_template

BLOG_API_URL = "https://api.npoint.io/4cedc647e52fc72c2543"

app = Flask(__name__)

posts = requests.get(BLOG_API_URL).json()


@app.route("/")
def home():
    return render_template('index.html', all_posts=posts)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/post/<int:id>")
def show_post(id):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == id:
            requested_post = blog_post
    return render_template('post.html', post=requested_post)


if __name__ == "__main__":
    app.run(debug=True)
