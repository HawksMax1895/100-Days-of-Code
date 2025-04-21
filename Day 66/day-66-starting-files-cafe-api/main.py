from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random


app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
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


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/random")
def get_random_cafe():
    all_cafes = db.session.execute(db.select(Cafe)).scalars().all()
    random_cafe = random.choice(all_cafes)
    return jsonify(
        can_take_calls=random_cafe.can_take_calls,
        coffee_price=random_cafe.coffee_price,
        has_sockets=random_cafe.has_sockets,
        has_toilet=random_cafe.has_toilet,
        has_wifi=random_cafe.has_wifi,
        id=random_cafe.id,
        img_url=random_cafe.img_url,
        location=random_cafe.location,
        name=random_cafe.name,
        seats=random_cafe.seats
    )

@app.route("/all")
def get_all_cafes():
    all_cafes = db.session.execute(db.select(Cafe).order_by(Cafe.name)).scalars().all()
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])


@app.route("/find")
def find_cafe():
    query_location = request.args.get("loc")
    all_cafes = db.session.execute(db.select(Cafe).where(Cafe.location == query_location)).scalars().all()
    if all_cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404

@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    data = request.form if request.method == "POST" else request.args

    new_cafe = Cafe(
        name=data.get("name"),
        map_url=data.get("map_url"),
        img_url=data.get("img_url"),
        location=data.get("loc"),
        has_sockets=data.get("sockets") == "True",
        has_toilet=data.get("toilet") == "True",
        has_wifi=data.get("wifi") == "True",
        can_take_calls=data.get("calls") == "True",
        seats=data.get("seats"),
        coffee_price=data.get("coffee_price"),
    )
    required_fields = ["name", "map_url", "img_url", "loc", "seats"]
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        return jsonify(error={"Missing fields": missing}), 400
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})

@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    new_price = request.args.get("new_price")
    if not new_price:
        return jsonify(error={"Missing": "Please provide a new_price."}), 400

    cafe = db.session.query(Cafe).get(cafe_id)
    if cafe is None:
        return jsonify(error={"Not Found": "Sorry, a cafe with that id was not found."}), 404

    cafe.coffee_price = new_price
    db.session.commit()
    return jsonify(response={"success": "Successfully updated the price."}), 200

@app.route("/delete/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api_key")
    if api_key != "TopSecretAPIKey":
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403

    cafe = db.session.query(Cafe).get(cafe_id)
    if cafe is None:
        return jsonify(error={"Not Found": "Sorry, a cafe with that id was not found."}), 404

    db.session.delete(cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200


if __name__ == '__main__':
    app.run(debug=True)
