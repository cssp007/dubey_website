import os
#from flask_mail import Mail, Message
from flask import Flask, render_template, request, session, redirect, url_for, flash, g
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
import base64
import io
from werkzeug.utils import secure_filename
from functools import wraps
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Email, Length, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message

# Database connection
engine = create_engine("mysql+pymysql://root:Cssp#143@localhost/sports")
db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)

#Mail
mail= Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'pandey.somnath007@gmail.com'
app.config['MAIL_PASSWORD'] = 'pziwwihymvgnbqpw'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

app.config['SECRET_KEY'] = os.urandom(24)

'''
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(
        min=4, max=50)], render_kw={"placeholder": "Username"})
    password = PasswordField("Password", validators=[InputRequired(), Length(
        min=4)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

    def validate_username(self, username):
        username = db.query.filter_by(username=username.data).first()
        if not username:
            raise ValidationError('Account does not exist.')
'''


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/dbbat", methods=["GET", "POST"])
def dbbat():
    if request.method == "GET":
        posts = db.execute("SELECT * FROM bat")
        return render_template('dbbat.html', posts=posts)

@app.route("/dbball", methods=["GET", "POST"])
def dbball():
    if request.method == "GET":
        posts = db.execute("SELECT * FROM balls")
        return render_template('dbball.html', posts=posts)

@app.route("/gloves")
def gloves():
    return render_template('gloves.html')

@app.route("/pad")
def pad():
    return render_template('pad.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
       return render_template("login.html")

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        email = request.form.get("emailID")
        password = request.form.get("passwd")
        emaildata = db.execute("SELECT email FROM login WHERE email=:email", {"email": email}).fetchone()
        passworddata = db.execute("SELECT passwd FROM login WHERE email=:email", {"email": email}).fetchone()
        if emaildata is None:
            flash("No username", "danger")
            return render_template("login.html")
        else:
            for i in passworddata:
                if i == password:
                    session['email'] = email
                    return redirect(url_for('update'))
                else:
                    return render_template("index.html")

    return render_template('index.html', title='index')
"""
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('admin'))
"""

@app.route("/updateItem", methods=["GET", "POST"])
def updateItem():
    if request.method == "POST":
        itemID = request.form.get("itemID")
        item_type = request.form.get("item_type")
        itemDetials = request.form.get("itemDetials")
        itemPrice = request.form.get("itemPrice")
#        f = request.files['image']
#        f.save(os.path.join('static/image', secure_filename(f.filename)))
#        image = f.filename

        if item_type == 'bat':
            if itemDetials is None and itemPrice is None:
                return render_template('signup.html')
            elif itemDetials is None:
                db.execute(
                    "UPDATE bat SET price=:itemPrice WHERE serialNumber=:itemID;", {"itemID": itemID, "itemPrice":itemPrice})
                db.commit()
                db.close()
                return redirect(url_for('dbbat'))
            elif itemPrice is None:
                db.execute(
                    "UPDATE bat SET details=:itemDetials WHERE serialNumber=:itemID;", {"itemID": itemID, "itemDetials":itemDetials})
                db.commit()
                db.close()
                return redirect(url_for('dbbat'))
            else:
                db.execute(
                    "UPDATE bat SET details=:itemDetials, price=:itemPrice WHERE serialNumber=:itemID;", {"itemID": itemID, "itemPrice":itemPrice, "itemDetials":itemDetials})
                db.commit()
                db.close()
                return redirect(url_for('dbbat'))
    return render_template('signup.html')


@app.route("/deleteItem", methods=["GET", "POST"])
def deleteItem():
    if request.method == "POST":
        addnewitem = request.form.get("addnewitem")
        itemID = request.form.get("itemID")
        item_type = request.form.get("item_type")
        if item_type == 'bat':
            db.execute(
                "DELETE FROM bat WHERE serialNumber=:itemID", {"itemID": itemID})
            db.commit()
            db.close()
            return redirect(url_for('dbbat'))
        elif item_type == 'ball':
            db.execute(
                "DELETE FROM ball WHERE serialNumber=:itemID", {"itemID": itemID})
            db.commit()
            db.close()
            return redirect(url_for('dbball'))
        else:
            flash("Password is not match..!!", "danger")
            return render_template('signup.html')

    return render_template('signup.html')

@app.route("/addItem", methods=["GET", "POST"])
def addItem():
    if request.method == "POST":
        item_type = request.form.get("item_type")
        ballName = request.form.get("ballName")
        itemDetials = request.form.get("itemDetials")
        itemPrice = request.form.get("itemPrice")
        f = request.files['image']
        f.save(os.path.join('static/image', secure_filename(f.filename)))
        image = f.filename


        if item_type == 'bat':
            db.execute(
                "INSERT INTO bat(details,price,image) VALUES(:itemDetials,:itemPrice,:image)",
                {"itemDetials": itemDetials, "itemPrice": itemPrice, "image": image})
            db.commit()
            db.close()
            return redirect(url_for('dbbat'))
        elif item_type == 'ball':
            db.execute(
                "INSERT INTO balls(ball_name,details,price,image) VALUES(:ballName,:itemDetials,:itemPrice,:image)",
                {"ballName": ballName,"itemDetials": itemDetials, "itemPrice": itemPrice, "image": image})
            db.commit()
            db.close()
            return redirect(url_for('dbball'))
        else:
            flash("Password is not match..!!", "danger")
            return render_template('signup.html')

    return render_template('signup.html')


@app.route("/update")
#@login_required
def update():
    flash("This is a flashed message.")
    return render_template('update.html')

@app.route("/contact1")
def contact1():
    return render_template('contact1.html')


@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/sendMail", methods=["GET", "POST"])
def sendMail():
    if request.method == "POST":
        fullname = request.form.get("fullname")
        emailID = request.form.get("emailID")
        mobileNumber = request.form.get("mobileNumber")
        requirement = request.form.get("requirement")

        msg = Message('Customer requirement', sender = 'pandey.somnath007@gmail.com', recipients = ['pandey.somnath007@gmail.com'])
        msg.body = "Full Name" + str(fullname) + "Email ID:" + str(emailID) + "mobileNumber"
        mail.send(msg)
        flash('Thanks for sharing your details..!!')
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

#app.run(debug=True)

