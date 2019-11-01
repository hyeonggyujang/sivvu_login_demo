from flask import Flask, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from random import randint

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456789456123456789'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(100), nullable=False)
    userPw = db.Column(db.String(100), nullable=False)
    userEmail = db.Column(db.String(500), nullable=True)
    f_Name = db.Column(db.String(100), nullable=True)
    l_Name = db.Column(db.String(100), nullable=True)

    def __init__(self, Id, Pw):
        self.id = randint(0, 1000)
        self.userName = Id
        self.userPw = Pw
        self.userEmail = 'null'
        self.f_Name = 'null'
        self.l_Name = 'null'

    def __repr__(self):
        return "User(%r, %s, %s %s)" % (self.id, self.userName, self.f_Name, self.l_Name)

    def add_email(self, Email):
        self.userEmail = Email

    def add_name(self, fName, lName):
        self.f_Name = fName
        self.l_Name = lName


@app.before_request
def make_session_permanent():
    """
    Makes a session permanent (month)
    """
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=31)

# @app.route("/")
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method =='POST':
        if request.form.get('register_button') == 'register':
            fName = str(request.form.get("fName"))
            lName = str(request.form.get("lName"))
            Email = str(request.form.get("userEmail"))
            Id = str(request.form.get("userId"))
            Pw1 = str(request.form.get("userPw1"))
            Pw2 = str(request.form.get("userPw2"))

            if Pw1 == Pw2:
                new_user = User(Id, Pw1)
                new_user.add_email(Email)
                new_user.add_name(fName, lName)

            else:
                flash( "Passwords don't match!" )

            try:
                db.session.add(new_user)
                db.session.commit()
                return "Registration Success!"

            except:
                return "There is an issue in the registration process!"
            
        elif request.form.get('login_button') == 'login':
            Id = str(request.form.get("loginId"))
            Pw = str(request.form.get("loginPw"))
            user_input = User(Id, Pw)

            try:
                if User.query.filter_by(userName=Id).first() == None:
                    return "No such user please register!"
                else:
                    if User.query.filter_by(userName=Id).first().userPw == Pw:
                        return "Login Success!"
                    else: 
                        return "Wrong Password!"

            except:
                return "There is an issue in the log in process!"
        
    else:
        return render_template('index.html')




if __name__ == '__main__':
    app.run(debug=True)