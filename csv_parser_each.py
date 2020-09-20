import csv
import pymysql
import os #用於獲取目標文件所在路徑

def getcon(db_name):
  # host是選擇連線哪的資料庫localhost是本地資料庫，port是埠號預設3306
  #user是使用的人的身份，root是管理員身份，passwd是密碼。db是資料庫的名稱，charset是編碼格式
  conn=pymysql.connect(host="localhost",port=3306,user='root',passwd='001240',db=db_name,charset='utf8')
  # 建立遊標物件
  cursor=conn.cursor()
  return conn,cursor

#----------------------------------------------------------------------

#連接資料庫
conn, cursor = getcon("news_data_processing")

path=os.getcwd() #資料夾夾絕對路徑
files=[] #csv檔案名稱array
for file in os.listdir(path+'/output'):  #找尋此資料夾內的所有檔案
    if file.endswith(".csv"): #排除資料夾內的其它檔案，只獲取".csv"檔
        files.append(file) 
#print(files)

#獲取當前DB內table
cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='news_data_processing'")
temp =cursor.fetchall()
table_list=[]
for x in range(0,len(temp)):
    table_list.append(temp[x][0]+".csv")
#print(table_list)

#資料夾內檔案與DB內table做差集，找出尚未歸檔之檔案
for i in range(len(files)-1,-1,-1):
    for j in range(0,len(table_list)):
        #解決DB自動小寫問題        
        if files[i].lower() == table_list[j]:
            del files[i]
            break;
#print(files)

# 開啟CSV檔案
for i in range(0,len(files)):
    schema=[]
    state=[]
    with open('./output/'+files[i], newline='',encoding="utf-8") as csvfile:
        # 讀取 CSV 檔案內容
        rows = csv.reader(csvfile)
        #將CSV內容分為schema & state
        schema=next(rows)
        schema[0]="id"
        for row in rows:
            state.append(row)
        print(schema)
        #print(state)

        #創建table
        cursor.execute("CREATE TABLE %s (%s VARCHAR(255))" %((files[i])[:-4],schema[0]))
        #加入各項attribute
        for j in range(1,len(schema)):
            cursor.execute("ALTER TABLE %s ADD %s VARCHAR(255)" %((files[i])[:-4],schema[j]))
        #引入state
        for j in range(0,len(state)):
            sql="INSERT INTO %s (%s" %((files[i])[:-4],schema[0])
            for k in range(1,len(schema)):
                sql+=",%s" %schema[k]
            sql+=") VALUES (\'%s\'" %(state[j][0])
            for l in range(1,len(state[j])):
                sql+=",\'%s\'" %(state[j][l])
            sql+=")"
            #print(sql)
            cursor.execute(sql)
            conn.commit() 
        
cursor.close()
conn.close()
print("close connection")
    
