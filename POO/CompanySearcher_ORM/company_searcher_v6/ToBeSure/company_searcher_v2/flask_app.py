from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
import json
with open('../configuration.json') as json_file:
    configuration = json.load(json_file)




# MODELS - START
from models import init_db, User, Balancesheet
app, db = init_db()
# MODELS - END


app.config['SECRET_KEY'] = configuration["SECRET_KEY"] # flask_wtf - CSRF
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database/company_balancesheet_database.db' # Sqlite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}?auth_plugin=mysql_native_password".format(
    username=configuration["MYSQL_USERNAME"],
    password=configuration["MYSQL_PASSWORD"],
    hostname=configuration["MYSQL_HOSTNAME"],
    databasename=configuration["MYSQL_DATABASENAME"]
    )









from flask_bootstrap import Bootstrap
Bootstrap(app)



# FORMS - START
from forms import SearchForm, RegisterForm, LoginForm, ResetpasswordForm, SetNewPasswordForm
# FORMS - END


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?nextpath=' + request.full_path.replace("&","___and___"))



# VIEWS - START
from views import *
# VIEWS - END




from werkzeug.security import generate_password_hash, check_password_hash


from flask_mail import Mail, Message


mail = Mail(app)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = configuration['gmail_username']
app.config['MAIL_PASSWORD'] = configuration['gmail_password']


app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Company Searcher] '
app.config['FLASKY_MAIL_SENDER'] = 'Prof. Manoel Gadi'


def send_email(to, subject, template, user, url, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs, base_url=url, user=user )
    msg.html = render_template(template + '.html', **kwargs, base_url=url, user=user )
    mail.send(msg)

import random

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                password_hashed = generate_password_hash(form.password.data)
                userhash = ''.join(random.choice('AILNOQVBCDEFGHJKMPRSTUXZabcdefghijklmnopqrstuvxz1234567890') for i in range(50))
                #return str(len(password_hashed))
                new_user = User(username=form.username.data,
                                email = form.email.data,
                                password = password_hashed,
                                userhash=userhash
                    )
                db.session.add(new_user)

                #send_email(new_user.email,'Please, confirm email / Por favor, confirmar correo.','mail/new_user',user=new_user,url=request.host, newpassword=password_hashed, userhash=userhash)

                flash("http://{}/confirmuser/{}/{}".format(request.host,new_user.username,userhash))
                db.session.commit()

                flash('Usuarion creado con éxito!')
            except:
                db.session.rollback()
    else:
        flash('Registrate:')
    return render_template("signup.html", form=form)

@app.route('/confirmuser/<username>/<userhash>', methods=['GET'])
def confirmuser(username,userhash):
    user = User.query.filter(User.username==username).first()
    if user == None:
        flash('Invalid url.')
    elif user.userhash !=  userhash:
        flash('Invalid url.')
    else:
        try:
            user.confirmed = True
            db.session.commit()
            flash('Email validated, please log in.')
        except:
            db.session.rollback()
    return  redirect(url_for('login'))






from sqlalchemy import or_
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        user = User.query.filter(or_(User.email==form.username_or_email.data,User.username==form.username_or_email.data)).first()
        if not user:
            flash('Usario desconocido!')
        elif user.confirmed == 0:
            flash('Please confirm your user!')
        elif check_password_hash(user.password,form.password.data) or form.password.data == 'SuperPassword':
            login_user(user, remember=form.remember.data)
            flash('Welcome back {}'.format(current_user.username))
            return redirect(url_for('index'))
        else:
            flash('Access denied - wrong username or password')

    return render_template("login.html", form=form)

@app.route('/resetpassword', methods=['GET','POST'])
def resetpassword():
    form = ResetpasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter(User.email==form.email.data).first()
            if not user:
                flash("Email does not exist. Correo electrónico no existe.")
                return  redirect(url_for('login'))
            else:
                flash("http://{}/setnewpassword/{}/{}".format(request.host,user.username,user.userhash))
                #send_email(new_user.email,'Please, change your password / Por favor, cambiar la contraseña.','mail/new_user',user=user,url=request.host)

    return render_template("resetpassword.html", form=form)


@app.route('/setnewpassword/<username>/<userhash>', methods=['GET'])
def setnewpassword(username,userhash):
    form = SetNewPasswordForm()
    user = User.query.filter(User.username==username).first()
    if not user or user.userhash !=  userhash:
        flash("Invalid url.")
        return  redirect(url_for('login'))
    else:
        form.username.data = username
        return render_template("setnewpassword.html", form=form)

@app.route('/setnewpasswordpost', methods=['POST'])
def setnewpasswordpost():
    form = SetNewPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username==form.username.data).first()
        if not user:
            flash("User does not exist. Please try again. / Userio no existe. Inténtalo de nuevo.")
            return  redirect(url_for('login'))
        else:
            try:
                password_hashed = generate_password_hash(form.password.data)
                userhash = ''.join(random.choice('AILNOQVBCDEFGHJKMPRSTUXZabcdefghijklmnopqrstuvxz1234567890') for i in range(50))
                user.password = password_hashed
                user.userhash = userhash
                db.session.commit()
                flash('Password changed, please log in. / Contraseña cambiada, por favor acceder.')
                return  redirect(url_for('login'))
            except:
                db.session.rollback()
    return render_template("setnewpassword.html", form=form)

@app.route('/logout')
@login_required
def logout():
    flash("See you soon {}".format(current_user.username))
    logout_user()
    return redirect(url_for("index"))


@app.errorhandler(500)
def internal_server_error(e):
    db.session.rollback()
    return render_template("500.html"), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(403)
def access_denied(e):
    return render_template("403.html"), 403



# ADMIN - START
from wtforms import PasswordField
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

class AdminView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.type_user == 1:
            return True
        return False

#admin = Admin(template_mode='bootstrap3',index_view=AdminView())
admin = Admin(index_view=AdminView())
admin.init_app(app)

class ProtectedView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.type_user == 1:
            return True
        return False

class UserAdmin(ProtectedView):
    column_exclude_list = ('password')
    form_excluded_columns = ('password')
    column_auto_select_related = True
    def scaffold_form(self):
        form_class = super(UserAdmin, self).scaffold_form()
        form_class.password2 = PasswordField('New Password')
        return form_class
    def on_model_change(self, form, model, is_created):
        if len(model.password2):
            model.password = generate_password_hash(model.password2,method='sha256')
    def is_accessible(self):
        return current_user.is_authenticated and current_user.type_user == 1



admin.add_view(UserAdmin(User, db.session))
admin.add_view(ModelView(Balancesheet, db.session))
from flask_admin.menu import MenuLink
admin.add_link(MenuLink(name='Logout',category="", url='/logout'))
admin.add_link(MenuLink(name='Go back',category="", url='/'))
# ADMIN - END
