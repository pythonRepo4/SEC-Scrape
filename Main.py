from urllib import request
import os
import Utility
import scrapHTML
import Download
        
"""Downloads 10ks if not in directory """
def download(tickerName, year):
    directory = str(os.getcwd()) + "\\html-files\\" 
    fileName = directory + tickerName + "-10k-" + year + ".html"
    
    if(os.path.isfile(fileName) == False):
        Download.documentList(tickerName, year)
    
"""Returns all tables on 10-k """
def getAllTables(tickerName, year):
    download(tickerName, year)
    titles, tables = scrapHTML.getAllTables(tickerName, year)
    
    for i in range(0, len(titles)):
        print(titles[i])
        Utility.makeTable(tables[i])

"""Attempts to find Consolidated Statements of Income/Earnings, Consolidated Balance Sheets,
and Consolidated Statements of Cash Flows """
def getConsolidatedFinancials(tickerName, year):
    print("Consolidated Financial Statements")
    print(tickerName + " : " + str(year))
    download(tickerName, year)
    titles, tables = scrapHTML.getAllTables(tickerName, year)
    if(titles == None or tables == None):
        print("Could not download tables")
        return

    print("")
    
    for i in range(0, len(tables)):
        title = titles[i]
        table = tables[i]
        
        """Sometimes title is in first row of table. If "Consolidated" is in, move it to title """
        for j in table:
            row = Utility.combineSingleArray(j)
            if("consolidatedbalance" in row.lower().replace(" ","") or "consolidatedstatemen" in row.lower().replace(" ","")):
                title = title + row
                titles[i] = title
                break
        
        tableVars = ""
        for j in table:
            for k in j:
                tableVars += k
        tableVars = tableVars.lower().replace(" ", "")
        title = title.lower().replace(" ", "")
        
        """Consolidated Statements of Income/Earnings"""
        match = ["Revenues", "Net Sales", "Gross", "Operat", "Interest Expense", "Income Taxes", "Net Income", "Net Earnings"]
        if("consolidatedstatement" in title and Utility.matches(tableVars, match) == True):
            print("Possible Consolidated Statements of Income/Earnings: ")
            Utility.makeTable(table)
        
        """Consolidated Balance Sheets"""
        match = ["assets", "liabilities", "equity"]
        if("consolidatedbalance" in title and Utility.matches(tableVars, match) == True):
            print("Possible Consolidated Balance Sheets: ")
            Utility.makeTable(table)
            
        """Consolidated Statements of Cash Flows"""
        match = ["Adjustments", "Operating", "Investing", "Financ"]
        if("consolidatedstatement" in title and "cashflows" in title and Utility.matches(tableVars, match) == True):
            print("Possible Consolidated Cash Flows: ")
            Utility.makeTable(table)
        

"""
Example:
getAllTables("AAPL", "2015")
Get all tables in the 10k.

getConsolidatedFinancials("AAPL", "2015")
Get GAAP consolidated statement of income, consolidated balance sheets, consolidated statements of cash flows


"""



