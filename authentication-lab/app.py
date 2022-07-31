from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase




config = {

  "apiKey": "AIzaSyD_s6A5cLGMRZAzHBW4oaWY_zlrQNZ9mKI",

  "authDomain": "authentication-lab-e94aa.firebaseapp.com",

  "projectId": "authentication-lab-e94aa",

  "storageBucket": "authentication-lab-e94aa.appspot.com",

  "messagingSenderId": "472045575567",

  "appId": "1:472045575567:web:95a2c9e9cb62c2df7ffffa",

  "measurementId": "G-FMR35DC9HN",

  "databaseURL": ""

}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()



app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'




@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except: 
            error = "Authentication failed"
    return render_template('signin.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    error = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except: 
            error = "Authentication failed"

    return render_template('signup.html')


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None

    return redirect(url_for("signin"))



if __name__ == '__main__':
    app.run(debug=True)