from SQL import sqlite as sql

"""-----------------------------------------------------------------------------------
Returns earnings data from EarningsData.db
-----------------------------------------------------------------------------------"""
def getDebtData(tickerName, year):   
    try:
        tableName = tickerName + "_debt_" + str(year)
        tempData = sql.executeReturn('SELECT * FROM ' + tableName)
        return tempData[0]
    except:
        return None

def returnTable(tableName):
    try:
        tempData = sql.executeReturn('SELECT * FROM ' + tableName)
        return tempData[0]
    except:
        return None  


"""-----------------------------------------------------------------------------------
Insert Operating Lease commitments as tickername, year, [y1, y2, y3, y4, y5, all others]
-----------------------------------------------------------------------------------"""
def insertDebt(tickerName, year, data):
    tableName = tickerName + "_debt_" + str(year)
    sql.execute("DROP TABLE IF EXISTS " + tableName , None)
    sql.execute('CREATE TABLE ' + tableName + "(y1 REAL, y2 REAL, y3 REAL, y4 REAL, y5 REAL, y6 REAL)", None)
    sql.execute("INSERT INTO " + tableName + " VALUES (?,?,?,?,?,?)" , data)
    
    
"""-----------------------------------------------------------------------------------
 getAll will return all tables currently in HistoricalPrices.db. 
 removeTicker will remove that table from the database. 
-----------------------------------------------------------------------------------"""
def getAll():
    allTables = sql.executeReturn("SELECT name FROM sqlite_master WHERE type = 'table';")
    return allTables

def deleteTicker(tickerName):
    sql.execute('DROP TABLE IF EXISTS ' + tickerName, None)
    

# 
# list = ["MSFT"]
# for i in list:
#     for j in range(2012,2018):
#         print(getDebtData(i, str(j)))