from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from dotenv import load_dotenv
import os
import random

# Load .env variables (e.g. API key)
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Flask Setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemy Base & Init
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Cafe Table
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


# Routes

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random")
def get_random_cafe():
    cafes = db.session.execute(db.select(Cafe)).scalars().all()
    if not cafes:
        return jsonify(error={"Not Found": "No cafes in database."}), 404
    cafe = random.choice(cafes)
    return jsonify(cafe.to_dict())


@app.route("/all")
def get_all_cafes():
    cafes = db.session.execute(db.select(Cafe).order_by(Cafe.name)).scalars().all()
    return jsonify(cafes=[cafe.to_dict() for cafe in cafes])


@app.route("/find")
def find_cafe():
    location = request.args.get("loc")
    if not location:
        return jsonify(error={"Missing": "Location parameter 'loc' is required."}), 400
    cafes = db.session.execute(db.select(Cafe).where(Cafe.location == location)).scalars().all()
    if cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in cafes])
    else:
        return jsonify(error={"Not Found": "No cafe found at that location."}), 404


from sqlalchemy.exc import IntegrityError

@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    data = request.form if request.form else request.args

    required_fields = ["name", "map_url", "img_url", "loc", "seats"]
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        return jsonify(error={"Missing fields": missing}), 400

    new_cafe = Cafe(
        name=data.get("name"),
        map_url=data.get("map_url"),
        img_url=data.get("img_url"),
        location=data.get("loc"),
        seats=data.get("seats"),
        has_sockets=data.get("sockets") == "True",
        has_toilet=data.get("toilet") == "True",
        has_wifi=data.get("wifi") == "True",
        can_take_calls=data.get("calls") == "True",
        coffee_price=data.get("coffee_price"),
    )

    db.session.add(new_cafe)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify(error={"Conflict": "A cafe with that name already exists."}), 409

    return jsonify(response={"success": "Successfully added the new cafe."})



@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    new_price = request.args.get("new_price")
    if not new_price:
        return jsonify(error={"Missing": "Please provide new_price."}), 400

    cafe = db.session.get(Cafe, cafe_id)
    if cafe is None:
        return jsonify(error={"Not Found": "Cafe not found."}), 404

    cafe.coffee_price = new_price
    db.session.commit()
    return jsonify(response={"success": "Successfully updated the price."}), 200


@app.route("/delete/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api_key")
    if api_key != API_KEY:
        return jsonify(error={"Forbidden": "Invalid API Key."}), 403

    cafe = db.session.get(Cafe, cafe_id)
    if cafe is None:
        return jsonify(error={"Not Found": "Cafe not found."}), 404

    db.session.delete(cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully deleted the cafe."}), 200


# Run app
if __name__ == "__main__":
    app.run(debug=True)
