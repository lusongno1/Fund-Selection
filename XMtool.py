# In[]: 
#!/usr/bin/env python
# coding: utf-8
# encoding=utf-8
import pandas as pd
import requests
from lxml import etree
import re
#import collections
import numpy as np


# In[]: 
sample = '150000'#样本数量
sc = '6yzf'#排序键值
st = 'desc'#排序方式
ft = 'gp'#基金类型
dx = '1'#是否可购
season = 1#季度选择


r1r = 1#日增长率
r1z = 1#近1周
r1y = 1#近1月
r3y = 0.3333#近3月
r6y = 0.3333#近6月
r1n = 0.25#近1年
r2n = 0.25#近2年
r3n = 0.25#近3年
rjnl = 0.25#今年来
rcll = 1#成立来


    
sd = '2021-01-07'
ed = '2021-02-07'

# In[] 在参数文书写单元后加上这么一段就可以了
#from PyQt5.QtWidgets import QInputDialog, QLineEdit, QDialog
from PyQt5.QtWidgets import QDialog
import sys
from PyQt5.QtWidgets import QApplication
import dialog
class TestDialog1(QDialog,dialog.Ui_XMtool):  
    def __init__(self,parent=None):  
        super(TestDialog1,self).__init__(parent)  
        self.setupUi(self)

app=QApplication(sys.argv)  
dlg=TestDialog1()  
dlg.show()  
app.exec_()

sample = dlg.sample.text() #样本数量
sc = dlg.sc.currentText() #排序键值
st = dlg.st.currentText() #排序方式
ft = dlg.ft.currentText() #基金类型
dx = dlg.dx.currentText() #是否可购
season = int(dlg.season.currentText()) #季度选择


r1r = float(dlg.r1r.text()) #日增长率
r1z = float(dlg.r1z.text())#近1周
r1y = float(dlg.r1y.text())#近1月
r3y = float(dlg.r3y.text())#近3月
r6y = float(dlg.r6y.text())#近6月
r1n = float(dlg.r1n.text())#近1年
r2n = float(dlg.r2n.text())#近2年
r3n = float(dlg.r3n.text())#近3年
rjnl = float(dlg.rjnl.text())#今年来
rcll = float(dlg.rcll.text())#成立来

# In[]:
header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
        'Referer': 'http://fund.eastmoney.com/data/fundranking.html',
        'Cookie':'st_si=74949607860286; st_asi=delete; ASP.NET_SessionId=gekyucnll0wte0wrks2rr23b; _adsame_fullscreen_18503=1; EMFUND1=null; EMFUND2=null; EMFUND3=null; EMFUND4=null; EMFUND5=null; EMFUND6=null; EMFUND7=null; EMFUND8=null; EMFUND0=null; EMFUND9=02-07 16:37:21@#$%u521B%u91D1%u5408%u4FE1%u5DE5%u4E1A%u5468%u671F%u80A1%u7968A@%23%24005968; st_pvi=90009717841707; st_sp=2021-02-07%2012%3A14%3A29; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Flink; st_sn=21; st_psi=2021020716562364-0-0372414431'
}
url = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft='+ft+'&rs=&gs=0&sc='+sc+'&st='+st+'&sd='+sd+'&ed='+ed+'&qdii=&tabSubtype=,,,,,&pi=1&pn='+sample+'&dx='+dx+'&v=0.2692835962833908'
response = requests.get(url=url, headers=header)
text = response.text
data = text.split('=')[1]#使用等号分开去后面一部分
compile_data = re.findall("{datas:\\[(.*)\\],allRecords", str(data))[0]#取datas和allRecords中的所有内容
strip_data = str(compile_data).strip('[').strip(']')#移除字符串头尾的中括号
replace_quta = strip_data.replace('"', "")#双引号替换为空
quota_arrays = replace_quta.split(",")#使用逗号转为列表
intervals = [[i * 25, (i + 1) * 25] for i in range(15000)]#生成10000个区间，每个区间长度为25
narrays = []
for k in intervals:
    start, end = k[0], k[1]
    line = quota_arrays[start:end]#将条目25个分为一组,表示一只基金
    narrays.append(line)
header = ["基金代码", "基金简称", "基金条码", "日期",
          "单位净值", "累计净值", "日增长率", "近1周", "近1月", "近3月", "近半年", "近1年", "近2年", "近3年",
          "今年来", "成立来", "其他1", "其他2", "其他3", "其他4", "其他5", "其他6", "其他7", "其他8", "其他9"]
