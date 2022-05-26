from flask import request, render_template, jsonify
from models import app, Balancesheet
from flask_login import login_required
from forms import SearchForm

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

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

@app.route('/to_json')
@login_required
def to_json():
    empresa = Balancesheet.query.filter(Balancesheet.nif_fical_number_id == request.args.get('nif')).first().as_dict()
    return jsonify(empresa)