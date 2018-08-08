from urllib import request
import os
import Utility
import scrapHTML
import Download
import opLease
from SQL import SQLMethods
        
"""Downloads 10ks if not in directory """
def download(tickerName, year):
    directory = str(os.getcwd()) + "\\html-files\\" 
    fileName = directory + tickerName + "-10k-" + year + ".html"
    
    if(os.path.isfile(fileName) == False):
        Download.documentList(tickerName, year)
    
def getAllTables(tickerName, year):
    download(tickerName, year)
    titles, tables = scrapHTML.getAllTables(tickerName, year)
    
    for i in range(0, len(titles)):
        print(titles[i])
        Utility.makeTable(tables[i])

def getConsolidatedFinancials(tickerName, year):
    print(tickerName + ' : ' + str(year))
    download(tickerName, year)
    try:
        titles, tables = scrapHTML.getAllTables(tickerName, year)
    except:
        return
    
#     if(titles == None or tables == None):
#         return
#     
#     consolidatedIncome = [["Net Sales", 0],
#                          ["Gross Margin", 0],
#                          ["Operating Income", 0],
#                          ["Interest Expense", 0],
#                          ["Income Taxes", 0],
#                          ["Net Income", 0 ] ] 
#     
#     consolidatedBalance = [["Shareholders Equity", 0],
#                            ["Preferred", 0] ]
#     
#     for i in range(0, len(tables)):
#         title = titles[i]
#         table = tables[i]
#         
#         """Sometimes title is in first row of table. If "Consolidated" is in, move it to title """
#         for j in table:
#             row = Utility.combineSingleArray(j)
#             if("consolidatedbalance" in row.lower().replace(" ","") or "consolidatedstatemen" in row.lower().replace(" ","")):
#                 title = title + row
#                 titles[i] = title
#                 break
#         
#         tableVars = ""
#         for j in table:
#             for k in j:
#                 tableVars += k
#         tableVars = tableVars.lower().replace(" ", "")
#         title = title.lower()
#         
#         """
#         --------Consolidated Statements of Income-----------
#         Get the following data: 
#         Revenues, Net Sales, Total Sales, 
#         Gross Profit
#         Operating Income
#         Income Taxes
#         Net Income, Net Earnings
#          """
# 
#         match = ["Revenues", "Net Sales", "Gross", "Operat", "Interest Expense", "Income Taxes", "Net Income", "Net Earnings"]
#         if("consolidated statement" in title and Utility.matches(tableVars, match) == True):
#             Utility.makeTable(table)
#             for j in table:
#                 wholeRowInText = ""
#                 for k in j:
#                     wholeRowInText += k 
#                 wholeRowInText = wholeRowInText.lower().replace(" ", "")
#                 
#                 rowTitle = j[0].lower().replace(" ", "")
# #                 print("interest" in rowTitle and "expense" in rowTitle)
#                                 
#                 """Revenue/Net Sales should be an exact match"""
#                 rowMatch = ["Revenues", "Total Revenues", "Net Sales", "Total Operating Revenue", "Operating Revenue"]
#                 if(Utility.singleMatch(rowTitle, rowMatch) == True):
#                     columnIndex = 1
#                     while(columnIndex < len(j)):
#                         try:
#                             consolidatedIncome[0][1] = float(j[columnIndex].replace(",", ""))
#                             columnIndex = len(j) + 5
#                         except:
#                             columnIndex += 1
#                     continue
#                               
#                 """Gross"""
#                 if("gross" in rowTitle):
#                     columnIndex = 1
#                     while(columnIndex < len(j)):
#                         try:
#                             consolidatedIncome[1][1] = float(j[columnIndex].replace(",", ""))
#                             columnIndex = len(j) + 5
#                         except:
#                             columnIndex += 1
#                     continue
#                  
#                 """Operating Income """
#                 if("income" in rowTitle and "operat" in rowTitle):
#                     columnIndex = 1
#                     while(columnIndex < len(j)):
#                         try:
#                             consolidatedIncome[2][1] = float(j[columnIndex].replace(",", ""))
#                             columnIndex = len(j) + 5
#                         except:
#                             columnIndex += 1
#                     continue
#  
#                 """Interest Expense"""
#                 rowMatch = ["Interest", "Expense"]
#                 if("interest" in rowTitle and "expense" in rowTitle):
#                     columnIndex = 1
#                     while(columnIndex < len(j)):
#                         try:
#                             consolidatedIncome[3][1] = float(j[columnIndex].replace(",", ""))
#                             columnIndex = len(j) + 5
#                         except:
#                             columnIndex += 1
#                     continue
# 
#                 """Net Earnings / Net Income"""
#                 rowMatch = ["Net Earnings", "Net Income"]
#                 if(Utility.singleMatch(rowTitle, rowMatch) == True):
#                     columnIndex = 1
#                     while(columnIndex < len(j)):
#                         try:
#                             consolidatedIncome[5][1] = float(j[columnIndex].replace(",", ""))
#                             columnIndex = len(j) + 5
#                         except:
#                             columnIndex += 1
#                     continue                       
          
#     for i in consolidatedIncome:
#         print(i)
        
