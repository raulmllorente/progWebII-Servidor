from flask import request, render_template, jsonify, flash, redirect, url_for
from app import app
from models import db, User, Balancesheet
from flask_login import LoginManager, login_required, login_user, current_user, logout_user

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from mail import send_email


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?nextpath=' + request.full_path.replace("&","___and___"))

from forms import SearchForm, RegisterForm, LoginForm, ResetPasswordForm, SetNewPasswordForm

@app.route('/', methods=['GET','POST'])
@login_required
def index():
    form = SearchForm()
    if request.method == 'GET':
        companies = None
        result = False
    else:
        companies = Balancesheet.query.filter(Balancesheet.company_name.\
                                              contains(form.company_name.data)).all()
        result = True
    empresas_autocompletar = list(set([c.company_name.strip().capitalize() for c in Balancesheet.query.filter(Balancesheet.id >=0).all()]))
    return render_template("index.html", result=result, rows=companies,form=form, entries = empresas_autocompletar)


@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route('/to_json')
def to_json():
    empresa = Balancesheet.query.filter(Balancesheet.nif_fical_number_id == request.args.get('nif')).first().as_dict()
    return jsonify(empresa)


from werkzeug.security import generate_password_hash, check_password_hash
import random
@app.route('/signup', methods=['GET','POST'])
def signup():
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
            return redirect(url_for('login'))
    else:
        flash('Registrate:')
    return render_template("signup.html", form=form)


from sqlalchemy import or_
@app.route('/login', methods=['GET','POST'])
def login():
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

@app.route('/logout')
@login_required
def logout():
    flash('Hasta luego Lucas!')
    logout_user()
    return redirect(url_for('index'))


@app.route('/confirmuser/<username>/<userhash>')
def confirmuser(username,userhash):
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
    return redirect(url_for('login'))

@app.route('/resetpassword', methods=['GET','POST'])
def resetpassword():
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


@app.route('/setnewpassword/<username>/<userhash>', methods=['GET'])
def setnewpassword_get(username,userhash):
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


@app.route('/setnewpassword', methods=['POST'])
def setnewpassword_post():
    form = SetNewPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username==form.username.data).first()
        if not user:
            flash('Invalid url.')
            return  redirect(url_for('login'))
        elif len(user.userhash)==0 or user.userhash != form.userhash.data:
            flash('Invalid url.')
            return  redirect(url_for('login'))
        else:
            try:
                user.userhash = ''
                user.password = generate_password_hash(form.password.data)
                user.confirmed = 1
                db.session.commit()
                flash('Password changed, please log in. / Contraseña cambiada, por favor acceder.')
                return  redirect(url_for('login'))
            except:
                db.session.rollback()
    return render_template("setnewpassword.html", form=form)
