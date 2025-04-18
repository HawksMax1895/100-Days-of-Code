import csv
from importlib.metadata import pass_none

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField("Cafe Location on Google Maps (URL)", validators=[DataRequired(), URL()])
    open = StringField("Opening Time", validators=[DataRequired()])
    close = StringField("Closing Time", validators=[DataRequired()])
    coffee = SelectField('Coffee', choices=['✘', '☕️', '☕️☕️', '☕️☕️☕️', '☕️☕️☕️☕️', '☕️☕️☕️☕️☕️'],
                         validators=[DataRequired()])
    wifi = SelectField('Wifi', choices=['✘', '💪', '💪💪️', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪️'], validators=[DataRequired()])
    power = SelectField('Power', choices=['✘', '🔌', '🔌🔌', '🔌🔌🔌️', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'], validators=[DataRequired()])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        new_cafe = [
            form.cafe.data,
            form.location.data,
            form.open.data,
            form.close.data,
            form.coffee.data,
            form.wifi.data,
            form.power.data
        ]

        with open("cafe-data.csv", "rb+") as f:
            f.seek(-1, 2)  # go to last byte
            last_char = f.read(1)
            if last_char != b'\n':
                f.write(b'\n')

        with open("cafe-data.csv", mode="a", encoding='utf-8', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(new_cafe)
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
