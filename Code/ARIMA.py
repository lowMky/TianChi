#coding:utf-8
import pandas as pd
import numpy as np
from scipy import  stats
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.api import qqplot
import datetime

def getlinedata():
	k=0
        for i in open("../Data/DataGroupByShopid.txt").readlines():
		if k!=10:
			k+=1
			continue
		flag=0
		linedata=i.strip().split(',')
		for j in range(1,len(linedata)):
			if linedata[j]!='0':
				flag+=1
			if flag>0:
				break
		return linedata[j:],j

def calscorce(a,b):
	pass

if __name__=="__main__":

	##########################
	crossdays=7
	##########################
	line1data,j=getlinedata()
	alllinedata=line1data
	print line1data,j
	line1data=line1data[:-crossdays]
	#print len(line1data)
	a = map(lambda x: float(x),line1data)
	b= map(lambda x: float(x),alllinedata)
	'''留下14周作为验证'''
	data=a
	firstdate = datetime.datetime(2015,06,26) + datetime.timedelta(days = j-1)
	lastdate=datetime.datetime(2016,10,31) - datetime.timedelta(days = crossdays)
	medialastdate=datetime.datetime(2016,10,31)
	print firstdate,lastdate,medialastdate
	data=pd.Series(data,index = pd.date_range(firstdate,lastdate))
	alldata=pd.Series(b,index = pd.date_range(firstdate,medialastdate))
	#data.index = pd.Index(sm.tsa.datetools.dates_from_range(str(j),'494'))
	
	fig = plt.figure(figsize=(12,8))
	ax1= fig.add_subplot(221)
	data.plot(ax=ax1)
	ax2= fig.add_subplot(222)
	diff1 = data.diff(1)
	diff1.plot(ax=ax2)
	#fig = plt.figure(figsize=(12,8))
	ax3=fig.add_subplot(223)
	fig = sm.graphics.tsa.plot_acf(data,lags=100,ax=ax3)
	ax4 = fig.add_subplot(224)
	fig = sm.graphics.tsa.plot_pacf(data,lags=50,ax=ax4)
	plt.show()
	'''建立模型'''
	arma_mod81 = sm.tsa.ARMA(data,(8,1)).fit()
	print arma_mod81.aic,arma_mod81.bic,arma_mod81.hqic
	
	''''''
	resid = arma_mod81.resid
	fig = plt.figure(figsize=(12,8))
	ax1 = fig.add_subplot(211)
	fig = sm.graphics.tsa.plot_acf(resid.values.squeeze(), lags=40, ax=ax1)
	ax2 = fig.add_subplot(212)
	fig = sm.graphics.tsa.plot_pacf(resid, lags=40, ax=ax2)
	plt.show()
	
	print(stats.normaltest(resid))
	fig = plt.figure(figsize=(12,8))
	ax = fig.add_subplot(111)
	fig = qqplot(resid, line='q', ax=ax, fit=True)
	plt.show()
	''''''
	predict_dta = arma_mod81.predict(lastdate, medialastdate, dynamic=True)
	print predict_dta
	print alllinedata[-crossdays:]
	fig, ax1 = plt.subplots(figsize=(12, 8))
	ax1 = data.ix[lastdate:].plot(ax=ax1)
	fig = arma_mod81.plot_predict(lastdate,medialastdate, dynamic=True, ax=ax1, plot_insample=False)
	alldata.plot(ax=ax1)
	plt.show()
