from flask import render_template
from flask_mail import Mail, Message
from app import app

mail = Mail(app)

def send_email(to, subject, template, url, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs, url=url)
    msg.html = render_template(template + '.html', **kwargs, url=url)
    #flash("send_email: {}".format(url))
    mail.send(msg)
