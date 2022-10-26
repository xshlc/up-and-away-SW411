import sqlite3
from datetime import datetime

class Record:
    queryParams = {}    #user entered query params
    rows = []           #store query results
    queryString = ""    #sql string
    def __init__(self,tableName):
        self.tableName = tableName
        self.conn = sqlite3.connect('database.db', check_same_thread=False, timeout=10)
        self.conn.row_factory = sqlite3.Row  # return dictionary instead of tuple
        self.cur = self.conn.cursor()

    #accepts a string of comma separated values to insert into a table. User must know table schema.
    def insert(self,arg):
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        itemsToInsert = [None, dt_string] + arg.split(',')
        numColumns = len(itemsToInsert)
        sql = f"INSERT INTO {self.tableName} VALUES (" + ",".join(numColumns * ["?"]) + ")"
        print(sql)
        self.cur.execute(sql, itemsToInsert)

    #adds query parameters to be built into sql 
    def addQuery(self,param,value):
        self.queryParams.update({param:value})

    #builds SQL select statement from list of queries. Currently only support AND operations
    def queryBuilder(self):
        self.queryString = f"SELECT * FROM {self.tableName} "
        if len(self.queryParams) > 0:
            self.queryString +="WHERE "
            for index, key in enumerate(self.queryParams):
                self.queryString += f"{key} = \'{self.queryParams[key]}\'"
                if index != len(self.queryParams) - 1:
                    self.queryString += " AND WHERE "
    
    #queries a DB table and stores all matching results to rows
    def query(self):
        self.queryBuilder()
        print(self.queryString)
        self.cur.execute(self.queryString)
        self.rows = self.cur.fetchall()
        self.queryParams = {}

    #returns a generator object of query results
    def results(self):
        for row in self.rows:
            yield dict(row)

    def commit(self):
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

    





