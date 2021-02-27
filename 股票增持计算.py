#!/usr/bin/env python
# coding: utf-8
# In[]:
import pandas as pd
#import os
import tkinter as tk
from tkinter import filedialog
def getLocalFile():
    root=tk.Tk()
    root.withdraw()
    filePath=filedialog.askopenfilename()
    print('文件路径：',filePath)
    return filePath
#if __name__ == '__main__':
# In[]: 
file1 = getLocalFile()
file2 = getLocalFile()
#sheet1 = pd.read_csv('./all_1/股票被持有信息统计.csv')
sheet1 = pd.read_csv(file1)
sheet1
#sheet2 = pd.read_csv('./all_2/股票被持有信息统计.csv')
sheet2 = pd.read_csv(file2)
sheet3 = pd.merge(sheet1,sheet2,how='inner',on='股票简称')
sheet3
sheet3['增持股数'] = sheet3['被持股数_万_x'] - sheet3['被持股数_万_y']


# In[]:
sheet3['增持市值'] = sheet3['被持仓市值_万_x'] - sheet3['被持仓市值_万_y']
#sheet3['增持占比'] = sheet3['平均占比_x'] - sheet3['平均占比_y']
sheet3['增持基金数量'] = sheet3['所属基金数目_x'] - sheet3['所属基金数目_y']
sheet3.to_csv('增持情况统计.csv',encoding="utf_8_sig")




