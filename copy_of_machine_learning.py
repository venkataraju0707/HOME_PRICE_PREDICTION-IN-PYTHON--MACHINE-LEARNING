# -*- coding: utf-8 -*-
"""Copy of machine learning

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RbHEC-3J4u7ab3p6XVwJzwRYesRYDeKj
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
d=pd.read_csv("/content/sample_data/california_houses.zip")
#d
d.dropna(inplace=True)
d.info()

from sklearn.model_selection import train_test_split
import seaborn as sns
x=d.drop(['median_house_value'] ,axis=1)
y=d['median_house_value']
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2)
train_data=x_train.join(y_train)
test_data=x_test.join(y_test)
train_data.hist(figsize=(15,5))
plt.figure(figsize=(10, 6))
train_data.corr(numeric_only=True)

train_data.ocean_proximity.value_counts()

train_data=train_data.join(pd.get_dummies(train_data.ocean_proximity)).drop(['ocean_proximity'],axis=1)

plt.figure(figsize=(15,8))
sns.heatmap(train_data.corr(),annot=True,cmap="YlGnBu")

train_data['total_rooms']=np.log(train_data['total_rooms']+1)
train_data['total_bedrooms']=np.log(train_data['total_bedrooms']+1)
train_data['total_population']=np.log(train_data['population']+1)
train_data['households']=np.log(train_data['households']+1)
train_data.hist(figsize=(15,8))

train_data

plt.figure(figsize=(15,8))
sns.heatmap(train_data.corr(numeric_only=True),annot=True,cmap="YlGnBu")
train_data.columns

plt.figure(figsize=(15,8))
sns.scatterplot(x="latitude",y="longitude",data=train_data,hue="median_house_value",palette="coolwarm")

train_data['bedroom_ratio']=train_data['total_bedrooms']/train_data['total_rooms']
train_data['household_rooms']=train_data['total_rooms']/train_data['households']

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
scaler=StandardScaler()
x_train,y_train=train_data.drop(["median_house_value"],axis=1),train_data["median_house_value"]
x_train_s=scaler.fit_transform(x_train)
reg=LinearRegression()
reg.fit(x_train,y_train)

reg.score(x_train,y_train)

test_data['total_rooms']=np.log(test_data['total_rooms']+1)
test_data['total_bedrooms']=np.log(test_data['total_bedrooms']+1)
test_data['total_population']=np.log(test_data['population']+1)
test_data['households']=np.log(test_data['households']+1)
test_data.hist(figsize=(15,8))

test_data=test_data.join(pd.get_dummies(test_data.ocean_proximity)).drop(['ocean_proximity'],axis=1)

plt.figure(figsize=(15,8))
sns.heatmap(test_data.corr(numeric_only=True),annot=True,cmap="YlGnBu")
test_data.columns

plt.figure(figsize=(15,8))
sns.scatterplot(x="latitude",y="longitude",data=test_data,hue="median_house_value",palette="coolwarm")

test_data['bedroom_ratio']=test_data['total_bedrooms']/test_data['total_rooms']
test_data['household_rooms']=test_data['total_rooms']/test_data['households']

test_data.columns

x_test,y_test=test_data.drop(["median_house_value"],axis=1),test_data["median_house_value"]
x_test_s=scaler.fit_transform(x_test)
reg=LinearRegression()
reg.fit(x_test,y_test)

reg.score(x_test,y_test)

from sklearn.ensemble import RandomForestRegressor
forest=RandomForestRegressor()
forest.fit(x_train_s,y_train)

forest.score(x_test_s,y_test)

from sklearn.model_selection import GridSearchCV
forest=RandomForestRegressor()
param_grid={
    "n_estimators":[30,50,100],
    "max_features":[8,12,20],
    "min_samples_split":[2,4,6,8]


}
grid_search=GridSearchCV(forest,param_grid,cv=5,
                         scoring="neg_mean_squared_error",
                         return_train_score=True)
grid_search.fit(x_train_s,y_train)

best_forest=grid_search.best_estimater_

best_forest.score(x_test_s,y_test)