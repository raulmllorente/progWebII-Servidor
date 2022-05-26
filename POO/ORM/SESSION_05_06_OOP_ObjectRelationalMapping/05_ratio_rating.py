import sqlite3
conn = sqlite3.connect('./company_balancesheet_database.db')

# pd.read_csv("fichero.csv")
# pd.read_excel("fichero.xlsx")
# pd.read_json("fichero.json")

import pandas as pd
df = pd.read_sql("""
 SELECT *
    FROM cuentas_anuales
    WHERE id < 10
""", conn)

df['company_name']

import pandas as pd
df = pd.read_sql("""
    SELECT 
        CNAE,    
        SUM(p10000_TotalAssets_h0) as SUMA,
        COUNT(p10000_TotalAssets_h0) as CANTIDAD,
        AVG(p10000_TotalAssets_h0) as PROMEDIO
    FROM 
        cuentas_anuales
    GROUP BY
        CNAE
""", conn)

print(df.head())

df[['CNAE','SUMA']].head()


import pandas as pd
df = pd.read_sql("""
 SELECT *
    FROM cuentas_anuales
""", conn)

df['detailed_status'].head()
df['detailed_status'].value_counts()

df['target_status'] = [0 if item in ['Activa', '0', 0] else 1 for item in df['detailed_status']] # 0 si Activa, 1 si algo raro!

# _h0, _h1, _h2
# _h0: history 0, here h0 means the year 2017 (historia 0, aquí h0 significa el año 2017)
# _h1: history -1, here h1 means the year 2016 (historia -1, aquí h1 significa el año 2016)
# _h2: history -2, here h2 means the year 2015 (historia -2, aquí h2 significa el año 2015)

# Ebita Margin - Ebitda / Turn over (Ventas)
# p49100: Profit (Resultado del ejercicio)
# p40800: Amortization (Amortización) 
# p40100: Sales Turnover (Ingresos de Explotación)
# p40500: Other sales (Otros Ingresos)
df['ebitda_income'] = (df.p49100_Profit_h1-df.p40800_Amortization_h1)/(df.p40100_40500_SalesTurnover_h1) 
df[['company_name','ebitda_income']].head(5)

# Total Debt / Ebita 
# p31200: Short Term Debt / Deuda a corto plazo
# p32300: Long Term Debt / Deuda a largo plazo
# p49100: Profit (Resultado del ejercicio)
# p40800: Amortization (Amortización) 
df['debt_ebitda'] =(df.p31200_ShortTermDebt_h1 + df.p32300_LongTermDebt_h1) /(df.p49100_Profit_h1-df.p40800_Amortization_h1) 
df[['company_name','debt_ebitda']].head(5)

# rraa_rrpp: Financial leveraging / apalancamiento financiero 
# p10000: Total Assets / Total activos
# p20000: Own Capital / Patrimonio neto
df['rraa_rrpp'] = (df.p10000_TotalAssets_h1 - df.p20000_OwnCapital_h1) /df.p20000_OwnCapital_h1
df[['company_name','rraa_rrpp']].head(5)

# Log of Operating Income
import numpy as np
df['log_operating_income'] = np.log(df.p40100_40500_SalesTurnover_h1)
df[['company_name','log_operating_income']].head(5)

df = df.fillna(0).replace(np.inf, 0).replace(-np.inf, 0)
df

from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(random_state=1234)

df_clean = df[['ebitda_income','debt_ebitda','rraa_rrpp','log_operating_income','target_status']].replace([np.inf, -np.inf], np.nan).dropna()
X = df_clean[['ebitda_income','debt_ebitda','rraa_rrpp','log_operating_income']]
y = df_clean['target_status']

X.head()
y.head()

fitted_model = model.fit(X, y)

y_pred = fitted_model.predict(X)
y_pred_proba = fitted_model.predict_proba(X)[:,1]

y_pred_proba[0:10]

#print ("ASSESSING THE MODEL...")
## CALCULATING GINI PERFORMANCE ON DEVELOPMENT SAMPLE
#from sklearn.metrics import roc_auc_score
#gini_score = 2*roc_auc_score(y, y_pred_proba)-1
#print ("GINI DEVELOPMENT=", gini_score)

from sklearn.metrics import accuracy_score
print("Accuracy: {0}".format(accuracy_score(y_pred,y)))

#print ("SAVING THE PERSISTENT MODEL...")
#from joblib import dump#, load
#dump(fitted_model, 'Rating_RandomForestClassifier.joblib') 


#
#i=0
#time_in_datetime = datetime.strptime(df.fecha_cambio_estado.iloc[i], "%Y-%m-%d)
#

    