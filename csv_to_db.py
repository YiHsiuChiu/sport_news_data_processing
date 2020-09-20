import csv
import pymysql
import os #用於獲取目標文件所在路徑
import re
import sys #用於讀取命令列參數

path=os.getcwd()+"\\data\\107\\12\\csv"
#path=sys.argv[1] #資料input路徑

#設定table名稱
table_name="data"

def getcon(db_name):
  #host是選擇連線哪的資料庫localhost是本地資料庫，port是埠號預設3306
  #user是使用的人的身份，root是管理員身份，passwd是密碼。db是資料庫的名稱，charset是編碼格式
  conn=pymysql.connect(host="localhost",port=3306,user='root',passwd='1234',db=db_name,charset='utf8')
  # 建立遊標物件
  cursor=conn.cursor()
  return conn,cursor

#----------------------------------------------------------------------

#連接資料庫
conn, cursor = getcon("news_data_processing")

files=[] #csv檔案名稱array
for file in os.listdir(path):  #找尋此資料夾內的所有檔案
    if file.endswith(".csv"): #排除資料夾內的其它檔案，只獲取".csv"檔
        files.append(file) 
#print(files)

# 開啟CSV檔案
for i in range(0,len(files)):
    schema=[]
    state=[]
    with open(path+"\\"+files[i], newline='',encoding="utf-8") as csvfile:
        # 讀取 CSV 檔案內容
        rows = csv.reader(csvfile)
        #將CSV內容分為schema & state
        #第一行為schema
        schema=next(rows)
        schema[0]="id"
        #第二行為主播，日期資訊等額外資訊
        exdate=next(rows)
        #把"主播:"截掉
        anchorman=(exdate[2])[3:]
        #date格式轉換
        temp=re.findall(r"\d+",exdate[3])
        date="";
        y=(int)(temp[0])+1911
        m=temp[1]
        d=temp[2]
        date=str(str(y)+"-"+m+"-"+d)
        #print(date)
        #資料陣列
        for row in rows:
            state.append(row)
        #print(schema)
        #print(state)

        #判斷table是否存在
        if i==0:
            sql="SHOW TABLES LIKE \'%s\'"%table_name
            cursor.execute(sql)
            result = cursor.fetchone()
            if not result:
                #創建table
                cursor.execute("CREATE TABLE %s (file_name VARCHAR(255),anchorman VARCHAR(255),date DATE ,id INT,news VARCHAR(255),reporter VARCHAR(255),title VARCHAR(255),footage VARCHAR(255),footage_sec INT,type VARCHAR(255),remark VARCHAR(255),CM INT,league VARCHAR(255))" %table_name)
        #引入state
        k=1
        for j in range(0,len(state)):
            if state[j][4]!='':
                temp=re.findall(r"\d+",state[j][4])
                sec=int(temp[0])*60+int(temp[1])
                sql="INSERT INTO %s (file_name,anchorman,date,id,news,reporter,title,footage,footage_sec,type,remark,CM,league) VALUES (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')"%(table_name,(files[i])[:-4],anchorman,date,state[j][0],state[j][1],state[j][2],state[j][3],state[j][4],sec,state[j][5],state[j][6],k,"")
            else:
                if 'CM' in state[j][3]:
                    k=k+1
                    sql="INSERT INTO %s (file_name,anchorman,date,id,news,reporter,title,footage,footage_sec,type,remark,CM,league) VALUES (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')"%(table_name,(files[i])[:-4],anchorman,date,state[j][0],state[j][1],state[j][2],state[j][3],state[j][4],0,state[j][5],state[j][6],-1,"")
                else:
                    sql="INSERT INTO %s (file_name,anchorman,date,id,news,reporter,title,footage,footage_sec,type,remark,CM,league) VALUES (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')"%(table_name,(files[i])[:-4],anchorman,date,state[j][0],state[j][1],state[j][2],state[j][3],state[j][4],0,state[j][5],state[j][6],k,"")
            #print(sql)
            cursor.execute(sql)
            conn.commit() 
        
cursor.close()
conn.close()
print("close connection")
    
