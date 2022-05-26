from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_login import LoginManager, login_required, login_user, current_user, logout_user, UserMixin
from flask_mail import Mail, Message

import json
with open('configuration.json') as json_file:
    configuration = json.load(json_file)

app = Flask(__name__)

app.config['SECRET_KEY'] = 'rf¡0jpetfgñksdjngoie6543tg9DWR5ERSDKFH09Rñçã3q4' # flask_wtf - CSRF
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database/company_balancesheet_database.db' # Sqlite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}?auth_plugin=mysql_native_password".format(
    username=configuration["MYSQL_USERNAME"],
    password=configuration["MYSQL_PASSWORD"],
    hostname=configuration["MYSQL_HOSTNAME"],
    databasename=configuration["MYSQL_DATABASENAME"]
    )

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = configuration["gmail_username"]
app.config['MAIL_PASSWORD'] = configuration["gmail_password"]
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Company searcher] '
app.config['FLASKY_MAIL_SENDER'] = 'Prof. Manoel Gadi'
mail = Mail(app)

def send_email(to, subject, template, url, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs, url=url)
    msg.html = render_template(template + '.html', **kwargs, url=url)
    #flash("send_email: {}".format(url))
    mail.send(msg)

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

class User(UserMixin,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique = True)
    email = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(200))
    confirmed = db.Column(db.Integer, default=0)
    userhash = db.Column(db.String(50))
    type_user = db.Column(db.Integer) # 1: admin, 2: usuario


class Balancesheet(db.Model):
    __tablename__ = 'cuentas_anuales'
    id = db.Column(db.Integer, primary_key=True)
    nif_fical_number_id = db.Column(db.String(9))
    company_name = db.Column(db.String(80))
    CNAE = db.Column(db.Integer)
    p10000_TotalAssets_h0 = db.Column(db.Float)
    p10000_TotalAssets_h1 = db.Column(db.Float)
    p10000_TotalAssets_h2 = db.Column(db.Float)
    p20000_OwnCapital_h0 = db.Column(db.Float)
    p20000_OwnCapital_h1 = db.Column(db.Float)
    p20000_OwnCapital_h2 = db.Column(db.Float)
    p31200_ShortTermDebt_h0 = db.Column(db.Float)
    p31200_ShortTermDebt_h1 = db.Column(db.Float)
    p31200_ShortTermDebt_h2 = db.Column(db.Float)
    p32300_LongTermDebt_h0 = db.Column(db.Float)
    p32300_LongTermDebt_h1 = db.Column(db.Float)
    p32300_LongTermDebt_h2 = db.Column(db.Float)
    p40100_40500_SalesTurnover_h0 = db.Column(db.Float)
    p40100_40500_SalesTurnover_h1 = db.Column(db.Float)
    p40100_40500_SalesTurnover_h2 = db.Column(db.Float)
    p40800_Amortization_h0 = db.Column(db.Float)
    p40800_Amortization_h1 = db.Column(db.Float)
    p40800_Amortization_h2 = db.Column(db.Float)
    p49100_Profit_h0 = db.Column(db.Float)
    p49100_Profit_h1 = db.Column(db.Float)
    p49100_Profit_h2 = db.Column(db.Float)
    detailed_status = db.Column(db.String(150))

    def as_dict(self):
        #return self.__dict__
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


from flask_bootstrap import Bootstrap
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'




from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, HiddenField#, SelectField,
from wtforms.validators import InputRequired, Length, Email,EqualTo

class SearchForm(FlaskForm):
    company_name = StringField('Entrar el nombre de la empresa que deseas buscar: ')

class RegisterForm(FlaskForm):
    username = StringField("User Name / Nombre de usuario", validators=[InputRequired(),Length(min=4,max=15)])
    email = StringField("E-mail", validators=[InputRequired(),Email(message="Email no es válido!"),Length(max=50)])
    password = PasswordField("Password / Contraseña ",
    validators=[InputRequired(), Length(min=4), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField("Confirm password / Confirmar contraseña ", validators=[InputRequired()])

class LoginForm(FlaskForm):
    username_or_email = StringField('Enter your username or your email / Entre su usuario o e-mail')
    password = PasswordField('Password / Contraseña', validators=[InputRequired(),Length(min=4,max=80)])
    nextpath = HiddenField('Next Path')
    remember = BooleanField('Remember Me / Recuérdame')

class ResetPasswordForm(FlaskForm):
    email = StringField("E-mail", validators=[InputRequired(),Email(message="Email no es válido!"),Length(max=50)])


class SetNewPasswordForm(FlaskForm):
    username = HiddenField('username')
    userhash = HiddenField('userhash')
    password = PasswordField("Password / Contraseña ",validators=[InputRequired(), Length(min=4), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField("Confirm password / Confirmar contraseña ", validators=[InputRequired()])


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?nextpath=' + request.full_path.replace("&","___and___"))



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

@app.errorhandler(500)
def internal_server_error(e):
    db.session.rollback()
    return render_template("500.html"), 500


@app.errorhandler(404)
def page_not_found(e):
    db.session.rollback()
    return render_template("404.html"), 404

@app.errorhandler(403)
def access_denied(e):
    db.session.rollback()
    return render_template("403.html"), 403










