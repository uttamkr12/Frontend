from flask import Flask, render_template, url_for, request, session, redirect
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
import bcrypt
import json
app = Flask(__name__, template_folder='../templates',static_folder='../static')
app.config['MONGO_URI'] = 'mongodb+srv://uttam_kr12:JGr73uR1ZlrA9ryx@cluster0.34ucg.mongodb.net/Forecast'

mongo = PyMongo(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/reg-login')
def reglogin():
    return render_template('reg_login.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['email']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['email'] = request.form['email']
            return redirect(url_for('dashboard'))

    return 'Invalid email/password combination'

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
   
            return render_template('dashboard.html', email=new_email)
    return render_template('reg_login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
if __name__=="__main__":
    app.run()