
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy import stats
from statsmodels.graphics.api import qqplot

def readfile():
    
    with open('../Data/DataGroupByShopid.txt') as file:
        for line in file:
            line = line.strip('\n').split(',')
            return [int(num) for num in line]

def process(datas):  
    datas = pd.Series(datas,index = pd.date_range('2015-06-26','2016-10-31'))
    #datas.plot(figsize=(12,8))
    fig = plt.figure(figsize=(12,8))
    ax1 = fig.add_subplot(221) 
    ax1.plot(datas)
    ax2 = fig.add_subplot(222)
    ax2.plot(datas)
    fig.show()

def process():
    with open('../Data/DataGroupByShopid.txt') as file:
        index = 1
        fig = plt.figure(figsize=(12,8))
        for line in file:
            line = line.strip('\n').split(',')
            datas = [int(num) for num in line]
            datas = pd.Series(datas,index = pd.date_range('2015-06-26','2016-10-31'))
            datas = datas.diff(1)
            ax = fig.add_subplot(330+index)
            ax.plot(datas)
            index += 1
            if index == 10:
                index = 1
                fig.show()
                ss = raw_input()
                fig.clf()

if __name__ == '__main__':
    #datas = readfile()
    #process(datas)
    process()
