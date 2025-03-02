from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def setpassword(self, password):
        self.password = generate_password_hash(password)

    def checkpassword(self, password):
        return check_password_hash(self.password, password)


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')  # This renders the index page


# LOGIN
@app.route('/login', methods=['GET','POST'])  # Handling both GET and POST for login
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.checkpassword(password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else: # Debugging log
            return render_template('index.html')  # Renders the login page when accessed with GET
# DASHBOARD



# REGISTER
@app.route('/register', methods=['GET', 'POST'])  # Handling both GET and POST for register
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template('index.html',error="User already here!")  # Renders the register page when accessed with GET
        else:
            new_user = User(username=username)
            new_user.setpassword(password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('dashboard'))
# LOGOUT



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