df = pd.DataFrame(narrays, columns=header)#生成pd数据结构
df.dropna()
total = df.count()[0]
print("共有{}支基金！".format(total))
df = df.head(total)
df_part = df[["基金代码", "基金简称", "日增长率", "近1周", "近1月", "近3月", "近半年", "近1年", "近2年", "近3年",
          "今年来", "成立来"]]#挑选部分感兴趣的条目
df.to_csv("./基金增长率.csv", encoding="utf_8_sig")

# In[]:
df_picked_part = df_part
rates = [r1r,r1z,r1y,r3y,r6y,r1n,r2n,r3n,rjnl,rcll]
i = -1
for sc in ["日增长率", "近1周", "近1月", "近3月", "近半年", "近1年", "近2年", "近3年",
          "今年来", "成立来"]:
    i = i+1
    #print(sc)
    rate = rates[i]
    rate_num = int(total*rate)
    df_tmp = df_part.sort_values(by=[sc], ascending=False, axis=0)
    df_tmp = df_tmp.head(rate_num)
    df_picked_part = pd.merge(df_picked_part,df_tmp,how='inner')
print(df_picked_part.head(10))
df_picked_part.to_csv("./4433法则结果.csv", encoding="utf_8_sig")

# In[]:
rank_codes = df_part['基金代码'].values.tolist()
#len_codes = len(rank_codes)
stocks_array = []
stock_funds = []
total_part = int(total/100)+1 #每百分之一报一次进度
for index, code in enumerate(rank_codes):
#    if index < 1:
#        print("<" * 30 + "所有基金的股票池前10情况" + ">" * 30)
#    print(code)
    if index%total_part==0:
        print("<" * 30 + "获得基金持仓数据中："+str(index)+"/"+str(total)+ ">" * 30)
    url = "http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code={}&topline=10&year=&month=&rt=0.5032668912422176".format(code)
    head = {
    "Cookie": "EMFUND1=null; EMFUND2=null; EMFUND3=null; EMFUND4=null; EMFUND5=null; EMFUND6=null; EMFUND7=null; EMFUND8=null; EMFUND0=null; st_si=44023331838789; st_asi=delete; EMFUND9=08-16 22:04:25@#$%u4E07%u5BB6%u65B0%u5229%u7075%u6D3B%u914D%u7F6E%u6DF7%u5408@%23%24519191; ASP.NET_SessionId=45qdofapdlm1hlgxapxuxhe1; st_pvi=87492384111747; st_sp=2020-08-16%2000%3A05%3A17; st_inirUrl=http%3A%2F%2Ffund.eastmoney.com%2Fdata%2Ffundranking.html; st_sn=12; st_psi=2020081622103685-0-6169905557"
    ,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"}
    response = requests.get(url, headers=head)
    text = response.text
    div = re.findall('content:\\"(.*)\\",arryear', text)[0]
    html_body = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>test</title></head><body>%s</body></html>' % (
        div)#构造网页
    html = etree.HTML(html_body)#将传进去的字符串转变成_Element对象
    stock_info = html.xpath('//div[{}]/div/table/tbody/tr/td/a'.format(season))
    # for ii in stock_info:
    #     print(ii.text)
    #print(season)
    stock_money = html.xpath('//div[{}]/div/table/tbody/tr/td[@class="tor"]'.format(season))
    if stock_money == []:
        stock_money = html.xpath('//div[{}]/div/table/tbody/tr/td[@class="toc"]'.format(season))
    stock_attr = []
    # for i in range(0,len(stock_money)):
    
    stock_money_text = []
    for ii in stock_money:
        ii_text = ii.text
 #       print(ii_text)
        if ii_text!=None:
            ii.text = ii.text.replace('---','0')
            stock_money_text.append(float(ii.text.replace(',','').replace('%','')))
    
#        print(ii.text)
   # stock_money_text.dropna()
    stock_one_fund = []
    if len(stock_info)!=0 and len(stock_money_text)!=0:
        count = -1
        for i in range(0,len(stock_info)):
            stock = stock_info[i]
            if stock.text==None:
                stock.text = '缺失'
            tmp0 = stock.text.split('.')
            tmp = tmp0[0]          
            if stock.text and (tmp.isdigit() or (tmp.isupper() and tmp.isalnum() and len(tmp0)>1)):
    #        if stock.text and stock.text.isdigit():
               # list_tmp = [stock.text,stock_info[i+1].text]
                count = count+1
                stock_one_fund.append([stock_info[i+1].text,
                                       stock_money_text[3*count+0],
                                       stock_money_text[3*count+1],
                                       stock_money_text[3*count+2]])
    #            print(stock_info[i+1].text)
