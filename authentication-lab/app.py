from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
from datetime import datetime




config = {

  "apiKey": "AIzaSyD_s6A5cLGMRZAzHBW4oaWY_zlrQNZ9mKI",

  "authDomain": "authentication-lab-e94aa.firebaseapp.com",

  "projectId": "authentication-lab-e94aa",

  "storageBucket": "authentication-lab-e94aa.appspot.com",

  "messagingSenderId": "472045575567",

  "appId": "1:472045575567:web:95a2c9e9cb62c2df7ffffa",

  "measurementId": "G-FMR35DC9HN",

  "databaseURL": "https://authentication-lab-e94aa-default-rtdb.europe-west1.firebasedatabase.app/"

}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()



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
        full_name = request.form['fullname']
        username = request.form['username']
        bio = request.form['bio']

        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {"fullname" : full_name, "username":username, "bio":bio}
            db.child("Users").child(login_session['user']['localId']).set(user)
            return redirect(url_for('add_tweet'))
        except: 
            error = "Authentication failed"

    return render_template('signup.html')


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        tweet = {"title":title, "text":text, "uid":login_session['user']['localId'], "timestamp":current_time, "likes":0}
        db.child("tweets").push(tweet)
        tweets = db.child("tweets").get().val()
        
        return all_tweets(tweets)
    return render_template("add_tweet.html")

@app.route('/like/<string:uid>')
def add_like(uid):
    updated = db.child('tweets').child(uid).get().val()
    print(updated)
    updated['likes']+= 1
    db.child('tweets').child(uid).update(updated)
    tweets = db.child('tweets').get().val()
    return all_tweets(tweets)
    
    


@app.route('/all_tweets')
def all_tweets(tweet):

    return render_template('all_tweets.html', tweet = tweet)

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None

    return redirect(url_for("signin"))



if __name__ == '__main__':
    app.run(debug=True, port = 5001)