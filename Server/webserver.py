from flask import Flask
from flask import Flask
from flask import session
from flask import redirect
from flask import url_for
from flask import escape
from flask import request
from flask import render_template
from flask import jsonify
from flask import make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Admin:Admin@localhost:3306/mycar'
db = SQLAlchemy(app)

app.secret_key = b'\xf9\xcc\x1b\xfc]\xd6\x87<\xc5\x18U\xc5KfM\xfa'

class Users(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), unique=True)
    Password = db.Column(db.String(80), unique=False)

    def __init__(self, username, password):
        self.Username = username
        self.Password = password

    def __repr__(self):
        return '<Users %r>' % self.Username

@app.route('/')
def index():
    if request.cookies.get('session'):
        return 'You are logged in as %s.' % escape(session['user_id'])
    return 'You are not logged in.'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        dbDataUser = db.session.query(Users).filter(Username = username, Password = password).first()
        if dbDataUser:
            session['user_id'] = str(dbDataUser.ID)
            response = make_response(jsonify('id: %s' % str(dbDataUser.ID)))
            response.status = '200'
            response.headers['Content-Type'] = 'application/json'
            return response
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

# @app.route('/user/')
# @app.route('/user/<name>')
# def user(name=None):
#     return render_template('user.html', name = name)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404