#         match = ["assets", "liabilities", "equity"]
#         if("consolidated balance" in title and Utility.matches(tableVars, match) == True):
#             Utility.makeTable(table)
#             for j in table:
#                 wholeRowInText = ""
#                 for k in j:
#                     wholeRowInText += k 
#                 wholeRowInText = wholeRowInText.lower().replace(" ", "")
#                 rowTitle = j[0].lower().replace(" ", "")
#     
#                 """Revenue/Net Sales should be an exact match"""
#                 rowMatch = ["Total Equity", "Total Stockholders Equity", "Total Shareholders Equity", "Operating Revenue",
#                             "Shareholders Equity", "Stockholders Equity", "Total Shareholders' Equity", "Total Stockholders' Equity"]
#                 if(Utility.singleMatch(rowTitle, rowMatch) == True):
#                     columnIndex = 1
#                     while(columnIndex < len(j)):
#                         try:
#                             consolidatedBalance[0][1] = float(j[columnIndex].replace(",", ""))
#                             columnIndex = len(j) + 5
#                             print(consolidatedBalance([0][1]))
#                         except:
#                             columnIndex += 1
#                     continue
#                 
#                 if("preferred" in rowTitle):
#                     columnIndex = 1
#                     while(columnIndex < len(j)):
#                         try:
#                             consolidatedBalance[1][1] = float(j[columnIndex].replace(",", ""))
#                             columnIndex = len(j) + 5
#                             print(consolidatedBalance([0][2]))
#                         except:
#                             columnIndex += 1
#                     continue
#                     
#     for i in consolidatedBalance:
#         print(i)
                    
#         match = ["Current Assets"] 
    
#             print(title)
#             Utility.makeTable(table)
            
#         if("consolidated" in title and "balanc" in title):
#             print(title)
#         print(title)
#         print(Utility.makeTable(table))

        """Consolidated Income"""
#         match = ["income", "tax", "net", "sales", "interest"]
#         titleMatch = ["Consolidated statement of Income", "Consolidated Statement of Operat", "Consolidated Statements of Income", "Consolidated Statements of Operat",
#                       "Consolidated Statements of Earning", "Consolidated Income Statement", "consolidated Statements of Net Income", "Statements of Consolidated Operations",
#                       "CONDENSED STATEMENTS OF EARNINGS AND COMPREHENSIVE EARNINGS", "consolidated statements of comprehensive income"]
#         if(Utility.titleMatch(title, titleMatch) == True
#             and Utility.matches(tableVars, match) == True):
#             consolidatedIncome = i
#              
#              
#         """Consolidated Balance Sheets"""
#         match = ["asset", "cash" , "equity", "inventor"]
#         titleMatch = ["Consolidated Balance Sheet", "Consolidated Balance Sheets", "Consolidated Statements of Condition", "CONDENSED BALANCE SHEETS"]
#         if(Utility.titleMatch(title, titleMatch) == True
#              and Utility.matches(tableVars, match) == True):
#             consolidatedBalanceSheets = i
#              
#      
#         """Consolidated Cash Flows"""
#         match = ["depreciation", "amortization", "adjustments", "net", "cash"]
#         titleMatch = ["Consolidated Statement of Cash Flow", "Consolidated Statements of Cash Flows", "Consolidated Statements of Cash Flow",
#                       "Statements of Consolidated Operations", "CONDENSED STATEMENTS OF CASH FLOWS"]
#         if(Utility.titleMatch(title, titleMatch) == True
#            and Utility.matches(tableVars, match) == True):
#             consolidatedCashFlow = i
#              
#     if(consolidatedCashFlow == -1 or consolidatedBalanceSheets == -1 or consolidatedIncome == -1):
#         print(str(tickerName) + " : " + str(year))
#         if(consolidatedIncome != -1):
#             print("Title = " + str(titles[consolidatedIncome]))
#     #         Utility.makeTable(tables[consolidatedIncome])
#             print("Consolidated Income Good")
#         else:
#             print("Consolidated Income Not Found")
#           
#         if(consolidatedBalanceSheets != -1):
#             print("Title = " + str(titles[consolidatedBalanceSheets]))
#     #         Utility.makeTable(tables[consolidatedBalanceSheets])
#             print("Consolidated Balance Sheets Good")
#         else:
#             print("Consolidated Balance Sheets Not Found")
#             
#         if(consolidatedCashFlow != -1):
#             print("Title = " + str(titles[consolidatedCashFlow]))
#     #         Utility.makeTable(tables[consolidatedCashFlow])
#             print("Consolidated Cash Flows Good")
#         else:
#             print("Consolidated Cash Flows Not Found")
#         print(" ")


                
#             """IF lease Commitment is empty """
#             if(len(leaseCommitment) < 1):
#                 for k in range(1, len(table[0])):
#                     temp = ""
#                     temp += table[0][k].lower()
#                     temp += table[1][k].lower()
#                     
#                     tempLease = []
#                     if("leases" in temp and "capitalize" not in temp):
#                         for j in table:
#                             print(j[k])
#                             tempLease.append(j[k])
#                     if(len(tempLease) > 0):
#                         leaseCommitment.append(tempLease)
#                 
#                 
#                 
#             
#             
#             
#                 
#                 
#             for k in leaseCommitment:
#                 print(k)
        
#             for k in range(0, len(table[0])):
#                 temp = ""
#                 temp += table[0][k].lower()
#                 temp += table[1][k].lower()
#                 if("total" in temp):
#                     totalIndex = k 
#             
#             for i in leaseCommitment:
#                 print(table[i][k])        
            
#             """If nothing in leaseCommitment, leases is probably on columns """
#             if(len(leaseCommitment) < 1): 
                



list = ["MSFT"]
for i in list:
    print(i)
    for j in range(2012, 2018):
        download(i,str(j))
        op = opLease.opLease(i, str(j))
        print(op)
        if(op == None):
            continue
        SQLMethods.insertDebt(i, j, op)
        
# print("hi") 
# for i in SQLMethods.getAll():
#     print(i)



