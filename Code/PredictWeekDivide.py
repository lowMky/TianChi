#!/usr/lib/python2.7
#coding = utf-8

import Arma
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy import stats
from statsmodels.graphics.api import qqplot

def pre_process(data):
    wedata = []
    wddata = []
    length = len(data)
    for i in range(length):
        if i % 7 == 1 or i % 7 == 2:
            wedata.append(data[i])
        else:
            wddata.append(data[i])
    return wddata,wedata


def after_process(wdscore,wdrecord,wescore,werecord):
    score = wdscore * 11.0/15 + wescore * 4.0/15
    
    record = [wdrecord[0],wdrecord[1]]
    record[0].insert(4,werecord[0][0])
    record[1].insert(4,werecord[1][0])
    record[0].insert(5,werecord[0][1])
    record[1].insert(5,werecord[1][1])

    record[0].insert(11,werecord[0][2])
    record[1].insert(11,werecord[1][2])
    record[0].insert(12,werecord[0][3])
    record[1].insert(12,werecord[1][3])
    return score,record

def predict():
    final_score = 0
    now = datetime.datetime.now()
    now = now.strftime("%m_%d_%d_%H:%M:%S")
    filepath = '../Record/PredictWeekDivideRecord' + now + '.txt'
    output = open(filepath,'w')

    with open('../Data/DataGroupByShopid.txt') as file:
        idx = 0
        for line in file:
            line = line.strip('\n').split(',')
            data = [float(num) for num in line]
        
            #Arma.predict(14,8,1,data = data)    
            wddata,wedata = pre_process(data)   
            wdscore,wdrecord = Arma.cross_validation(11,6,1,data = wddata)
            wescore,werecord = Arma.cross_validation(4,3,1,data = wedata)
            
            score,record = after_process(wdscore,wdrecord,wescore,werecord)
            
            output.write(str(idx) + " " + str(score)+"\n")
            output.write(','.join(str(i)for i in record[0]))
            output.write('\n')
            output.write(','.join(str(i)for i in record[1]))
            output.write('\n') 
            final_score += score
            idx += 1
            print str(idx) + " " + str(score)
            if idx == 20:
                break
    print final_score/idx

if __name__ == '__main__':
    predict()
