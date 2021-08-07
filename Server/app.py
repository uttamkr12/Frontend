from datetime import timedelta
from flask import Flask, render_template, url_for, request, session, redirect, flash
from flask_bootstrap import Bootstrap
from numpy.core.numeric import array_equal
from numpy.testing._private.utils import tempdir
from flask_pymongo import PyMongo
import bcrypt
import pickle
import numpy as np
#import sklearn
f = open('/home/itachi/Downloads/Project Documents/virtual/Final-year-project/ML-Model/model.pkl', 'rb')
g = open('/home/itachi/Downloads/Project Documents/virtual/Final-year-project/ML-Model/model1.pkl', 'rb')
model = pickle.load(f)
model1 = pickle.load(g)
app = Flask(__name__, template_folder='../templates',
            static_folder='../static')
app.config['MONGO_URI'] = 'mongodb+srv://uttam_kr12:JGr73uR1ZlrA9ryx@cluster0.34ucg.mongodb.net/Forecast'
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=10)
mongo = PyMongo(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/reg-login')
def reglogin():
    return render_template('reg_login.html')
#
# @app.route('/logged_in')
# def logged_in():
 #   if "email" in session:
  #      email = session["email"]
   #     return render_template('dashboard.html', email=email)
    # else:
    #   return redirect(url_for("reglogin"))
#
###############login route############################


@app.route('/login', methods=['POST', 'GET'])
def login():
    users = mongo.db.Users
    login_user = users.find_one({'email': request.form['email']})

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

@app.route('/pricedashboard')
def pricedashboard():
    return render_template('pricedashboard.html')

###############Logging out ###############


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return redirect(url_for('home'))
    else:
        return redirect(url_for('dashboard'))


@app.route("/predict", methods=["POST", "GET"])
def predict():

    if request.method == "POST":

        # print(request.form.values())

        state_dict = {'Andaman and Nicobar': 1, 'Andhra Pradesh': 2, 'Arunachal Pradesh': 3, 'Assam': 4, 'Bihar': 5, 'Chandigarh': 6, 'Chhattisgarh': 7, 'Dadra and Nagar Haveli': 8, 'Goa': 9, 'Gujarat': 10, 'Haryana': 11, 'Himachal Pradesh': 12, 'Jammu and Kashmir ': 13, 'Jharkhand': 14, 'Karnataka': 15,
                      'Kerala': 16, 'Madhya Pradesh': 17, 'Maharashtra': 18, 'Manipur': 19, 'Meghalaya': 20, 'Mizoram': 21, 'Nagaland': 22, 'Odisha': 23, 'Puducherry': 24, 'Punjab': 25, 'Rajasthan': 26, 'Sikkim': 27, 'Tamil Nadu': 28, 'Telangana ': 29, 'Tripura': 30, 'Uttarakhand': 31, 'Uttar Pradesh': 32, 'West Bengal': 33}
        ##states in dict. form##

        season_dict = {'Kharif': 1, 'Rabi': 2}
        ## season in dict. form##

        crop_dict = {'Rice': 1, 'Wheat': 2, 'Bajra': 3, 'Jowar': 4}
        ## crop in dict. form##

        state = state_dict.get(request.form.get("state"))
        # for value, key in state_dict.items():
        #     if state == key:
        #         state_key = value

        season = season_dict.get(request.form.get("season"))
        # for value, key in season_dict.items():
        #     if season == key:
        #         season_key = value

        crop = crop_dict.get(request.form.get("crop"))
        # for value, key in crop_dict.items():
        #     if crop == key:
        #         crop_key = value
        rainfall = request.form.get("rainfall")

        temp = request.form.get("temperature")

        area = request.form.get("area")
        # List of attributes
        user_input = [state, season, crop, rainfall, temp, area]
        print(user_input)
        prediction = model.predict([user_input])
        print(prediction)
        
        return render_template('dashboard.html',pred='prediction{}'.format(prediction))

@app.route("/pricepredict",methods = ["POST","GET"])
def pricepredict():

   if request.method == "POST":
       crop_dict = {'Rice': 1, 'Wheat': 2, 'Bajra': 3, 'Jowar': 4}
        
       crop = crop_dict.get(request.form.get("crop"))
       rainfall = request.form.get("rainfall")
       temp = request.form.get("temperature")

       month = request.form.get("month")
       print(crop,rainfall,temp,month)
       userinput = [crop,rainfall,temp,month]
       prediction = model1.predict([userinput])
       print (prediction)
       return render_template('pricedashboard.html',pred='prediction{}'.format(prediction))




if __name__ == "__main__":
    app.run(debug=True)
