from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase



config = {
  

  'apiKey': "AIzaSyAVCMdA2KL1Bi5R5MiAy-T82OEW7CbtcgA",
  'authDomain': "clab-17389.firebaseapp.com",
  'projectId': "clab-17389",
  'storageBucket': "clab-17389.appspot.com",
  'messagingSenderId': "431047308597",
  'appId': "1:431047308597:web:56bf47769442331c07c87c",
  'measurementId': "G-DZ5BDQ5759",
  "databaseURL":"https://clab-17389-default-rtdb.europe-west1.firebasedatabase.ap"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db= firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
   error = ""
   if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
       except:
           error = "Authentication failed"
           return render_template("signin.html")
   else :
       return render_template("signin.html")




@app.route('/signup', methods=['GET', 'POST'])
def signup():
   error = ""
   if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user_dict =  {"password": request.form['password'],
              "email": request.form['email'],
              "full_name" : request.form['full_name'],
              "username" : request.form["username"] ,
              "bio" :request.form['bio']
              }
            db.child("Users").child(login_session['user']['localId']).set(user_dict)
            return redirect(url_for('add_tweet'))
       except:
           return render_template("signup.html", error = 'there is a previous on or a weak password')
   else:
    return render_template("signup.html")




  

@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method=='POST' :
     try:
      tweets = { 'title' : request.form['the_title'], 'textt': request.form['the_text'] , "uid" : login_session['user']['localId']}
      db.child("Tweet").push(tweets)
      return redirect(url_for ('alltweet'))
     except:
           print("Couldn't add article")
    return render_template("add_tweet.html")


@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return render_template("out.html")


@app.route('/alltweet')
def alltweet ():
    tweets=db.child('Tweet').get().val()
    return render_template('allthetweets.html', tweets = tweets)








              




   



   


if __name__ == '__main__':
    app.run(debug=True)