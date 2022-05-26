# APP - START
from app import app
# APP - END

import json
with open('../configuration.json') as json_file:
    configuration = json.load(json_file)


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




from flask_bootstrap import Bootstrap
Bootstrap(app)


# VIEWS - START
from views import *

from module001.module001 import module001
from module002.module002 import module002
app.register_blueprint(module001, url_prefix="/module001") # Loggin
app.register_blueprint(module002, url_prefix="/module002") # Dashboard
# VIEWS - END


# ERRORS - START
from errors import *
# ERROS - END



# ADMIN - START
from admin import *
# ADMIN - END











