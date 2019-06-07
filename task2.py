import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv
plt.rcParams['font.sans-serif'] = 'SimHei'## 设置中文显示
plt.rcParams['axes.unicode_minus'] = False

#因为部分参数存在重复赋值的情况，因此绘制图时需要单独运行对应代码段绘制

##===========绘制销量前五的商品柱状图==================
data = pd.DataFrame(pd.read_csv('附件一.csv', sep = ',', encoding = 'GB2312'))
data['支付时间'] = pd.to_datetime(data['支付时间']) #将支付时间的数据类型转化为时间类型
n = pd.DataFrame(data.商品.value_counts())
print(n[:5]) #输出销量前五的商品及销量
label = ['怡宝纯净水','脉动','东鹏特饮','阿萨姆奶茶','营养快线']
num_list = [4964,2778,2581,2396,2239]
rects=plt.bar(range(len(num_list)), num_list)
plt.xlabel('商品名称')
plt.ylabel('销量')
plt.bar(range(len(num_list)),num_list,color = 'blue')
plt.xticks(range(5),label)
for i in range(len(num_list)):
    plt.text(i, num_list[i], num_list[i], va='bottom', ha='center')  
plt.show()

#==========绘制交易额折线图及环比增长率柱状图=========
dataA = pd.DataFrame(pd.read_csv('task1-1A.csv', sep = ',', encoding = 'GB2312'))
dataA['支付时间'] = pd.to_datetime(dataA['支付时间'])
loandata = dataA.set_index('支付时间', drop = False)
sumA = loandata.resample('M',how = sum) #计算A地点每月交易总额
x = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
y1 = []
for i in range(12):
    y1.append(round((sumA['实际金额'][i]-sumA['实际金额'][i-1])/(sumA['实际金额'][i-1]),2))#计算环比增长率
y2 = sumA['实际金额']

plt.rcParams['figure.figsize'] = (12.0,5.0)  
fig = plt.figure()
 
#画柱状图
ax1 = fig.add_subplot(111)
ax1.bar(x, y1,alpha=.7,color='b')
ax1.set_ylabel('环比增速（%）')
ax1.set_title("A地区月销售总额与环比增速")  
for i in range(len(y1)):
    plt.text(i, y1[i], y1[i], va='bottom', ha='center')  
#折线图
ax2 = ax1.twinx()
ax2.plot(x, y2, 'r',marker='.',ms=10)
ax2.set_ylabel('销售总额',fontsize='15')
ax2.set_xlabel('销售总额')

#================售货机毛利润占总毛利润的饼图==========
totaldata = pd.DataFrame(pd.read_csv('大类商品数据.csv', sep = ',', encoding = 'GB2312'))
totaldata['支付时间'] = pd.to_datetime(totaldata['支付时间']) #将支付时间的数据类型转化为时间类型
groups = totaldata['实际金额'].groupby([totaldata['地点'],totaldata['大类']]).sum()#按地区和商品类别分组计算交易额
plt.figure(figsize = (6,6))
income = []
for i in [0,2,4,6,8]:
    income.append(round(groups[i]*0.2+groups[i+1]*0.25,2))
label = ['A地区','B地区','C地区','D地区','E地区']
plt.pie(income,labels = label)
plt.title('各地区毛利润饼图')
plt.show()

#==============每月交易额均值气泡图====================
totaldata = pd.DataFrame(pd.read_csv('大类商品数据.csv', sep = ',', encoding = 'GB2312'))
totaldata['支付时间'] = pd.to_datetime(totaldata['支付时间']) #将支付时间的数据类型转化为时间类型
totaldata['支付时间'] = totaldata['支付时间'].map(lambda x:1000*x.year + x.month) #提取支付时间中的年、月数据
groups = totaldata['实际金额'].groupby([totaldata['二级类'],totaldata['支付时间']]).mean()#按月分组计算各二级类商品的交易额均值
groups.to_csv('mdata.csv',encoding = 'GB2312') #写入csv文件
bubble = pd.DataFrame(pd.read_csv('mdata.csv', sep = ',', encoding = 'GB2312',header = None, names = ['二级类','支付时间','价格均值'])) #读取数据
size = bubble['价格均值'] #价格均值越大则气泡图越大

plt.scatter(bubble['支付时间'],bubble['二级类'],s = size*10,alpha = 0.6)#绘制气泡图
plt.title('二级类商品月度交易额均值气泡图',fontsize='20')
plt.xlabel('月份',fontsize='15')
plt.show()

#============绘制售货机C的6月订单量热力图(7、8月只需更换判断条件)=======
dataC = pd.DataFrame(pd.read_csv('task1-1C.csv', sep = ',', encoding = 'GB2312'))
dataC['支付时间'] = pd.to_datetime(dataC['支付时间'])
dataC['支付时间'] = pd.PeriodIndex(dataC['支付时间'],freq = 'H')

months = [i.month for i in dataC['支付时间']]
file = open('file.csv', 'w', newline = '')
writer = csv.writer(file)  
writer.writerow(dataC.columns)
for i in range(len(dataC)):
    if months[i] == 6:  #将6改为7或8即可实现绘制对应月份的热力图
        writer.writerow(dataC.loc[i]) #提取六月数据
file.close()

data = pd.DataFrame(pd.read_csv('file.csv', sep = ',', encoding = 'GB2312'))
data['支付时间'] = pd.to_datetime(data['支付时间'])
data['支付时间'] = pd.PeriodIndex(data['支付时间'],freq = 'H')
data['day'] = [i.day for i in data['支付时间']]
data['hour'] = [i.hour for i in data['支付时间']] 
groups = data['状态'].groupby([data['day'],data['hour']]).count() #计算每天的各个小时内订单量
groups.to_csv('data.csv', encoding = 'GB2312')

heat = pd.DataFrame(pd.read_csv('data.csv', sep = ',', encoding = 'GB2312',header = None, names = ['日期','小时','订单量']))
z = np.zeros((24,30))
for i in range(len(heat)):
    z[int(heat['小时'][i]),int(heat['日期'][i])-1] = int(heat['订单量'][i]) #以小时为横轴，日期为纵轴，订单量为值的矩阵
plt.xlabel('小时',)
f,(ax1) = plt.subplots(figsize = (6,6), nrows = 1)
sns.heatmap(z, linewidths = 0.05, ax = ax1, cmap = 'rainbow')
ax1.set_title('C地区6月订单量热力图',fontsize='20')
ax1.set_xlabel('日期（0为1号）',fontsize='15')
ax1.set_ylabel('小时',fontsize='15')