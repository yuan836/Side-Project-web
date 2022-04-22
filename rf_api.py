import pickle
import gzip
import pandas as pd
with gzip.open('iris_predict2.pgz','r') as f:
  
    iris_predict = pickle.load(f)

def predict(input):

    pred = iris_predict(pd.DataFrame(input))[0]
    print (pred)
    return pred