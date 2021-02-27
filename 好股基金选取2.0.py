#!/usr/bin/env python
# coding: utf-8

# In[]:
import pandas as pd
#import os


# In[]:
import tkinter as tk
from tkinter import filedialog
def getLocalFile():
    root=tk.Tk()
    root.withdraw()
    filePath=filedialog.askopenfilename()
    print('文件路径：',filePath)
    return filePath
#if __name__ == '__main__':


# In[]
print('请输入增持情况统计：')
increase_hold_add  = getLocalFile()
inc = pd.read_csv(increase_hold_add,index_col = 0)
inc
# In[]:
#print('请输入比率：')
str_num = input("Enter your number: ")
rate = int(str_num)
rate


# In[]:


inc_sort_zcgs = inc.sort_values(by=["增持股数"], ascending=False, axis=0)
inc_sort_zcsz = inc.sort_values(by=["增持市值"], ascending=False, axis=0)
inc_sort_zcjjsl = inc.sort_values(by=["增持基金数量"], ascending=False, axis=0)
inc_sort_zcgs
inc_sort_zcgs = inc_sort_zcgs.head(rate)
inc_sort_zcsz = inc_sort_zcsz.head(rate)
inc_sort_zcjjsl = inc_sort_zcjjsl.head(rate)
inc_merge = pd.merge(inc_sort_zcsz,inc_sort_zcjjsl,how='inner',on='股票简称')
inc_merge
intersec = inc_merge['股票简称']
intersec
print('选出来的前{}股票交集为：'.format(rate))
print(intersec)
print('共{}只！'.format(len(intersec)))


# In[]:


print('请选择基金持仓：')
funds_hold_add = getLocalFile()
funds_hold = pd.read_csv(funds_hold_add,index_col = 0)
stock_funds = funds_hold
stock_funds
intersec
intersec_ex = pd.merge(intersec,inc,how='inner',on='股票简称')
intersec_ex['权重_增持市值'] = intersec_ex['增持市值']/intersec_ex['增持市值'].sum()
intersec_ex['权重_增持基金数量'] = intersec_ex['增持基金数量']/intersec_ex['增持基金数量'].sum()
intersec_ex.to_csv("./好股.csv", encoding="utf_8_sig")


# In[ ]:

result = []# pd.DataFrame()
for row in stock_funds.iterrows():
    tenpos = row[1]['十大重仓']
    exec('tps='+tenpos)
    fund_jc = row[1]['基金简称']
    #tmp = [i[0] for i in tps]   
    #rate = [r[1] for r in tps]
    list_tmp = [[i[0],i[1]] for i in tps]
    df_stock_rate = pd.DataFrame(list_tmp,columns=['股票简称','股票占比'])
 #   good_stock_rate 
 #   df_stock_funds = pd.DataFrame(tmp,columns=['股票简称'])
#    print(df_stock_funds)
    good_stock = pd.merge(intersec_ex,df_stock_rate,how='inner',on='股票简称')#.iloc[:,0]
    count = good_stock['股票简称'].size
    rate_vector = good_stock['股票占比']
    total_rate = rate_vector.sum()
    tmp = (rate_vector.mul(good_stock['权重_增持市值']))#.sum
    tmp = tmp.sum()
    total_rate_weighted_zcsz = tmp
    tmp = (rate_vector.mul(good_stock['权重_增持基金数量']))#.sum
    tmp = tmp.sum()
    total_rate_weighted_zcjjsl = tmp
    #good_stock_jc = good_stock['基金简称']   
    result.append([fund_jc,count,total_rate,total_rate_weighted_zcsz,total_rate_weighted_zcjjsl])

pd_result = pd.DataFrame(result,columns = ['基金简称','好股数目','好股占比','加权好股占比_增持市值','加权好股占比_增持基金数量'])
pd_result = pd_result.sort_values(by='加权好股占比_增持市值',ascending=False)



pd_result = pd.merge(pd_result,stock_funds,how='inner',on='基金简称')


# In[]:


pd_result.to_csv("./基金持好股情况统计.csv", encoding="utf_8_sig")
print('完成！按任意键退出！')
stop = input() 