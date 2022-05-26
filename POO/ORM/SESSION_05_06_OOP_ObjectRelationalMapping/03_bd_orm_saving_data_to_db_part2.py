import pandas as pd
df = pd.read_excel("TurnOverEstimation.xlsx")
df = df.fillna(0)

# #CREATING A CONNECTION WITH THE DATABASE ENGINE, IT CAN BE ANY SQL Server, MySql, Posgres, etc...
# / CREANDO UNA CONEXIÓN CON EL MOTOR DE BASE DE DATOS, PUEDE SER CUALQUIERA SQL Server, MySql, Posgres, etc...
from sqlalchemy import create_engine
engine = create_engine('sqlite:///./company_balancesheet_database.db')

# DECLARING THE OBJECT - Object-relational mapping
# / DECLARANDO EL OBJECTO - Object-relational mapping
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# EXTENDING THE Base OBJECT INTO AN OBJECT CALLED User
# / EXTENDENDO EL OBJECTO Base EN UN OBJECTO LLAMADO User
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
    detailed_status = Column(String(150))



# WE RUN create_all SO THAT IF THE TABLE DOES NOT EXIST IT CREATES IT
# / EJECUTAMOS create_all PARA QUE SI LA TABLA NO EXISTE LA CREE
Base.metadata.create_all(engine)

# WE CREATE A SESSION TO BE ABLE TO INSERT, UPDATE AND DELETE DATA.
# / CREAMOS UNA SESIÓN PARA PODER INSERTAR, ACTUALIZAR Y BORRAR DATOS.
from sqlalchemy.orm import sessionmaker
DBSession = sessionmaker(bind=engine)
session = DBSession()



df.columns
for i in range(0,5): #range(len(df)):
    print(i, df['CNAE'].iloc[i], df['company_name'].iloc[i], df['nif_fical_number_id'].iloc[i])


# INSERTING 1000 USERS EACH TIME
# / INSERTAR 1000 USUARIOS CADA VEZ 
for i in range(len(df)):
    company = Balancesheet(nif_fical_number_id=df['nif_fical_number_id'].iloc[i],
                           company_name=df['company_name'].iloc[i],
                           CNAE=int(df['CNAE'].iloc[i]),
                           p10000_TotalAssets_h0=df['p10000_TotalAssets_h0'].iloc[i],
                           p10000_TotalAssets_h1=df['p10000_TotalAssets_h1'].iloc[i],
                           p10000_TotalAssets_h2=df['p10000_TotalAssets_h2'].iloc[i],
                           p20000_OwnCapital_h0=df['p20000_OwnCapital_h0'].iloc[i],
                           p20000_OwnCapital_h1=df['p20000_OwnCapital_h1'].iloc[i],
                           p20000_OwnCapital_h2=df['p20000_OwnCapital_h2'].iloc[i],
                           p31200_ShortTermDebt_h0=df['p31200_ShortTermDebt_h0'].iloc[i],
                           p31200_ShortTermDebt_h1=df['p31200_ShortTermDebt_h1'].iloc[i],
                           p31200_ShortTermDebt_h2=df['p31200_ShortTermDebt_h2'].iloc[i],
                           p32300_LongTermDebt_h0=df['p32300_LongTermDebt_h0'].iloc[i],
                           p32300_LongTermDebt_h1=df['p32300_LongTermDebt_h1'].iloc[i],
                           p32300_LongTermDebt_h2=df['p32300_LongTermDebt_h2'].iloc[i],
                           p40100_40500_SalesTurnover_h0=df['p40100_40500_SalesTurnover_h0'].iloc[i],
                           p40100_40500_SalesTurnover_h1=df['p40100_40500_SalesTurnover_h1'].iloc[i],
                           p40100_40500_SalesTurnover_h2=df['p40100_40500_SalesTurnover_h2'].iloc[i],
                           p40800_Amortization_h0=df['p40800_Amortization_h0'].iloc[i],
                           p40800_Amortization_h1=df['p40800_Amortization_h1'].iloc[i],
                           p40800_Amortization_h2=df['p40800_Amortization_h2'].iloc[i],
                           p49100_Profit_h0=df['p49100_Profit_h0'].iloc[i],
                           p49100_Profit_h1=df['p49100_Profit_h1'].iloc[i],
                           p49100_Profit_h2=df['p49100_Profit_h2'].iloc[i],
                           detailed_status=df['detailed_status'].iloc[i])
    session.add(company)
#    session.commit()
#    print("insertada fila",i)    
    if ( i % 1000 == 0):
        print ("inserting 1000 companies - i = {} - name last company inserted = {}".format(i,df['company_name'].iloc[i]))
        session.commit()

session.commit()



    