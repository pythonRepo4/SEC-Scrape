import sqlite3
import os

def execute(commands, input = None):
    directory = "D:\\Eclipse Library\\SEC_Scrape\\SQL\\SECdata.db"

    conn = sqlite3.connect(directory)
    c = conn.cursor()
    
    if(input == None or input == False):
        c.execute(commands)
    else:
        c.execute(commands,input)
    
    conn.commit()
    conn.close()


def executeReturn(commands):
    directory = "D:\\Eclipse Library\\SEC_Scrape\\SQL\\SECdata.db"
    returnArray = []
    conn = sqlite3.connect(directory) 
    c = conn.cursor()
    
    cursor = c.execute(commands)
    
    for i in cursor:
        returnArray.append(i)
    
    conn.commit()
    conn.close()
    
    return returnArray    
