from flask import Flask, redirect, url_for, render_template, request, session, flash, g
from datetime import timedelta, datetime

from flask.signals import Namespace
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "weAreCoolest"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=7)

db = SQLAlchemy(app)

@app.before_request
def before_request():
    g.user = None
    if 'name' in session:
        # user = [x for x in users if x.id == session['user_id']][0]
        # print(session['user_id'])
        user = User.query.filter_by(username = session['name']).first()
        g.user = user

class User(db.Model):
    id = db.Column("id", db.Integer, primary_key= True)
    username = db.Column("username", db.String(100))
    password = db.Column("password", db.String(100))

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
    def __repr__(self):
        return self.username

#users = []
#users.append(User(id=1, username='Tyler', password="iscoolest"))
#users.append(User(id=2, username='Fiona', password="iscool"))
#users.append(User(id=3, username='Sharon', password="issomewhatcool"))



@app.route("/")
@app.route('/home')
def home():
    return render_template("index.html")
    
@app.route("/profile")
def profile():
    if "name" in session:
        user = User.query.filter_by(username=session['name']).first()
        return render_template('profile.html', content=user.username, id=user.id)
    flash("You must login first!")
    return redirect(url_for("login"))

@app.route("/activity")
def activity():
    return render_template("activity.html")

@app.route("/Meditation")
def meditation():
    return render_template("Meditation.html")

@app.route("/Journal")
def journal():
    return render_template("Journal.html")

@app.route("/Walk")
def walk():
    return render_template("Walk.html")

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        username = request.form["username"]
        password = request.form["password"]

        #db 
        # user = [x for x in users if x.username == username][0]
        user = User.query.filter_by(username=username).first()
        print(user)
        #print(user)
        #print(user[0])
        if user and user.password == password:
            session['name'] = user.username
            flash("Login Successful!")
            return redirect(url_for('profile'))
        else:
            flash("Login Unsuccessful :(")
            return redirect(url_for("login"))
    else: 
        if "name" in session:        
            flash("Already Logged In!")
            return redirect(url_for("home"))
        return render_template("login.html")

@app.route("/create", methods=["POST","GET"])
def create():
    
    if request.method == "POST":
        newusername = request.form["newusername"]
        newpassword = request.form["newpassword"]
        found_user = User.query.filter_by(username=newusername).first()
        
        if found_user:
            flash("That username is already taken!")
            return render_template("create.html")
        else:
            
            flash("Congrats! You have created a new account.")
            usr = User(len(User.query.all())+1, newusername, newpassword) #temp setting id = 0 for all but have to fix later
            db.session.add(usr)
            db.session.commit()
            return redirect(url_for("profile"))
    else:
        return render_template("create.html")

@app.route("/Questions", methods=["POST", "GET"])
def questions():
    return render_template("questions.html")


@app.route("/view")
def view():
    return render_template("view.html", values=User.query.all())
    

@app.route("/logout")
def logout():
    flash("You have been logged out!", "info")
    session.pop("name", None)
    #session.pop("email", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)