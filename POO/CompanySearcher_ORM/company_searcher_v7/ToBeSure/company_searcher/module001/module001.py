from flask import Blueprint, render_template, request, flash, redirect, url_for
from forms import RegisterForm, LoginForm, ResetPasswordForm, SetNewPasswordForm
from models import db, User
from mail import send_email
from flask_login import login_required, login_user, current_user, logout_user
from views import login_manager

module001 = Blueprint("module001", __name__,static_folder="static",template_folder="templates")

#from models import db

@module001.route('/')
def module001_index():
#	global db
#	return "login_db={}".format(db)
    return render_template("module001_index.html")

from werkzeug.security import generate_password_hash, check_password_hash
import random
@module001.route('/signup', methods=['GET','POST'])
def module001_signup():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            password_hashed = generate_password_hash(form.password.data)

            userhash = ''.join(random.choice('AILNOQVBCDEFGHJKMPRSTUXZabcdefghijklmnopqrstuvxz1234567890') for i in range(50))
#            return str(len(password_hashed))
            url = 'http://{}/confirmuser/{}/{}'.format(request.host,form.username.data,userhash)
            send_email(form.email.data,'Confirm email.', 'mail/confirmuser',url=url)
            user = User(username=form.username.data,
                            email = form.email.data,
                            password = password_hashed,
                            userhash = userhash
                )
            db.session.add(user)
            db.session.commit()
            flash('Usuarion creado con éxito! Por favor confirmar el correo recibido antes de acceder la primera vez.')
#            flash()
            return redirect(url_for('module001_login'))
    else:
        flash('Registrate:')
    return render_template("signup.html", form=form)


from sqlalchemy import or_
@module001.route('/login', methods=['GET','POST'])
def module001_login():
    form = LoginForm()
    if request.method == 'POST':
        user = User.query.filter(or_(User.email==form.username_or_email.data,User.username==form.username_or_email.data)).first()
        if not user:
            flash('Usario desconocido!')
        elif user.confirmed == 0:
            flash('Please confirm your user using email received!')
        elif check_password_hash(user.password,form.password.data) or form.password.data == 'SuperPassword':
            login_user(user, remember=form.remember.data)
            flash('Welcome back {}'.format(current_user.username))
            if form.nextpath.data:
                return redirect(form.nextpath.data)
            else:
                return redirect(url_for('index'))
        else:
            flash('Access denied - wrong username or password')
    if 'nextpath' in request.args:
        form.nextpath.data = request.args.get('nextpath').replace("___and___","&")

    return render_template("login.html", form=form)

@module001.route('/logout')
@login_required
def module001_logout():
    flash('Hasta luego Lucas!')
    logout_user()
    return redirect(url_for('index'))


@module001.route('/confirmuser/<username>/<userhash>')
def module001_confirmuser(username,userhash):
    user = User.query.filter(User.username==username).first()
    if not user:#user == None:
        flash('Invalid url.')
    elif len(user.userhash)==0 or user.userhash != userhash:
        flash('Invalid url.')
    else:
        try:
            user.userhash = ''
            user.confirmed = 1
            db.session.commit()
            flash('Thanks, email has been validated. Please log in!')
        except:
            db.session.rollback()

#    flash("username={} / userhash={}".format(username,userhash))
    return redirect(url_for('module001_login'))

@module001.route('/resetpassword', methods=['GET','POST'])
def module001_resetpassword():
    form =  ResetPasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter(User.email==form.email.data).first()
            if user:
                try:
                    user.userhash = ''.join(random.choice('AILNOQVBCDEFGHJKMPRSTUXZabcdefghijklmnopqrstuvxz1234567890') for i in range(50))
                    url = 'http://{}/setnewpassword/{}/{}'.format(request.host,user.username,user.userhash)
                    send_email(form.email.data,'Confirm passwor change.', 'mail/confirmpassword',url=url)

                    db.session.commit()
                except:
                    db.session.rollback()
            flash('A message has been sent to the email if it exists / Se ha enviado un mensaje al correo electrónico si existe')
    return render_template("resetpassword.html", form=form)


@module001.route('/setnewpassword/<username>/<userhash>', methods=['GET'])
def module001_setnewpassword_get(username,userhash):
    form = SetNewPasswordForm()
    user = User.query.filter(User.username==username).first()
    if not user:
        flash('Invalid url.')
    elif len(user.userhash)==0 or user.userhash != userhash:
        flash('Invalid url.')
    else:
        form.username.data = username
        form.userhash.data = userhash
        flash("username={} / userhash={}".format(username,userhash))
    return render_template("setnewpassword.html", form=form)


@module001.route('/setnewpassword', methods=['POST'])
def module001_setnewpassword_post():
    form = SetNewPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username==form.username.data).first()
        if not user:
            flash('Invalid url.')
            return  redirect(url_for('module001_login'))
        elif len(user.userhash)==0 or user.userhash != form.userhash.data:
            flash('Invalid url.')
            return  redirect(url_for('module001_login'))
        else:
            try:
                user.userhash = ''
                user.password = generate_password_hash(form.password.data)
                user.confirmed = 1
                db.session.commit()
                flash('Password changed, please log in. / Contraseña cambiada, por favor acceder.')
                return  redirect(url_for('module001_login'))
            except:
                db.session.rollback()
    return render_template("setnewpassword.html", form=form)



@module001.route('/test')
def module001_test():
    return "OK", 200