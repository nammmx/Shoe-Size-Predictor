import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.metrics import mean_squared_error
from math import sqrt

#creating dataframe
df = pd.read_csv('shoe_data.csv')

#data splitting
X = df.drop(columns=['shoe_size'])
y = df['shoe_size']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=10)

#print RMSE
linreg = LinearRegression()
print("RMSE: {:.7f}".format(sqrt(abs(cross_val_score(linreg, X_train, y_train, cv=5, scoring="neg_mean_squared_error").mean()))))

#define model
model = linreg
model.fit(X,y)

# saving model to disk
pickle.dump(model, open('model.pkl', 'wb'))

# loading model to compare results
model = pickle.load(open('model.pkl', 'rb'))