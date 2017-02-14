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


def predict():
    final_score = 0
    now = datetime.datetime.now()
    now = now.strftime("%m_%d_%d_%H:%M:%S")
    filepath = '../Record/PredictOriginalRecord' + now + '.txt'
    output = open(filepath,'w')

    with open('../Data/DataGroupByShopid.txt') as file:
        idx = 0
        for line in file:
            line = line.strip('\n').split(',')
            data = [float(num) for num in line]
        
            #Arma.predict(14,8,1,data = data)       
            score,record = Arma.cross_validation(14,3,1,data = data)
            
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
