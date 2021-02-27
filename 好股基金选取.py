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
    good_stock = pd.merge(intersec,df_stock_rate,how='inner',on='股票简称')#.iloc[:,0]
    count = good_stock['股票简称'].size
    total_rate = good_stock['股票占比'].sum()   
    #good_stock_jc = good_stock['基金简称']   
    result.append([fund_jc,count,total_rate])

pd_result = pd.DataFrame(result,columns = ['基金简称','好股数目','好股占比'])
pd_result = pd_result.sort_values(by='好股占比',ascending=False)

pd_result = pd.merge(pd_result,stock_funds,how='inner',on='基金简称')


# In[]:


pd_result.to_csv("./基金持好股数目统计.csv", encoding="utf_8_sig")
print('完成！按任意键退出！')
stop = input() 