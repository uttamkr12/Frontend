from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
app = Flask(__name__, template_folder='../templates',static_folder='../static')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/reg-login')
def reglogin():
    return render_template('reg_login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
if __name__=="__main__":
    app.run()