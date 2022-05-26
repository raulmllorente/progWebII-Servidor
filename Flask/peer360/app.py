import os
import random
from flask import Flask, flash, request, redirect, url_for, render_template, make_response
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'xlsx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app) # class db extends app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database/user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

import json
with open('./configuration.json') as json_file:
    configuration = json.load(json_file)

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = configuration['gmail_username']
app.config['MAIL_PASSWORD'] = configuration['gmail_password']
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[360 peer grading] '
app.config['FLASKY_MAIL_SENDER'] = 'Raul Martinez'
mail = Mail(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15),unique=True)
    email = db.Column(db.String(50),unique=True)
    group = db.Column(db.String(80))

    def __repr__(self):
        return "<Name: {}> <Email: {}> <Group: {}>".format(self.name,self.email,self.group)

def send_email(to, subject, template, url, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])

    msg.body = render_template(template + '.txt', **kwargs, base_url=url)
    msg.html = render_template(template + '.html', **kwargs, base_url=url)
    mail.send(msg)

#import pandas as pd
@app.route('/')
def index():
    if request.cookies.get('filename'):
        return render_template('index.html',module="home",cookie=True)
    else:
        return render_template('index.html',module="home")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = "F"+''.join(random.choice('AILNOQVBCDEFGHJKMPRSTUXZabcdefghijklmnopqrstuvxz1234567890') for i in range(10))+".xlsx"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


            df_original = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            df_groups = pd.DataFrame({'groups':df_original["group"].unique()})
            df_groups = df_original.merge(df_groups, how='cross')
            df_groups = df_groups[df_groups.group != df_groups.groups].copy()
            df_360 = df_original[["email","group"]].copy()
            df_360.columns = ["email2","group2"]
            df_360 = df_original.merge(df_360, how='cross')
            df_360 = df_360[(df_360.group == df_360.group2)&(df_360.email!=df_360.email2)].copy()
            # Create a Pandas Excel writer using XlsxWriter as the engine.
            writer = pd.ExcelWriter(os.path.join(app.config['UPLOAD_FOLDER'], filename), engine='xlsxwriter')
            # Write each dataframe to a different worksheet.
            df_original.to_excel(writer, sheet_name='original')
            df_groups.to_excel(writer, sheet_name='group')
            df_360.to_excel(writer, sheet_name='360')
            # Close the Pandas Excel writer and output the Excel file.
            writer.save()

            response = make_response(redirect(url_for('uploaded_file',
                                    filename=filename)))
            response.set_cookie('filename', filename)
            return response
    return render_template('upload_file.html',module="upload_file",cookie=True)

import pandas as pd
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    df = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template('peer360.html',module="home",df_html=df.fillna('').to_html())

@app.route('/degree360')
def degree360():
    filename = request.cookies.get('filename')
    token= filename
    url = "{}/assess?type=degree360&token={}".format(configuration["base_url"], token)
    df = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return render_template('degree360.html',module="degree360",df_html=df.fillna('').to_html(),url=url)

@app.route('/peergrading')
def peergrading():
    filename = request.cookies.get('filename')
    token= filename
    url = "{}/assess?type=peergrading&token={}".format(configuration["base_url"], token)
    df = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template('peergrading.html',module="peergrading",df_html=df.fillna('').to_html(),url=url)


@app.route('/request_assessment/<type>')    #int has been used as a filter that only integer will be passed in the url otherwise it will give a 404 error
def request_assessment(type):
	filename = request.cookies.get('filename')
	df = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	for i in range(len(df)):
		token=generate_password_hash(str(df['name'].iloc(i))+filename,method="sha256")
		url = "http://localhost:5000/assess?type={}&email={}&filename={}&token={}".format(type, \
		df['email'].iloc[i],filename,token)
		send_email(str(df['email'].iloc[i]),'Please assess your colleagues.', \
		'mail/email_requesting_assessment',url=url)
	return "sucessfully sent request to all users!"


@app.route('/assess', methods=['GET','POST'])
def assess():
    if request.method == 'GET':
        return render_template("confirm_email.html",type_get=request.args.get('type'),token=request.args.get('token'))
    else:

        filename = request.form.get("token")
        if filename:
            df = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if (len(df[df["email"]==request.form.get("email")])>0): #Existe el correo
                name = str(df[df["email"]==request.form.get("email")]["name"].iloc[0])
                str_encoded = request.form.get("email")[1:2] + name[2:4] + request.form.get('token')[8:10]

                send_email(request.form.get("email"),'Please assess your colleagues.', 'mail/email_requesting_assessment',url=str_encoded)

                response = make_response(redirect(url_for('assessing',
                                        type_get=request.form.get("type_get"),
                                        token=request.form.get("token"),
                                        email=request.form.get("email"))))
                return response
            else:
                return "Wrong email!"
        else:
            return "Wrong url!"

@app.route('/assessing', methods=['GET','POST'])
def assessing():
    if request.method == 'GET':
        return render_template("confirm_pin.html",type_get=request.args.get('type'),token=request.args.get('token'), email=request.args.get('email'))
    else:
        filename = request.form.get("token")
        if filename:
            try:
                df = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                if (len(df[df["email"]==request.form.get("email")])>0): #Existe el correo
                    name = str(df[df["email"]==request.form.get("email")]["name"].iloc[0])
                    str_encoded = request.form.get("email")[1:2] + name[2:4] + request.form.get('token')[8:10]
                    if str_encoded == request.form.get("pin"):
                        return "ACCESO LIBERADO"
                    else:
                        return "ACCESS DENIED"
            except:
                return "Wrong url!"


@app.route('/setcookie')
def setcookie():
    mycookie = str(request.args.get('name'))
    response = make_response(redirect(url_for('index',
                            filename='yyy')))
    response.set_cookie('miprimeracookie', mycookie)
    return response

@app.route('/getcookie')
def getcookie():
    return request.cookies.get('miprimeracookie')