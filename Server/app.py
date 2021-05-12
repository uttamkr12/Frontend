from datetime import timedelta
from flask import Flask, render_template, url_for, request, session, redirect, flash
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
import bcrypt
app = Flask(__name__, template_folder='../templates',static_folder='../static')
app.config['MONGO_URI'] = 'mongodb+srv://uttam_kr12:JGr73uR1ZlrA9ryx@cluster0.34ucg.mongodb.net/Forecast'
app.secret_key="hello"
app.permanent_session_lifetime=timedelta(minutes=10)
mongo = PyMongo(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/reg-login')
def reglogin():
    return render_template('reg_login.html')
#
#@app.route('/logged_in')
#def logged_in():
 #   if "email" in session:
  #      email = session["email"]
   #     return render_template('dashboard.html', email=email)
    #else:
     #   return redirect(url_for("reglogin"))
#
###############login route############################
@app.route('/login', methods=['POST','GET'])
def login():
    users = mongo.db.Users
    login_user = users.find_one({'email' : request.form['email']})

    if login_user:
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['email'] = request.form['email']
            return redirect(url_for('dashboard'))

    flash('Invalid email/password combination')
    return redirect(url_for('reglogin'))
    
#########################sign up route###############################
@app.route('/register', methods=['POST', 'GET'])
def register():
    if "email" in session:
        return redirect(url_for("dashboard"))
    if request.method == "POST":

        user = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        
        email_found = mongo.db.Users.find_one({"email": email})

        if email_found:
            message = 'This email already exists.'
            return render_template('reg_login.html', message=message)
        else:
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user_input = {'name': user, 'email': email, 'password': hashed}
            mongo.db.Users.insert_one(user_input)
            
            user_data = mongo.db.Users.find_one({"email": email})
            new_email = user_data['email']
   
            return render_template('reg_login.html', email=new_email)
    return render_template('reg_login.html')
############## Dashboard ##################
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

###############Logging out ###############
@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return redirect(url_for('home'))
    else:
        return redirect(url_for('dashboard'))




if __name__=="__main__":
    app.run(debug=True)