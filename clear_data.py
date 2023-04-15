import pandas as pd
data=pd.read_excel('data.xlsx')
data['降水量']=data['降水量'].fillna(0)
data[['最高温度','最低温度']]=data[['高温','低温']].apply(lambda col:[x.replace('℃','') for x in col])
data['风级']=data['风向'].apply(lambda x:x.split('风')[-1].split('级')[0])
data.to_excel('./echarts/predata.xlsx',index=False)