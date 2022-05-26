from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database/company_balancesheet_database.db'
app.config['SECRET_KEY'] = 'rf¡0jpetfgñksdjngoie6543tg9DWR5ERSDKFH09Rñçã3q4'

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

class Balancesheet(db.Model):
    __tablename__ = 'balance_sheet'
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
        return {'id':self.id,
                'nif_fical_number_id':self.nif_fical_number_id,
                'company_name':self.company_name,
                'CNAE':self.CNAE,
                'p10000_TotalAssets_h0':self.p10000_TotalAssets_h0,
                'p10000_TotalAssets_h1':self.p10000_TotalAssets_h1,
                'p10000_TotalAssets_h2':self.p10000_TotalAssets_h2,
                'p20000_OwnCapital_h0':self.p20000_OwnCapital_h0,
                'p20000_OwnCapital_h1':self.p20000_OwnCapital_h1,
                'p20000_OwnCapital_h2':self.p20000_OwnCapital_h2,
                'p31200_ShortTermDebt_h0':self.p31200_ShortTermDebt_h0,
                'p31200_ShortTermDebt_h1':self.p31200_ShortTermDebt_h1,
                'p31200_ShortTermDebt_h2':self.p31200_ShortTermDebt_h2,
                'p32300_LongTermDebt_h0':self.p32300_LongTermDebt_h0,
                'p32300_LongTermDebt_h1':self.p32300_LongTermDebt_h1,
                'p32300_LongTermDebt_h2':self.p32300_LongTermDebt_h2,
                'p40100_40500_SalesTurnover_h0':self.p40100_40500_SalesTurnover_h0,
                'p40100_40500_SalesTurnover_h1':self.p40100_40500_SalesTurnover_h1,
                'p40100_40500_SalesTurnover_h2':self.p40100_40500_SalesTurnover_h2,
                'p40800_Amortization_h0':self.p40800_Amortization_h0,
                'p40800_Amortization_h1':self.p40800_Amortization_h1,
                'p40800_Amortization_h2':self.p40800_Amortization_h2,
                'p49100_Profit_h0':self.p49100_Profit_h0,
                'p49100_Profit_h1':self.p49100_Profit_h1,
                'p49100_Profit_h2':self.p49100_Profit_h2,
                'detailed_status':self.detailed_status
            }

from flask_bootstrap import Bootstrap
Bootstrap(app)

from flask_wtf import FlaskForm
from wtforms import StringField #, PasswordField, BooleanField, SelectField, HiddenField
    
class SearchForm(FlaskForm):
    company_name = StringField('Entrar el nombre de la empresa que deseas buscar: ') 


@app.route('/', methods=['GET','POST'])
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
def to_json():
    empresa = Balancesheet.query.filter(Balancesheet.nif_fical_number_id == request.args.get('nif')).first().as_dict()
    return jsonify(empresa)


if __name__ == "__main__":
    app.run(debug=True)
    