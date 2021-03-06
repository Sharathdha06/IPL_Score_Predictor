# -*- coding: utf-8 -*-
"""IPL_score_predictor.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rrWL-m6Wi1RiDzQlnm7BgqIZXpHJR52i
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

df = pd.read_csv('ipl.csv')

df.head()

df = df.drop(['mid','batsman','bowler'], axis=1)

df.head()

const_team = df['bat_team'].unique()
print(const_team)

const_team = ['Kolkata Knight Riders' ,'Chennai Super Kings', 'Rajasthan Royals'
 'Mumbai Indians' , 'Kings XI Punjab',
 'Royal Challengers Bangalore' ,'Delhi Daredevils' ,
  'Sunrisers Hyderabad']

df = df[(df['bat_team'].isin(const_team))&(df['bowl_team'].isin(const_team))]

df['venue'].unique()

ind_stad = ['M Chinnaswamy Stadium',
       'Punjab Cricket Association Stadium, Mohali',
       'MA Chidambaram Stadium, Chepauk', 'Feroz Shah Kotla',
       'Eden Gardens', 'Wankhede Stadium',
      'Himachal Pradesh Cricket Association Stadium',
       'Rajiv Gandhi International Stadium, Uppal',
       'Shaheed Veer Narayan Singh International Stadium',
       'JSCA International Stadium Complex',
       'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium',
       'Punjab Cricket Association IS Bindra Stadium, Mohali',
       'Holkar Cricket Stadium']

df = df[df['venue'].isin(ind_stad)]

df.head()

df = df[df['overs'] > 5.0]

from datetime import datetime
df['date'] = df['date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))

#Creating dummy variables
data = pd.get_dummies(data = df, columns = ['venue','bat_team','bowl_team'])

data.head()

#Splitting dataset
x_train = data.drop('total', axis = 1)[data['date'].dt.year <=2016]
x_test = data.drop('total', axis = 1)[data['date'].dt.year >=2017]

y_train = data[data['date'].dt.year <=2016]['total'].values
y_test = data[data['date'].dt.year >=2017]['total'].values

x_train = x_train.drop(['date'], axis =1)
x_test = x_test.drop(['date'], axis =1)

#Model 
from sklearn.ensemble import RandomForestRegressor
regressor = RandomForestRegressor()

#HyperParameter tuning
n_estimators = [int(x) for x in np.linspace(start = 100, stop = 1200, num = 12)]
max_depth = [int(x) for x in np.linspace(start = 5, stop = 30, num = 6)]
max_features = ['auto', 'sqrt']
criterion = ['gini','entropy']
min_samples_split = [2,5,10,20,50,100]
min_samples_leaf = [1,2,5,7,10]

from sklearn.model_selection import RandomizedSearchCV
random_grid = {'n_estimators':n_estimators,
               'max_depth':max_depth,
               'max_features':max_features,
               'min_samples_split':min_samples_split,
               'min_samples_leaf':min_samples_leaf}
print(random_grid)

rand_cv = RandomizedSearchCV(estimator = regressor, param_distributions=random_grid, scoring= 'neg_mean_squared_error', cv = 10  )

rand_cv.fit(x_train, y_train)

rand_cv.best_params_

rand_cv.best_score_

regressor = RandomForestRegressor(n_estimators=400, max_depth=15, max_features='auto', min_samples_split=10, min_samples_leaf=2)

regressor.fit(x_train, y_train)

y_pred = regressor.predict(x_test)

sns.distplot(y_test - y_pred)

from sklearn import metrics
import numpy as np
print('MAE:', metrics.mean_absolute_error(y_test, y_pred))
print('MSE:', metrics.mean_squared_error(y_test, y_pred))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

from sklearn.linear_model import Lasso
from sklearn.model_selection import GridSearchCV
lasso = Lasso()
parameters={'alpha':[1e-15,1e-10,1e-8,1e-3,1e-2,1,5,10,20,30,35,40]}
lasso_regressor=GridSearchCV(lasso,parameters,scoring='neg_mean_squared_error',cv=10)

lasso_regressor.fit(x_train, y_train)

y_lasso = lasso_regressor.predict(x_test)

sns.distplot(y_test - y_lasso)

from sklearn import metrics
import numpy as np
print('MAE:', metrics.mean_absolute_error(y_test, y_lasso))
print('MSE:', metrics.mean_squared_error(y_test, y_lasso))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, y_lasso)))

from xgboost import XGBRegressor
xg_reg = XGBRegressor()

#HyperParameter tuning
n_estimators = [int(x) for x in np.linspace(start = 100, stop = 1200, num = 12)]
max_depth = [int(x) for x in np.linspace(start = 5, stop = 30, num = 6)]
learning_rate = [0.001,0.002,0.005,0.01,0.02,0.05,0.1,0.2,0.5]
from sklearn.model_selection import RandomizedSearchCV
random_grid = {'n_estimators':n_estimators,
               'max_depth':max_depth,
               'learning_rate':learning_rate}
print(random_grid)

rand_cv = RandomizedSearchCV(estimator = xg_reg, param_distributions=random_grid, scoring= 'neg_mean_squared_error', cv = 10  )

rand_cv.fit(x_train, y_train)

rand_cv.best_params_

xg_reg = XGBRegressor(max_depth=5, learning_rate=0.01, n_estimators= 1000)

xg_reg.fit(x_train,y_train)

y_rg = xg_reg.predict(x_test)

sns.distplot(y_test - y_rg)

print('MAE:', metrics.mean_absolute_error(y_test, y_rg))
print('MSE:', metrics.mean_squared_error(y_test, y_rg))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, y_rg)))

from lightgbm import LGBMRegressor
lg = LGBMRegressor()

#HyperParameter tuning
n_estimators = [int(x) for x in np.linspace(start = 100, stop = 1200, num = 12)]
max_depth = [-5,-3,-2,-1,1,3,5,8,15,20,25,30]
learning_rate = [0.001,0.002,0.005,0.01,0.02,0.05,0.1,0.2,0.5]
from sklearn.model_selection import RandomizedSearchCV
random_grid = {'n_estimators':n_estimators,
               'max_depth':max_depth,
               'learning_rate':learning_rate}
print(random_grid)

rand_cv = RandomizedSearchCV(estimator = lg, param_distributions=random_grid, scoring= 'neg_mean_squared_error', cv = 10  )

rand_cv.fit(x_train, y_train)

rand_cv.best_params_

lg = LGBMRegressor(learning_rate=0.02, max_depth=25,n_estimators=300)

lg.fit(x_train,y_train)

y_lg = lg.predict(x_test)

sns.distplot(y_test -y_lg)

print('MAE:', metrics.mean_absolute_error(y_test, y_lg))
print('MSE:', metrics.mean_squared_error(y_test, y_lg))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, y_lg)))

from sklearn.linear_model import LinearRegression
lr = LinearRegression()

lr.fit(x_train,y_train)
y_lr = lr.predict(x_test)
sns.distplot(y_test - y_lr)

print('MAE:', metrics.mean_absolute_error(y_test, y_lr))
print('MSE:', metrics.mean_squared_error(y_test, y_lr))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, y_lr)))

# Creating a pickle file for the classifier
import pickle
filename = 'first-innings-score-ipl-model.pkl'
pickle.dump(lr, open(filename, 'wb'))













