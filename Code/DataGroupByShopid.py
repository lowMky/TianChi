
import datetime

def DataGroupByShopid(): 
    
    FirstDay = datetime.datetime.strptime('2015-06-26 00:00:00','%Y-%m-%d %H:%M:%S')
    LastDay = datetime.datetime.strptime('2016-10-31 23:59:59','%Y-%m-%d %H:%M:%S')
    lastdays = (LastDay - FirstDay).days+1
    idx = 0
    Mat = [[0 for i in range(lastdays)] for i in range(2000)]
    
    with open('../Download/dataset/dataset/user_pay.txt','r') as file:
        for line in file:
            datas = line.split(',')
            shopid = int(datas[1])
            shopday = datetime.datetime.strptime(datas[2][0:18],'%Y-%m-%d %H:%M:%S')
            index = (shopday - FirstDay).days
            Mat[shopid-1][index] += 1
            idx += 1
            if idx % 1000000 == 0:
                print idx + idx/1000000
    output = open('DataGroupByShopid.txt','w')
    for line in Mat:
        output.write(','.join(str(i)for i in line))
        output.write('\n')
    output.close()

if __name__ == "__main__":
    DataGroupByShopid()

