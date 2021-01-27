# -*- coding: utf-8 -*-
"""house-prices.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1t8rQ8iNIjEOGZXPrW1yDAbeZKemJWmX8
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
# %matplotlib inline

"""Upload and read file"""

df_train=pd.read_csv('../input/house-prices-advanced-regression-techniques/train.csv')
df_train.shape

df_test=pd.read_csv('../input/house-prices-advanced-regression-techniques/test.csv')
df_test.shape

train_test=pd.concat([df_train,df_test],axis=0,sort=False)
train_test.head()

sales= train_test['SalePrice']
Id= train_test['Id']

train_test= train_test.drop(columns=['SalePrice'])
train_test= train_test.drop(columns=['Id'])
train_test.head()

total = train_test.isnull().sum().sort_values(ascending=False)
percent = (train_test.isnull().sum()/train_test.isnull().count()).sort_values(ascending=False)
missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
missing_data.head(20)

df_numeric=train_test.select_dtypes(include=np.number)
df_numeric

total = df_numeric.isnull().sum().sort_values(ascending=False)
percent = (df_numeric.isnull().sum()/df_numeric.isnull().count()).sort_values(ascending=False)
missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
missing_data.head(5)

df_numeric=df_numeric.fillna(df_numeric.median())

df_obj = train_test.select_dtypes(include=['object']).copy()
df_obj

total = df_obj.isnull().sum().sort_values(ascending=False)
percent = (df_obj.isnull().sum()/df_obj.isnull().count()).sort_values(ascending=False)
missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
missing_data.head(5)

df_obj = df_obj.drop(columns=['PoolQC','MiscFeature','Alley','Fence','FireplaceQu'])
df_obj

for column in df_obj.columns:
  df_obj[column] = df_obj[column].astype('category')
  df_obj[column] = df_obj[column].cat.codes

df_obj

df_new = pd.concat([df_numeric, df_obj], axis=1)
df_new

df1 = pd.concat([df_new, sales], axis=1)
df2 = pd.concat([Id , df1], axis=1)
df2

train= df2[1:1460]
train.shape

test= df2[1460:].drop(columns=['SalePrice'])
test.shape

X= train.drop('SalePrice', axis=1)
y = train['SalePrice']

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import cross_val_score

GBoost = GradientBoostingRegressor(n_estimators=3000, learning_rate=0.05,
                                   max_depth=4, max_features='sqrt',
                                   min_samples_leaf=15, min_samples_split=10, 
                                   loss='huber', random_state =5)

GBoost.fit(X, y)

score = cross_val_score(GBoost, X, y, cv=10, n_jobs=-1)
print("Score: ", score.max())

print("train score: ", GBoost.score(X,y))

submission = pd.read_csv('../input/house-prices-advanced-regression-techniques/sample_submission.csv')

y_pred = GBoost.predict(test)

submission['SalePrice'] = y_pred
submission.head(10)

submission.to_csv('submission.csv', index=False)
