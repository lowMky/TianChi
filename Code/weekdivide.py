#!/usr/lib/python2.7
#coding = utf-8

import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy import stats
from statsmodels.graphics.api import qqplot


def readfile(index):
    with open('../Data/DataGroupByShopid.txt') as file:
        idx = 0
        for line in file:
            if index == idx:
                line = line.strip('\n').split(',')
                return [float(num) for num in line]
            idx += 1


def (crossdays,p,q,IndexOfShop = None,data = None,DEBUG = False):
    #a-all  u-use for predict  p-predict_data
    if data == None:
        data = readfile(IndexOfShop) 
    
    adata,idx = pre_process(data)
    udata = adata[:-crossdays]
    ufirstday = datetime.datetime(2015,6,26) + datetime.timedelta(days = idx)
    ulastday = datetime.datetime(2016,10,31) - datetime.timedelta(days = crossdays)

    afirstday = ufirstday
    alastday = datetime.datetime(2016,10,31)

    pfirstday = ulastday + datetime.timedelta(days = 1)
    plastday = alastday

    adata = pd.Series(adata,index = pd.date_range(afirstday,alastday))
    udata = pd.Series(udata,index = pd.date_range(ufirstday,ulastday))
  
    #print (ulastday - ufirstday).days + 1,len(udata) 
   
    if DEBUG:
        fig = plt.figure(figsize=(12,8))
        ax1 = fig.add_subplot(221)
        udata.plot(ax = ax1)
        ax2 = fig.add_subplot(222)
        diff1 = udata.diff(1)
        diff1.plot(ax = ax2)
    
        ax3 = fig.add_subplot(223)
        fig = sm.graphics.tsa.plot_acf(udata,lags = 40,ax = ax3)
        ax4 = fig.add_subplot(224)
        fig = sm.graphics.tsa.plot_pacf(udata,lags = 40,ax = ax4)
        fig.show()
        pause = raw_input()
    
    arma_mod81 = sm.tsa.ARMA(udata,(p,q)).fit()
    
    if DEBUG:
        print arma_mod81.aic,arma_mod81.bic,arma_mod81.hqic

    resid = arma_mod81.resid
    
    if DEBUG:
        fig = plt.figure(figsize = (12,8))
        ax1 = fig.add_subplot(211)
        fig = sm.graphics.tsa.plot_acf(resid.values.squeeze(),lags = 40, ax = ax1)
        ax2 = fig.add_subplot(212)
        fig = sm.graphics.tsa.plot_pacf(resid,lags = 40, ax = ax2)
        #fig.show()
        #pause = raw_input()    
 
        print(stats.normaltest(resid))
        fig = plt.figure(figsize=(12,8))
        ax = fig.add_subplot(111)
        fig = qqplot(resid,line = 'q',ax = ax,fit = True)
        fig.show()
        pause = raw_input()

    print pfirstday,plastday 
    pdata = arma_mod81.predict(pfirstday,plastday,dynamic = True)    
    print pdata
    print adata[-crossdays:]
    
    if DEBUG:
        fig = plt.figure(figsize=(12,8))
        ax = fig.add_subplot(111)
   
        adata.ix[pfirstday:].plot(ax = ax)
        pdata.ix[pfirstday:].plot(ax = ax)
        fig = arma_mod81.plot_predict(pfirstday,plastday,dynamic = True,ax = ax,plot_insample = False)
        fig.show()
    
    score = cal_score(adata.ix[pfirstday:],pdata.ix[pfirstday:])
    print 'mod'+str(p)+str(q)+" : "+str(score)
    pause = raw_input() 
    
if __name__ == '__main__':
    #cross_validation(7,8,1,IndexOfShop = 88)
    #cross_validation(7,7,0,IndexOfShop = 88)
    #predict(7,8,1,IndexOfShop = 88)

