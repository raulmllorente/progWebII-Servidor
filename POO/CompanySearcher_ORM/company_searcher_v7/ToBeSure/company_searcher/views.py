from flask import request, render_template, jsonify, redirect, url_for
from app import app
from models import db, User, Balancesheet
from flask_login import LoginManager, login_required, login_user, current_user, logout_user

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?nextpath=' + request.full_path.replace("&","___and___"))


@app.route('/', methods=['GET','POST'])
def index():
    return redirect(url_for('module002.module002_index'))



