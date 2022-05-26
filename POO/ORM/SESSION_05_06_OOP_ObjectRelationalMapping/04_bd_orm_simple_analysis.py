# DECLARING THE OBJECT - Object-relational mapping
# / DECLARANDO EL OBJECTO - Object-relational mapping
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# EXTENDING THE Base OBJECT INTO AN OBJECT CALLED Balancesheet
# / EXTENDENDO EL OBJECTO Base EN UN OBJECTO LLAMADO Balancesheet
from sqlalchemy import Column, Integer, String, Float
class Balancesheet(Base):
    __tablename__ = 'cuentas_anuales'
    id = Column(Integer, primary_key=True)
    nif_fical_number_id = Column(String(9)) 
    company_name = Column(String(80))
    CNAE = Column(Integer)
    p10000_TotalAssets_h0 = Column(Float())
    p10000_TotalAssets_h1 = Column(Float())
    p10000_TotalAssets_h2 = Column(Float())
    p20000_OwnCapital_h0 = Column(Float())
    p20000_OwnCapital_h1 = Column(Float())
    p20000_OwnCapital_h2 = Column(Float())
    p31200_ShortTermDebt_h0 = Column(Float())
    p31200_ShortTermDebt_h1 = Column(Float())
    p31200_ShortTermDebt_h2 = Column(Float())
    p32300_LongTermDebt_h0 = Column(Float())
    p32300_LongTermDebt_h1 = Column(Float())
    p32300_LongTermDebt_h2 = Column(Float())
    p40100_40500_SalesTurnover_h0 = Column(Float())
    p40100_40500_SalesTurnover_h1 = Column(Float())
    p40100_40500_SalesTurnover_h2 = Column(Float())
    p40800_Amortization_h0 = Column(Float())
    p40800_Amortization_h1 = Column(Float())
    p40800_Amortization_h2 = Column(Float())
    p49100_Profit_h0 = Column(Float())
    p49100_Profit_h1 = Column(Float())
    p49100_Profit_h2 = Column(Float())



# CREATING A CONNECTION WITH THE DATABASE ENGINE, IT CAN BE ANY SQL Server, MySql, Posgres, etc...
# / CREANDO UNA CONEXIÓN CON EL MOTOR DE BASE DE DATOS, PUEDE SER CUALQUIERA SQL Server, MySql, Posgres, etc...
from sqlalchemy import create_engine
engine = create_engine('sqlite:///./company_balancesheet_database.db')


# WE CREATE A SESSION TO BE ABLE TO INSERT, UPDATE AND DELETE DATA.
# / CREAMOS UNA SESIÓN PARA PODER INSERTAR, ACTUALIZAR Y BORRAR DATOS.
from sqlalchemy.orm import sessionmaker
DBSession = sessionmaker(bind=engine)
session = DBSession()


company = session.query(Balancesheet).filter(Balancesheet.id == 1).first()
if company != None:
    print(company.company_name)
    print(company.p40100_40500_SalesTurnover_h0)
else:
    print("empresa no encontrada")


company = session.query(Balancesheet).filter(Balancesheet.nif_fical_number_id == 'B79031290').first()
if company != None:
    print(company.company_name)
    print(company.p40100_40500_SalesTurnover_h0)
else:
    print("empresa no encontrada")

company = session.query(Balancesheet).filter(Balancesheet.nif_fical_number_id == 'Xasdasd').first()
if company != None:
    print(company.company_name)
else:
    print("empresa no encontrada")

"""
SELECT * FROM cuentas_anuales WHERE CNAE = 1013;
"""
companies = session.query(Balancesheet).filter(Balancesheet.CNAE == 1013).all()

for company in companies:
    if company != None:
        print("Razón Social={}, ventas en 2017={}".format(company.company_name,
              company.p40100_40500_SalesTurnover_h0))
    else:
        print("empresa no encontrada")
    

"""
SELECT 
    SUM(p10000_TotalAssets_h0) AS SumTotalAssets,
    COUNT(p10000_TotalAssets_h0) AS NumOfItems,
    AVG(p10000_TotalAssets_h0) AS AverageAssets
FROM
    cuentas_anuales
GROUP BY
    CNAE;    
"""   
from sqlalchemy import func
# GROUP BY
rq = session.query(
    Balancesheet.CNAE,
    func.sum(Balancesheet.p10000_TotalAssets_h0).label('SumTotalAssets'),
    func.count(Balancesheet.p10000_TotalAssets_h0).label('NumOfItems'),
    func.avg(Balancesheet.p10000_TotalAssets_h0).label('AverageAssets')
).group_by(Balancesheet.CNAE).all()


print("CNAE={}; SUMA={}; #={}; PROMEDIO={}".format(rq[0][0],rq[0][1],rq[0][2],rq[0][3]))

for i in range(len(rq)):    
    print("CNAE={}; SUMA={}; #={}; PROMEDIO={}".format(rq[i][0],
          rq[i][1],
          rq[i][2],
          rq[i][3]))
