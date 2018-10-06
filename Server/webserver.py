from flask import Flask, session, redirect, url_for, escape, request, render_template, jsonify, make_response

app = Flask(__name__)

app.secret_key = b'\xf9\xcc\x1b\xfc]\xd6\x87<\xc5\x18U\xc5KfM\xfa'

@app.route('/')
def index():
    if request.cookies.get('session'):
        return 'You are logged in as %s.' % escape(session['username'])
    return 'You have not logged in.'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username and password:
            session['username'] = request.form['username']
            response = make_response(jsonify('ok: true'))
            response.status = '200'
            response.headers['Content-Type'] = 'application/json'
            return response
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# @app.route('/user/')
# @app.route('/user/<name>')
# def user(name=None):
#     return render_template('user.html', name = name)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404