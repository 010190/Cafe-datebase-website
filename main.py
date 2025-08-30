import flask_sqlalchemy
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text, MetaData, Table, insert, delete
from sqlalchemy.orm import DeclarativeBase
from flask_bootstrap import Bootstrap4
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, URL


app = Flask(__name__)
bootstrap = Bootstrap4(app)

engine = create_engine("sqlite:///cafes.db")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:/Users/olcza/Desktop/cafe_wifi_website/cafes.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Cafe = db.Table('cafe', db.metadata, autoload_with=engine)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

conn = engine.connect()

metadata = MetaData()

metadata.create_all(engine)




class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    map_url = StringField('map_url', validators=[DataRequired()])
    image_url = StringField('Image URL', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    socket =  SelectField('Socket', validators=[DataRequired()], choices= [bool(True),bool(False)])
    toilet = SelectField('Toilet    ', validators=[DataRequired()], choices= [bool(True),bool(False)])
    wifi = SelectField('WiFi', validators=[DataRequired()], choices= [bool(True),bool(False)])
    calls = SelectField('Can take calls', validators=[DataRequired()], choices= [bool(True),bool(False)])

    seats = StringField('Seats', validators=[DataRequired()])
    price =StringField('Price', validators=[DataRequired()])


    submit = SubmitField('Submit')


columns_names = [column.name for column in Cafe.c]
print(columns_names)
@app.route('/add',methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()

    with (app.app_context()):
        if form.validate_on_submit():

            cafe = form.cafe.data
            map_url = form.map_url.data
            image_url = form.image_url.data
            location = form.location.data
            socket = bool(form.socket.data)

            toilet = bool(form.toilet.data)
            wifi = bool(form.wifi.data)

            calls = bool(form.calls.data)
            seats = form.seats.data
            price = form.price.data

            value = {

                'name': cafe,
                'map_url': map_url,
                'img_url': image_url,
                'location': location,
                'has_sockets': socket,
                'has_toilet': toilet,
                'has_wifi': wifi,
                'can_take_calls': calls,
                'seats': seats,
                'coffee_price': price,
            }
            print(value)

            with engine.connect() as conn:

                query = db.insert(Cafe).values(value)
                conn.execute(query)

                conn.commit()
            with app.app_context():
                result = db.session.query(Cafe).all()
            for record in result:
                print(record)
            print("record added")

    return render_template('add.html', form=form)
@app.route('/',methods=['GET', 'POST'])
def index():
    attribute_list = ['id', 'name', 'map_url', 'img_url', 'location', 'sockets', 'toilet', 'wifi', 'can take calls',
                      'seats', 'coffee price']
    with app.app_context():
        result = db.session.query(Cafe).all()
    return render_template("index.html", cafes=result, attribute_list=attribute_list)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    with engine.connect() as conn:
        stmt = db.delete(Cafe).where(Cafe.c.id == id)
        conn.execute(stmt)
        conn.commit()
    print("deleted")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)