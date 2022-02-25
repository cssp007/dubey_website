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



# Database connection
engine = create_engine("mysql+pymysql://root:Cssp#143@localhost/sports")
db = scoped_session(sessionmaker(bind=engine))


app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/bat")
def bat():
    return render_template('bat.html')

@app.route("/dbbat", methods=["GET", "POST"])
def dbbat():
    if request.method == "GET":
        posts = db.execute("SELECT * FROM bat")
        return render_template('dbbat.html', posts=posts)

@app.route("/dbball", methods=["GET", "POST"])
def dbball():
    if request.method == "GET":
        posts = db.execute("SELECT * FROM ball")
        return render_template('dbball.html', posts=posts)

@app.route("/ball")
def ball():
    return render_template('ball.html')

@app.route("/gloves")
def gloves():
    return render_template('gloves.html')

@app.route("/pad")
def pad():
    return render_template('pad.html')

@app.route("/processpost")
def processpost():
    return render_template('processpost.html')

@app.route("/iomemory")
def iomemory():
    return render_template('iomemory.html')

@app.route("/data60")
def data60():
    return render_template('data60.html')

@app.route("/data102")
def data102():
    return render_template('data102.html')

@app.route("/grack")
def grack():
    return render_template('grack.html')

@app.route("/post")
def post():
    return render_template('post.html')

@app.route("/sign_out")
def sign_out():
    return render_template('sign_out.html')

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
                    return redirect(url_for('update'))
                else:
                    return render_template("index.html")

    return render_template('index.html', title='index')


@app.route("/deleteItem", methods=["GET", "POST"])
def deleteItem():
    if request.method == "POST":
        addnewitem = request.form.get("addnewitem")
        itemID = request.form.get("itemID")
        db.execute(
            "DELETE FROM bat WHERE serialNumber=:itemID", {"itemID": itemID})
        db.commit()
        db.close()
        return redirect(url_for('login'))


@app.route("/addbat", methods=["GET", "POST"])
def addbat():
    if request.method == "POST":
        item_type = request.form.get("item_type")
        addnewitem = request.form.get("addnewitem")
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
                "INSERT INTO ball(details,price,image) VALUES(:itemDetials,:itemPrice,:image)",
                {"itemDetials": itemDetials, "itemPrice": itemPrice, "image": image})
            db.commit()
            db.close()
            return redirect(url_for('dbball'))
        else:
            flash("Password is not match..!!", "danger")
            return render_template('signup.html')

    return render_template('signup.html')


@app.route("/update")
def update():
    flash("This is a flashed message.")
    return render_template('update.html')

@app.route("/forgot")
def forgot():
    return render_template('sign_out.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
