import numpy as np
import glob
import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns
import warnings
from sklearn import preprocessing
from keras.models import Sequential 
from keras.layers import Dense, LSTM
import numpy
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import GridSearchCV
from keras.preprocessing.sequence import pad_sequences

def loadLable(path):
    with open(path, 'r') as stream:
        return [int(i) for i in stream]
    
def loadData(path, step):      
    with open(path, 'r') as stream:
        data = {}
        for line in stream:
            line = line.strip()
            if not line:
                continue 
            lst = line.split(',')
            if len(lst) < step + 2:
                continue
            if lst[0] not in data:
                data[lst[0]] = []
            data[lst[0]].append(lst[step+1])
    maxLen = min(len(v) for v in data.values())
    
    data = {k:v[:maxLen] for k, v in data.items()}
        
    return data, maxLen

def loadExample(path):
    scaler = preprocessing.MinMaxScaler()
    res = []
    with open(path, 'r') as stream:
        tmp = []
        for line in stream:
            line = line.strip()
            if not line:
                res.append(tmp)
                tmp = []
                continue
            lst = line.split(',')
            value = [float(ele) for ele in lst[1:]]
            scaler.fit([value])
            norm = scaler.transform([value])
            norm = pad_sequences([value], padding='post', maxlen=50)
            tmp.extend(norm[0])
    if tmp:
        res.append(tmp)

    return res

def getFeatureLabel():
    basePath = 'E:\\PythonCode\\dota2\\src\\data\\'
    featurePath =  basePath + 'tsDataX.txt'
    labelPath =  basePath + 'tsDataY.txt'

    raw = loadExample(featurePath)
    data = np.array(raw)

    label = loadLable(labelPath)
    label = np.array(label)

    trainLable, pick3500 = zip(*[(l,row) for l, row in zip(label, data) if len(row) == 3500])
    train = np.array([np.reshape(row, (50, 70)) for row in pick3500]) 

    return train, trainLable

def lstmModel(data, label):
    sampleSize, step, featureSize = data.shape
    batchSize = sampleSize//60
    model = Sequential()
    model.add(LSTM(36, input_shape=(step, featureSize),dropout=0.07))
    model.add(Dense(1))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(data, label, epochs=400, batch_size=batchSize, verbose=1)
    model.save('E:\\PythonCode\\dota2\\src\\modelWeight\\lstm_model.h5')
    return model

def run():
    feature, label = getFeatureLabel()
    model = lstmModel(feature, label)