import os

import dotenv
import requests
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

dotenv.load_dotenv()
TMDB_API_KEY = os.environ.get("TMDB_API_KEY")
TMDB_READ_ACCESS_TOKEN = os.environ.get("TMDB_READ_ACCESS_TOKEN")

TMDB_API_URL = "https://api.themoviedb.org/3/search/movie"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {TMDB_READ_ACCESS_TOKEN}"
}

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


# CREATE DB
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
db.init_app(app)


# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True)
    year: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String(500))
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250))


'''
new_movie = Movie(
    title="Phone Booth",
    year=2002,
    description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
    rating=7.3,
    ranking=10,
    review="My favourite character was the caller.",
    img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
)

second_movie = Movie(
    title="Avatar The Way of Water",
    year=2022,
    description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
    rating=7.3,
    ranking=9,
    review="I liked the water.",
    img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
)
'''

with app.app_context():
    db.create_all()

    # db.session.add(new_movie)
    # db.session.add(second_movie)
    # db.session.commit()


class EditForm(FlaskForm):
    rating = StringField("Your Rating Out of 10 e.g. 7.5")
    review = StringField("Your Review")
    submit = SubmitField("Done")


class AddForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")


@app.route("/")
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.rating))
    movies = result.scalars().all()
    for i in range(len(movies)):
        movies[i].ranking = len(movies) - i
    return render_template("index.html", movies=movies)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    form = EditForm()
    id = request.args.get("id")
    movie = db.get_or_404(Movie, id)
    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", movie=movie, form=form)


@app.route("/delete")
def delete():
    id = request.args.get("id")
    movie = db.get_or_404(Movie, id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddForm()
    if form.validate_on_submit():
        params = {
            "query": form.title.data
        }
        response = requests.get(TMDB_API_URL, params=params, headers=headers).json()["results"]
        return render_template("select.html", options=response)
    return render_template("add.html", form=form)


@app.route("/find", methods=["GET", "POST"])
def find_movie():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        api_url = f"https://api.themoviedb.org/3/movie/{movie_api_id}"
        response = requests.get(api_url, headers=headers).json()
        print(response)
        new_movie = Movie(
            title=response["title"],
            year=response["release_date"].split("-")[0],
            description=response["overview"],
            img_url=f"https://image.tmdb.org/t/p/original/{response['poster_path']}",
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('edit', id=new_movie.id))


if __name__ == '__main__':
    app.run(debug=True)
