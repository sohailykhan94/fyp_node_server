import warnings
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

month = options[int(sys.argv[2])]
d = date(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
t = time(int(sys.argv[4]), int(sys.argv[5]))
dateObj = datetime.combine(d, t)
dateObj = dateObj + timedelta(hours = 8)

#load it again
importString = '/home/sohailyarkhan/pythonLearningModels/'+month+'/model.pkl'
with open(importString, 'rb') as fid:
    SGD = cPickle.load(fid)
cols = ['src', 'des'];
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
print pred_new