#    if len(stock_one_fund)>1:
  #      print("基金代码：{}".format(code), "基金持有前10股票池", stock_one_fund)
    stock_funds.append([code,stock_one_fund])
        # print(code)
        # print(stock_one_fund)
#    else:
#        print('发现无持仓基金！')
#   if len(stock_one_fund) > 1 and stock_one_fund:
    stocks_array.extend(stock_one_fund)
print("<" * 30 + "获得基金持仓数据中：done!!!"+ ">" * 30)
# print("test")
tmp = pd.DataFrame(stock_funds,columns=['基金代码','十大重仓'])
df_funds_info_extend = pd.merge(df_part,tmp,how='inner',on='基金代码')
df_funds_info_extend.set_index('基金代码')
df_funds_info_extend.to_csv("./基金持仓.csv", encoding="utf_8_sig")


# In[]:
stock_info_list = []
for row in df_funds_info_extend.iterrows():
    tenpos = row[1]['十大重仓']
    fund_jc = row[1]['基金简称']
    if len(tenpos)!=0:
        tmp = [tenpos[0][0],fund_jc,tenpos[0][1],tenpos[0][2],tenpos[0][3]]
        stock_info_list.append(tmp)
df_stock_info = pd.DataFrame(stock_info_list,columns=['股票简称','所属基金','占净值比例','持股数_万','持仓市值_万'])
df_stock_info.to_csv("./股票被持有信息.csv", encoding="utf_8_sig")

# In[]
#df_stock_info.loc[:,['股票简称','持股数_万','持仓市值_万','占净值比例']]
df_stock_info_cp = df_stock_info
df_stock_info_cp['所属基金cp'] = df_stock_info['所属基金']
df_stock_info_gb = df_stock_info_cp.groupby('股票简称')
#df_stock_info.drop(axis=1,['所属基金'])
# for n in df_stock_info_gb:
#     print(n)
#     print('\n')
#stock_agg_result = df_stock_info_gb.agg({'持股数_万':np.sum,'持仓市值_万':np.sum,'占净值比例':np.mean})
stock_agg_result = df_stock_info_gb.agg({'持股数_万':np.sum,'持仓市值_万':np.sum,'占净值比例':np.mean,'所属基金':len,'所属基金cp':list})
stock_agg_result.columns = ['被持股数_万','被持仓市值_万','平均占比','所属基金数目','所属基金集合']
stock_agg_result.to_csv("./股票被持有信息统计.csv", encoding="utf_8_sig")
# df_stock_info_gb.to_csv("./测试.csv", encoding="utf_8_sig")

# In[]
rank = 10
stock_agg_result = stock_agg_result.sort_values(by="所属基金数目",ascending=False)
stock_agg_result_head0 = stock_agg_result.head(rank)
stock_agg_result = stock_agg_result.sort_values(by="被持仓市值_万",ascending=False)
stock_agg_result_head1 = stock_agg_result.head(rank)
stock_agg_result = stock_agg_result.sort_values(by="平均占比",ascending=False)
stock_agg_result_head2 = stock_agg_result.head(rank)
funds_stocks_count = []
for st_funds_ in stock_funds:
    #st_funds_ = stock_funds[0]
    st_funds = st_funds_[1]
    tmp = [i[0] for i in st_funds]
    df_stock_funds = pd.DataFrame(tmp,columns=['股票简称'])
#    print(df_stock_funds)
    count0 = pd.merge(stock_agg_result_head0,df_stock_funds,how='inner',on='股票简称').iloc[:,0].size
    count1 = pd.merge(stock_agg_result_head1,df_stock_funds,how='inner',on='股票简称').iloc[:,0].size
    count2 = pd.merge(stock_agg_result_head2,df_stock_funds,how='inner',on='股票简称').iloc[:,0].size
    jc_tmp = df_part[df_part['基金代码']==st_funds_[0]].iloc[0,1]
    funds_stocks_count.append([jc_tmp,count0,count1,count2])
df_funds_stock_count = pd.DataFrame(funds_stocks_count,columns = ['基金简称','优仓数目_所属基金数','优仓数目_被持仓市值','平均占比'])
df_funds_stock_count = df_funds_stock_count.sort_values(by=["优仓数目_所属基金数"], ascending=False, axis=0)
df_funds_stock_count = pd.merge(df_funds_stock_count,df_part,how='inner',on='基金简称')
df_funds_stock_count.to_csv("./基金持受欢迎股数目统计.csv", encoding="utf_8_sig")







