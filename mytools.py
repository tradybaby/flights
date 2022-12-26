import sqlite3
import random
import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.feature_extraction import text 
import pickle

def create_my_file(fn):
    fp = open(fn, 'w')
    fp.close()
def append_my_file(fn, txt):
    fp = open(fn, 'a')
    fp.write(txt + '\n')
    fp.close()

def predict_delay(fn, fp):
    f = open(fn)
    flights = f.readlines()
    flights_2 = np.array_split(flights, len(flights)/9)

    labels = ["id", "Airline", "Flight", "AirportFrom", "AirportTo", "DayOfWeek", "Time", "Length", "Delay"]
    df = pd.DataFrame.from_records(flights_2, columns = labels)
    df = df.replace('\n', '', regex=True)
    
    minobs = min(df.value_counts('Delay').values)
    df = df.groupby('Delay').sample(n=minobs, random_state=1).sample(frac=1, random_state=1)
    df.iloc[:5,:]
    
    X = np.asarray(df["Time"])
    X = X.reshape(-1, 1)

    Y = np.asarray(df["Delay"], dtype='int8')
    Y = Y.reshape(-1, 1)
    Y = Y.ravel()
    
    clff, Xmax2 = pickle.load(open('clf.pkl', 'rb'))
    fpp = open(fp, 'a')

    df = df.reset_index()   
    results = clff.predict(X)
    for i in range(len(df["Time"])):
            fpp.write(df["Flight"][i] + " - " + df["Delay"][i] + " - " + str(results[i]) + '\n')

    fpp.close()


def append_my_file2(fn, txt):
    fp = open(fn, 'a')
    fa = open(fn)
    if len(fa.readlines())%3 == 2:
        fp.write(str(len(fp.readlines())) + ';' + "\n")
    else:
        fp.write(txt + ';')
    fp.close()
