from flask import Blueprint, render_template, request, jsonify
from forms import SearchForm
from flask_login import login_required
from models import Balancesheet
from views import login_manager

module002 = Blueprint("module002", __name__,static_folder="static",template_folder="templates")

#from models import db

@module002.route('/', methods=['GET','POST'])
@login_required
def module002_index():
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


@module002.route('/dashboard', methods=['GET','POST'])
@login_required
def module002_dashboard():
    return render_template("dashboard.html")

@module002.route('/to_json')
def module002_to_json():
    empresa = Balancesheet.query.filter(Balancesheet.nif_fical_number_id == request.args.get('nif')).first().as_dict()
    return jsonify(empresa)



@module002.route('/test')
def module002_test():
    return "OK", 200