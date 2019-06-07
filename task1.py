import pandas as pd
import csv
import calendar
#===========数据预处理================
data = pd.DataFrame(pd.read_csv('附件一.csv', sep = ',', encoding = 'GB2312'))
data.isnull().any() #查看各列是否有缺失值
data.set_index('支付时间') #建立支付时间索引来观察异常值
for i in data.index: #查看所有订单中是否存在实际金额和应付金额不等的情况
    if data.loc[i,'实际金额'] != data.loc[i,'应付金额']:
        print(data[i])
data['支付时间'] = pd.to_datetime(data['支付时间']) #将支付时间的数据类型转化为时间类型

#=========分地区生成文件及初步描述性统计===============
#以A地区为例，其余地区的分析只需更换部分变量名称
fileA = open('task1-1A.csv', 'w', newline = '')
writer = csv.writer(fileA)  
writer.writerow(data.columns)
for i in data.index:
    if data.loc[i,'地点'] == 'A':
        writer.writerow(data.loc[i]) #按地区分类写入文件
fileA.close()

dataA = pd.DataFrame(pd.read_csv('task1-1A.csv', sep = ',', encoding = 'GB2312'))
dataA['支付时间'] = pd.to_datetime(dataA['支付时间']) #将支付时间的数据类型转化为时间类型
loandata = dataA.set_index('支付时间', drop = False)

#===========计算各月订单数=================
num = []
dataA1 = loandata['2017-01']
num.append(len(dataA1)) #计算1月份A地点的订单总量

dataA2 = loandata['2017-02']
num.append(len(dataA2))

dataA3 = loandata['2017-03']
num.append(len(dataA3))

dataA4 = loandata['2017-04']
num.append(len(dataA4))
 
dataA5 = loandata['2017-05']
num.append(len(dataA5))
 
dataA6 = loandata['2017-06']
num.append(len(dataA6))
 
dataA7 = loandata['2017-07']
num.append(len(dataA7))
 
dataA8 = loandata['2017-08']
num.append(len(dataA8))
 
dataA9 = loandata['2017-09']
num.append(len(dataA9))

dataA10 = loandata['2017-10']
num.append(len(dataA10))

dataA11 = loandata['2017-11']
num.append(len(dataA11))

dataA12 = loandata['2017-12']
num.append(len(dataA12))

sumA = loandata.resample('M',how = sum) #计算A地点每月交易总额
print(sumA['2017-05'])
print('五月订单量为：',num[4])
for i in range(12):
    print(i+1,'月的日均订单量为：',num[i]//calendar.mdays[i+1]) #计算每月日均订单量（向下取整）