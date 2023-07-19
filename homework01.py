import requests
import re
import pymysql.cursors
import xlwt

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
           }
url = "https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery1123011199533951932761_1689732571763&sortColumns=HOLD_NOTICE_DATE%2CSECURITY_CODE&sortTypes=-1%2C-1&pageSize=50&pageNumber=%d&reportName=RPT_HOLDERNUMLATEST&columns=SECURITY_CODE%2CSECURITY_NAME_ABBR%2CEND_DATE%2CINTERVAL_CHRATE%2CAVG_MARKET_CAP%2CAVG_HOLD_NUM%2CTOTAL_MARKET_CAP%2CTOTAL_A_SHARES%2CHOLD_NOTICE_DATE%2CHOLDER_NUM%2CPRE_HOLDER_NUM%2CHOLDER_NUM_CHANGE%2CHOLDER_NUM_RATIO%2CEND_DATE%2CPRE_END_DATE&quoteColumns=f2%2Cf3&quoteType=0&source=WEB&client=WEB"
list = []
for pageNum in range(1,5):
    #new_url = format(url%pageNum)
    new_url = f"https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery1123011199533951932761_1689732571763&sortColumns=HOLD_NOTICE_DATE%2CSECURITY_CODE&sortTypes=-1%2C-1&pageSize=50&pageNumber={pageNum}&reportName=RPT_HOLDERNUMLATEST&columns=SECURITY_CODE%2CSECURITY_NAME_ABBR%2CEND_DATE%2CINTERVAL_CHRATE%2CAVG_MARKET_CAP%2CAVG_HOLD_NUM%2CTOTAL_MARKET_CAP%2CTOTAL_A_SHARES%2CHOLD_NOTICE_DATE%2CHOLDER_NUM%2CPRE_HOLDER_NUM%2CHOLDER_NUM_CHANGE%2CHOLDER_NUM_RATIO%2CEND_DATE%2CPRE_END_DATE&quoteColumns=f2%2Cf3&quoteType=0&source=WEB&client=WEB"
    page_text = requests.get(url=new_url,headers=headers).text
    ex1 = '.*?"SECURITY_CODE":"(.*?)","SECURITY_NAME_ABBR":"(.*?)".*?"f2":(.*?),.*?'
    stage = re.findall(ex1,page_text,re.S)
    list = list+stage

new_list = []
# for i in list:
#       new_list.append(i.replace(""-"","0"))
nums = len(list)
print(list[0])


#连接数据库
connect = pymysql.Connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='hyb06059454',
    db='hyb',
    charset='utf8'
)

#获取游标
cursor = connect.cursor()
#创建表格
sql = "CREATE TABLE stock(id INTEGER PRIMARY KEY,number INTEGER,name TEXT,fate FLOAT)"
try:
    cursor.execute(sql)
    connect.commit()
except:
    print("表已存在")
print('成功创建表格')
#插入数据
sql = "INSERT INTO stock VALUES(%d,%d,'%s',%f)"
for num in range(0,nums):
    place0 = int(list[num][0])
    place1 = str(list[num][1])
    if list[num][2]=='"-"':
        place2 = 0
    else:
        place2 = float(list[num][2])
    data = (int(num)+1,place0,place1,place2)
    cursor.execute(sql % data)
    connect.commit()
    print('成功插入', cursor.rowcount, '条数据')
    



