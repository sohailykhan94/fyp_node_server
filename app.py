#!flask/bin/python
from flask import Flask, jsonify, request
import logging, json
from logging.handlers import RotatingFileHandler
import warnings
import redis
warnings.filterwarnings('ignore')

from datetime import timedelta
from datetime import datetime
from datetime import date
from datetime import time
import dateutil.parser
import sys
import random
import numpy as np
import cPickle
np.random.seed(21)

from sklearn import linear_model, cross_validation, metrics, svm
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support, accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd
global r
r = redis.StrictRedis(host='localhost', port=6379, db=0)
def totalPrediction(str):
    app.logger.warning('Predicting Total')
    str_array = str.split()
    if len(str_array) != 5:
        return "Incorrect Input"
    options = {1 : 'jan',
               2 : 'feb',
               3 : 'mar',
               4 : 'apr',
               5 : 'may',
               6 : 'jun',
               7 : 'jul',
               8 : 'aug',
               9 : 'sep',
               10 : 'oct',
               11 : 'nov',
               12 : 'dec'
    }

    month = options[int(str_array[1])]
    d = date(int(str_array[0]), int(str_array[1]), int(str_array[2]))
    t = time(int(str_array[3]), int(str_array[4]))
    dateObj = datetime.combine(d, t)
    dateObj = dateObj - timedelta(hours = 8)

    #load it again
    importString = '/home/sohailyarkhan/pythonLearningModels/'+month+'/model.pkl'
    with open(importString, 'rb') as fid:
        SGD = cPickle.load(fid)
    cols = ['src', 'des']
    data_speed = pd.read_csv('/home/sohailyarkhan/node-server/fyp_node_server/speedmap.csv', names=cols, dtype={})
    final_data = pd.DataFrame(columns=['year','month','day','hour','minute','src','des'])
    final_data['src'] = data_speed['src']
    final_data['des'] = data_speed['des']
    final_data['year'] = int(dateObj.year)
    final_data['month'] = int(dateObj.month)
    final_data['day'] = int(dateObj.day)
    final_data['hour'] = int(dateObj.hour)
    final_data['minute'] = int(dateObj.minute)
    pred_new = SGD.predict(final_data)
    data = pd.Series(pred_new)
    df = pd.Series.to_frame(data, name='road_saturation')
    df2 = pd.read_json("/home/sohailyarkhan/node-server/fyp_node_server/speedMap.json")
    df2 = df2.drop('index', axis=1)
    frames = [df, df2]
    result = pd.concat(frames, axis=1, join='inner')
    resultJSON = result.to_json(orient='records')
    return resultJSON

def predict(str):
    app.logger.warning('Predicting')
    str_array = str.split()
    if len(str_array) != 7:
        return "Incorrect Input"
    options = {1 : 'jan',
               2 : 'feb',
               3 : 'mar',
               4 : 'apr',
               5 : 'may',
               6 : 'jun',
               7 : 'jul',
               8 : 'aug',
               9 : 'sep',
               10 : 'oct',
               11 : 'nov',
               12 : 'dec'
    }
    month = options[int(str_array[1])]
    d = date(int(str_array[0]), int(str_array[1]), int(str_array[2]))
    t = time(int(str_array[3]), int(str_array[4]))
    dateObj = datetime.combine(d, t)
    dateObj = dateObj - timedelta(hours = 8)
    importString = '/home/sohailyarkhan/pythonLearningModels/'+month+'/model.pkl'
    with open(importString, 'rb') as fid:
        SGD = cPickle.load(fid)
    final_data = pd.DataFrame(np.array([[int(dateObj.year), int(dateObj.month), int(dateObj.day), int(dateObj.hour), int(dateObj.minute), int(str_array[5]), int(str_array[6])]]), columns=['year','month','day','hour','minute','src','des'])
    pred_new = SGD.predict(final_data)
    return pred_new

app = Flask(__name__, static_url_path='')

@app.route('/get_single_prediction', methods=['GET'])
def getSinglePrediction():
    with open('/home/sohailyarkhan/node-server/flask-api/speedMapSrcDes.json') as data_file:
        data = json.load(data_file)
    year = request.args.get('year')
    month = request.args.get('month')
    day = request.args.get('day')
    hour = request.args.get('hour')
    minute = request.args.get('minute')
    src = request.args.get('src')
    des = request.args.get('des')
    for i in data['nodes']:
        if ('src' in i and i['src'] == int(src)) and ('des' in i and i['des'] == int(des)):
            src_lat = i['src_lat']
            src_long = i['src_long']
            des_lat = i['des_lat']
            des_long = i['des_long']
    new_req = str(year) + "-"  +str(month)+ "-"  +str(day)+ "-"  +str(hour)+ "-"  +str(minute)+ "-"  +str(src) + "-"  +str(des)
    if r.get(new_req):
	app.logger.warning('Reading from Redis')
	prediction = r.get(new_req)
	app.logger.warning('Retrieved value = '+prediction)
    else:
	app.logger.warning('Writting to Redis')
    	prediction = predict(str(year) + " " + str(month) + " " + str(day) + " " + str(hour) + " " + str(minute) + " " + str(src) + " " + str(des))
	r.set(new_req, prediction)
	r.expire(new_req, 172800)	    
    return jsonify({'status': "success", 'nodes': {'src_lat': str(src_lat), 'src_long': str(src_long), 'des_lat':str(des_lat), 'des_long':str(des_long), 'road_saturation_level': str(prediction)}})

@app.route('/get_prediction', methods=['GET'])
def getPrediction():
    year = request.args.get('year')
    month = request.args.get('month')
    day = request.args.get('day')
    hour = request.args.get('hour')
    minute = request.args.get('minute')
    new_req = str(year) + "-"  +str(month)+ "-"  +str(day)+ "-"  +str(hour)+ "-"  +str(minute)
    if r.get(new_req):
        app.logger.warning('Reading from Redis')
        prediction = r.get(new_req)
    else:
        app.logger.warning('Writting to Redis')
	prediction = totalPrediction(str(year) + " " + str(month) + " " + str(day) + " " + str(hour) + " " + str(minute))
        r.set(new_req, prediction)
        r.expire(new_req, 172800)
    resultJSON = json.loads(prediction)
    return jsonify({'nodes': resultJSON, 'status': "success"})

if __name__ == '__main__':
    handler = RotatingFileHandler('err.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0', port=4000)
