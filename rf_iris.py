import pandas as pd
#from statsmodels.api import datasets
from sklearn import datasets ## Get dataset from sklearn

import numpy as np

## Import the dataset from sklearn.datasets
iris = datasets.load_iris()

## Create a data frame from the dictionary
species = [iris.target_names[x] for x in iris.target]
iris = pd.DataFrame(iris['data'], columns = ['Sepal_Length', 'Sepal_Width', 'Petal_Length', 'Petal_Width'])
iris['Species'] = species

from sklearn.model_selection import train_test_split

# Spliting the iris dataset into it‘s attributes (X) and labels (y).
# drop() is making a copy of the data (if inplace = False)
X = iris.drop("Species", axis=1)
y = iris["Species"].copy()

# Spliting the data into training and testing dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
print(f"Shape of X_train: {X_train.shape}")
print(f"Shape of X_test:  {X_test.shape}")

from sklearn import preprocessing

# Converting string labels into numbers
# Encoding before splitting the data will lead to data leakage
le = preprocessing.LabelEncoder()
y_train = le.fit_transform(y_train)
y_test = le.transform(y_test)

from sklearn.model_selection import cross_val_score
from sklearn import  ensemble, preprocessing, metrics
forest = ensemble.RandomForestClassifier(n_estimators = 15)
forest_fit = forest.fit(X_train, y_train)
test_y_predicted = forest_fit.predict(X_test)
print(test_y_predicted)
accuracy = metrics.accuracy_score(y_test, test_y_predicted)

print(f"Accuracy: {accuracy}")

result = forest_fit
# x = np.array([[5.1,	3.5 ,1.4, 0.2]])
# test_y_predicted = forest.predict(pd.DataFrame(x))[0]
# print(test_y_predicted)
import pickle
import gzip

with gzip.GzipFile('iris_predict3沒有red.pgz','w') as f:
    pickle.dump(result,f)