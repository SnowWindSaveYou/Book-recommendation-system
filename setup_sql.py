# try to connect sql
import pymysql
import pandas as pd
import os
import csv

HOST = "127.0.0.1"
PORT = 3306
USER = 'root'
PASS = "12345678"
DB = "bookrs"

class CsvToMysql(object):
    def __init__(self, hostname, port, user, passwd, db):
        self.dbname = db
        self.conn = pymysql.connect(host=hostname, port=port, user=user, passwd=passwd, db=db)
        self.cursor = self.conn.cursor()
 
 
    def read_csv(self,filename,indexcol=None):
        df = pd.read_csv(filename, keep_default_na=False, encoding='utf-8')
        try:
            df.drop(['id'],axis=1,inplace=True)
        except:
            pass
        
        table_name = '`'+os.path.split(filename)[-1].split('.')[0].replace(' ', '_') + '`'
        self.csv2mysql(db_name=self.dbname,table_name=table_name, df=df, col_index = indexcol)
 
    def read_dataframe(self,table_name, dataframe,indexcol=None):
        table_name = '`'+table_name+ '`'
        self.csv2mysql(db_name=self.dbname,table_name=table_name, df=dataframe, col_index = indexcol)
    
 
    def make_table_sql(self,df,col_index):
        columns = df.columns.tolist()
        types = df.ftypes
        make_table = []
        make_field = []
        if col_index == None:
            print('none index')
            make_table.append('id INT')
        for item in columns:
            if item ==col_index:
                item1 = item.replace(' ', '_').replace(':','')
            else:
                item1 = '`'+item.replace(' ', '_').replace(':','')+'`'
                
            if 'int' in types[item]:
                char = item1 + ' INT'
            elif 'float' in types[item]:
                char = item1 +' FLOAT'
            elif 'object' in types[item]:
                char = item1 +' VARCHAR(1000)'
            elif 'datetime' in types[item]:
                char = item1 + ' DATETIME'
            else:
                char = item1 + ' VARCHAR(400)'
            #char = item1 + ' VARCHAR(255)'
            make_table.append(char)
            make_field.append(item1)

#         return ','.join(make_table), ','.join(make_field)
        return make_table,make_field

    def csv2mysql(self,db_name,table_name,df, col_index):
        make_table, make_field = self.make_table_sql(df,col_index)

        field1 = ','.join(make_table[1:])
        field2 = ','.join(make_field)
        
        print("create table {} ({} AUTO_INCREMENT not null primary key, {})".format(table_name,make_table[0],field1))
        self.cursor.execute('drop table if exists {}'.format(table_name))
        self.cursor.execute("create table {} ({} AUTO_INCREMENT not null primary key,{})".format(table_name,make_table[0],field1))
        values = df.values.tolist()
        s = ','.join(['%s' for _ in range(len(df.columns))])
        try:
            print(len(values[0]),len(s.split(',')))
            print('insert into {}({}) values ({})'.format(table_name, field2, s), values[0])
#             if col_index == None:
#                 self.cursor.executemany('insert into {}({}) values ({})'.format(table_name, field2, s), values)
#             else:
            self.cursor.executemany('insert into {}({}) values ({})'.format(table_name, field2, s), values)
            
        except Exception as e:
            print("Exception",e)
        finally:
            self.conn.commit()

def if __name__ == "__main__":
    M = CsvToMysql(hostname=HOST, port=PORT, user=USER, passwd=PASS, db=DB)
    rating_df = pd.read_csv('./book-data/ratings.csv', header = 0)
    user_df = rating_df.groupby('user_id')['user_id'].agg(['count']).reset_index()

    M.read_dataframe("users", user_df,indexcol="user_id")
    M.read_dataframe("rating_record", rating_df)
    M.read_csv('./book-data/books.csv','book_id')