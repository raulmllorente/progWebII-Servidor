from app import app


from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from flask_login import UserMixin

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
        #return self.__dict__
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
