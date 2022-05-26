# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 13:17:15 2018

@author: mgadi
"""

# Defining Gini and KS calculation
from sklearn.metrics import roc_auc_score

def GS(a,b):
    """Function that received two parameters; first: a binary variable representing 0=good and 1=bad, and then a second variable with the prediction of the first variable, the second variable can be continuous, integer or binary - continuous is better. Finally, the function returns the GINI Coefficient of the two lists."""    
    gini = 2*roc_auc_score(a,b)-1
    return gini

import pandas as pd
def KS(b,a):  
    """Function that received two parameters; first: a binary variable representing 0=good and 1=bad, and then a second variable with the prediction of the first variable, the second variable can be continuous, integer or binary - continuous is better. Finally, the function returns the KS Statistics of the two lists."""
    try:
        tot_bads=1.0*sum(b)
        tot_goods=1.0*(len(b)-tot_bads)
        elements = zip(*[a,b])
        elements = sorted(elements,key= lambda x: x[0])
        elements_df = pd.DataFrame({'probability': b,'gbi': a})
        pivot_elements_df = pd.pivot_table(elements_df, values='probability', index=['gbi'], aggfunc=[sum,len]).fillna(0)
        max_ks = perc_goods = perc_bads = cum_perc_bads = cum_perc_goods = 0
        for i in range(len(pivot_elements_df)):
            perc_goods =  (pivot_elements_df.iloc[i]['len'] - pivot_elements_df.iloc[i]['sum']) / tot_goods
            perc_bads = pivot_elements_df.iloc[i]['sum']/ tot_bads
            cum_perc_goods += perc_goods
            cum_perc_bads += perc_bads
            A = cum_perc_bads-cum_perc_goods
            if abs(A['probability']) > max_ks:
                max_ks = abs(A['probability'])
    except:
        max_ks = 0
    return max_ks



def prepare_dictionary_of_measures(model, X_train, y_train, X_test, y_test):
    #TRAIN MEASURES
    try: #If it is classification, we need the proba, not the predict
        y_pred_train = model.predict_proba(X_train)[:,1]
    except:
        y_pred_train = model.predict(X_test)        
    a_train = model.score(X_train, y_train)
    ks_train = KS(y_train,y_pred_train)
    gini_train = GS(y_train,y_pred_train)    

    #TEST MEASURES
    try: #If it is classification, we need the proba, not the predict
        y_pred_test = model.predict_proba(X_test)[:,1]
    except:
        y_pred_test = model.predict(X_test)        
    a_test = model.score(X_test, y_test)
    ks_test = KS(y_test,y_pred_test)
    gini_test = GS(y_test,y_pred_test)    

    return {'model':model,'accuracy_train':a_train,'ks_train':ks_train,'gini_train':gini_train,'accuracy_test':a_test,'ks_test':ks_test,'gini_test':gini_test}


from sklearn.linear_model import LinearRegression
def LR(X_train, y_train, X_test, y_test):
    """
    Linear Regresssion
    """
    model = LinearRegression().fit(X_train, y_train)
    return prepare_dictionary_of_measures(model, X_train, y_train, X_test, y_test)

from sklearn.linear_model.logistic import LogisticRegression
def LOGR(X_train, y_train, X_test, y_test):
    """
    Logistic Regresssion
    """
    model = LogisticRegression().fit(X_train, y_train)
    return prepare_dictionary_of_measures(model, X_train, y_train, X_test, y_test)


from sklearn.tree import DecisionTreeClassifier
def DT(X_train, y_train, X_test, y_test):
    """
    Decision Tree Classifier
    """
    model = DecisionTreeClassifier(min_samples_split=20, random_state=99).fit(X_train, y_train)
    return prepare_dictionary_of_measures(model, X_train, y_train, X_test, y_test)


from sklearn.linear_model import Lasso
def LASSO(X_train, y_train, X_test, y_test):
    """
    Lasso Regresssion
    """
    model = Lasso(alpha = 0.01).fit(X_train, y_train)
    return prepare_dictionary_of_measures(model, X_train, y_train, X_test, y_test)

from sklearn.linear_model import Ridge
def RIDGE(X_train, y_train, X_test, y_test):
    """
    Ridge Regresssion
    """
    model = Ridge(alpha = 0.01).fit(X_train, y_train)
    return prepare_dictionary_of_measures(model, X_train, y_train, X_test, y_test)

from sklearn.ensemble import RandomForestRegressor
def RFR(X_train, y_train, X_test, y_test):
    """
    Random Forest Regressor
    """
    model = RandomForestRegressor(n_estimators=1000, min_samples_split=2).fit(X_train, y_train)
    return prepare_dictionary_of_measures(model, X_train, y_train, X_test, y_test)


from sklearn.ensemble import RandomForestClassifier
def RFC(X_train, y_train, X_test, y_test):
    """
    Random Forest Classifier
    """
    model = RandomForestClassifier(n_estimators=1000, min_samples_split=2).fit(X_train, y_train)
    return prepare_dictionary_of_measures(model, X_train, y_train, X_test, y_test)

from sklearn.ensemble import GradientBoostingRegressor
def GBR(X_train, y_train, X_test, y_test):
    """
    Gradient Boosting Regression
    """
    model = GradientBoostingRegressor(n_estimators=1000,alpha=0.01).fit(X_train, y_train)
    return prepare_dictionary_of_measures(model, X_train, y_train, X_test, y_test)


# Defining the methods we will test
def train_method(X_train, y_train, X_test, y_test, method):  
    """ Function to redirect call to the desired method """
    if method == 'LR':  # Linear Regresssion
        return LR(X_train, y_train, X_test, y_test)
    
    elif method == 'LOGR': # Logistic Regresssion
        return LOGR(X_train, y_train, X_test, y_test)

    elif method == 'DT': # Decision Tree Classifier
        return DT(X_train, y_train, X_test, y_test)    
    
    elif method == 'LASSO': # Lasso Regresssion 
        return LASSO(X_train, y_train, X_test, y_test)
    
    elif method == 'RIDGE': # Ridge Regresssion
        return RIDGE(X_train, y_train, X_test, y_test)
    
    elif method == 'RFR': # Random Forest Regressor
        return RFR(X_train, y_train, X_test, y_test)

    elif method == 'RFC': # Random Forest Classifier
        return RFC(X_train, y_train, X_test, y_test)    

    elif method == 'GBR': # Gradient Boosting Regression
        return GBR(X_train, y_train, X_test, y_test)

#import pandas as pd    
class CustomDF():
    # def  __init__(self, filename_train, filename_test):
    #     self.df_train = pd.read_excel(filename_train)
    #     self.df_test = pd.read_excel(filename_test)
    def set_df(self, df_train, df_test):
        self.df_train = df_train
        self.df_test = df_test		
    def get_df(self):
        return (self.df_train, self.df_test)
		
    def train_method(self, inputvars, targetvar, method):  
        """ Function to redirect call to the desired method """
        y_train = self.df_train[targetvar]
        X_train = self.df_train[inputvars]        
        y_test = self.df_test[targetvar]
        X_test = self.df_test[inputvars]        

        if method == 'LR':  # Linear Regresssion
            return LR(X_train, y_train, X_test, y_test)
        
        elif method == 'LOGR': # Logistic Regresssion
            return LOGR(X_train, y_train, X_test, y_test)
    
        elif method == 'DT': # Decision Tree Classifier
            return DT(X_train, y_train, X_test, y_test)    
        
        elif method == 'LASSO': # Lasso Regresssion 
            return LASSO(X_train, y_train, X_test, y_test)
        
        elif method == 'RIDGE': # Ridge Regresssion
            return RIDGE(X_train, y_train, X_test, y_test)
        
        elif method == 'RFR': # Random Forest Regressor
            return RFR(X_train, y_train, X_test, y_test)
    
        elif method == 'RFC': # Random Forest Classifier
            return RFC(X_train, y_train, X_test, y_test)    
    
        elif method == 'GBR': # Gradient Boosting Regression
            return GBR(X_train, y_train, X_test, y_test)

    def train_methods(self, inputvars, targetvar, methods = ['LR','LASSO', 'DT', 'LOGR','RIDGE','RFR','RFC','GBR']):  
        # We develop the model in df_dev and test is on df_oot.
        self.dict_trained_model = {}
        data = []
        for method in methods:
            self.dict_trained_model[method] = self.train_method(inputvars, targetvar,method)
        #    print (dict_trained_model[method])
            data.append([method, self.dict_trained_model[method]['accuracy_train'], self.dict_trained_model[method]['accuracy_test'], self.dict_trained_model[method]['gini_train'], self.dict_trained_model[method]['gini_test'], self.dict_trained_model[method]['ks_train'], self.dict_trained_model[method]['ks_test']])
        
        self.df_result_summary = pd.DataFrame(data,columns=['method','accuracy_train', 'accuracy_test', 'gini_train', 'gini_test', 'ks_train', 'ks_test'])    
        return self.df_result_summary