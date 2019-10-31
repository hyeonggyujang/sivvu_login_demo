from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from random import randint

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456789456123456789'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String(100), nullable=False)
    userPw = db.Column(db.String(100), nullable=False)
    userEmail = db.Column(db.String(500), nullable=False)
    fName = db.Column(db.String(100), nullable=True)
    lName = db.Column(db.String(100), nullable=True)

    def __init__(self, Id, Pw, Email):
        self.id = randint(0, 1000)
        self.userId = Id
        self.userPw = Pw
        self.userEmail = Email
        self.fName = 'null'
        self.lName = 'null'

    def __repr__(self):
        return f"User('{self.userId}', '{self.fName}', '{self.lName}')"


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
        if request.form.get('create_button') == 'create_user':
            Id = request.form("userId")
            Pw = request.form("userPw")
            Email = request.form("userEmail")
            user_input = User(Id, Pw, Email)

            try:
                db.session.add(user_input)
                db.session.commit()
                return redirect('/')

            except:
                return "THere is an issue in log in process!"
            
        elif request.form.get('login_button') == 'login_user':
            Id = request.form("existing_user")
            Pw = request.form("existing_pw")
            Email = ''
            user_input = User(Id, Pw, Email)

            try:
                db.session.add(user_input)
                db.session.commit()
                return redirect('/')

            except:
                return "THere is an issue in log in process!"
        
    else:
        return render_template('index.html')




if __name__ == '__main__':
    app.run(debug=True)