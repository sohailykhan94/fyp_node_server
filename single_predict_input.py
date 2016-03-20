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

endSignal = False

def predict(str):
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

for line in sys.stdin:
    print predict(line)
