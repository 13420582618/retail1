import pandas as pd
import csv
#============task3-1===================
data = pd.DataFrame(pd.read_csv('大类商品数据.csv', sep = ',', encoding = 'GB2312')) #大类商品数据是在原始数据中加入了“大类”列的数据表
file1 = open('A地区饮料类商品数据.csv', 'w', newline = '')
writer = csv.writer(file1)  
writer.writerow(data.columns)
for i in data.index:
    if data.loc[i,'地点'] == 'A':
        if data.loc[i,'大类'] == '饮料':
            writer.writerow(data.loc[i]) #按商品分类写入文件
file1.close()
dataA = pd.DataFrame(pd.read_csv('A地区饮料类商品数据.csv', sep = ',', encoding = 'GB2312'))
n = pd.DataFrame(dataA.商品.value_counts()) #计算各商品的销量
n.columns = ['销量']
n['标签'] = None #添加标签列
c = n.describe() #查看n的描述性统计量
num25 = c.loc['25%'] #获取四分位点
num75 =  c.loc['75%'] #获取四分位点
for i in range(len(n)):
    if int(n['销量'][i]) > int(num75): #若商品销量大于四分之三的商品，则为畅销商品
        n['标签'][i] = '畅销'
    elif int(n['销量'][i]) < int(num25): #若商品销量小于四分之三的商品，则为滞销商品
        n['标签'][i] = '滞销'
    else:
        n['标签'][i] = '正常' 
n.to_csv('task3-1A.csv',encoding = 'GB2312')

#============task3-2====================
#受限于编程能力和任务进度，销售数据的词云图是通过在线词云生成工具绘制的
data32A = pd.DataFrame(pd.read_csv('task3-2A.csv', sep = ',', encoding = 'GB2312'))
groupsA = data32A.groupby(['二级类']).sum()
groupsA.columns = ['A地区销量']

data32B = pd.DataFrame(pd.read_csv('task3-2B.csv', sep = ',', encoding = 'GB2312'))
groupsB = data32B.groupby(['二级类']).sum()
groupsB.columns = ['B地区销量']
example = pd.merge(groupsA,groupsB,how = 'inner',left_index = True,right_index = True) #将各地区二级类商品数据合并成一个表

data32C = pd.DataFrame(pd.read_csv('task3-2C.csv', sep = ',', encoding = 'GB2312'))
groupsC = data32C.groupby(['二级类']).sum()
groupsC.columns = ['C地区销量']
example = pd.merge(example,groupsC,how = 'inner',left_index = True,right_index = True)

data32D = pd.DataFrame(pd.read_csv('task3-2D.csv', sep = ',', encoding = 'GB2312'))
groupsD = data32D.groupby(['二级类']).sum()
groupsD.columns = ['D地区销量']
example = pd.merge(example,groupsD,how = 'inner',left_index = True,right_index = True)

data32E = pd.DataFrame(pd.read_csv('task3-2E.csv', sep = ',', encoding = 'GB2312'))
groupsE = data32E.groupby(['二级类']).sum()
groupsE.columns = ['E地区销量']
example = pd.merge(example,groupsE,how = 'inner',left_index = True,right_index = True)