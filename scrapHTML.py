from bs4 import BeautifulSoup
import os
import Utility

def htmlTable(html, rowTagInput, columnTagInput):
    rowTag = "<" + rowTagInput
    endTag = "</" + rowTagInput + ">"
    columnTag = "<" + columnTagInput 
    columnEnd = "</" + columnTagInput + ">"

    row = ""
    table = []
    title = ""
    for i in html.splitlines():
        if(rowTag in i):
            title = row
            row = ""
            continue
        
        """Found end of row. Now get each cell by going through columns """
        if(endTag in i):
            rowArray = []
            tempCell = []
            blank = 0
            for j in row.splitlines():
                if(columnTag in j):
                    subString = 'colspan="'
                    if(subString in j):
                        index = j.find(subString) + len(subString)
                        payload = j[index:]
                        blank = int(payload.split('"')[0]) - 1
                    continue
                
                if(j == columnEnd):
                    joinedCells = ""
                    for k in tempCell:
                        joinedCells +=k + " "
                    rowArray.append(joinedCells)
                    for i in range(0,blank):
                        rowArray.append("")
                    blank = 0

                    tempCell = []
                    continue

                tempCell.append(j)
            """Reset row for outer loop """   
            row = ""
            table.append(rowArray)
            continue
                    
        row += i + "\n"
    
    """Delete All Tags, Strip() [remove trailing spaces] from all cells. Remove dollar ($) signs  """
    for i in table:
        for j in range(0,len(i)):
            i[j] = Utility.deleteAllTags(i[j]).strip().replace("$", "") 

        
    """Delete if row is empty or filled with empty strings"""
    i = 0
    while(i < len(table)):
        if(len(table[i]) < 1): 
            del table[i]
            continue
              
        row = table[i]
        empty = True
        for j in row:
            if(j.strip() != ""):
                empty = False
                 
        if(empty == True):
            del table[i]
            i -= 1  
        i += 1
                
    """If there is a problem with first two rows, fix it. EX 
    row 1: cell, cell, ......
    row 2:     ,     , cell , cell                           Merges into one row"""
    if(len(table) > 2):
        if(len(table[0]) > len(table[1])):
            endOfFirst = len(table[0]) - len(table[1])
            allEmpty = True
            
            for i in range(len(table[1]), len(table[0])):
                if(table[0][i].strip() != ""):
                    allEmpty = False
                    
            if(allEmpty == True):
                for i in range(0, endOfFirst):
                    table[1].insert(0,"")

#     for i in table:
#         print(len(i))
#         print(i)
    
    """Make all table the same length """
    longestLength = 0
    for i in table:
        if(len(i) > longestLength):
            longestLength = len(i)

    for i in table:
        while(len(i) < longestLength):
            i.append("")
    
    if(len(table) < 1):
        return

    """ If it has %, ), comma [,] , or $, join right or left """ 
    for row in table:
        columnIndex = 0 
        while(columnIndex < len(row)):
            
            if(row[columnIndex].strip() == ")" or row[columnIndex].strip() == "%" or row[columnIndex].strip() == ")%"
               or row[columnIndex].strip() == ","):
                tempIndex = columnIndex - 1
                
                """If ), % or )% found, make index go left until it hits a number. If empty spaces keeps going back. """ 
                while(row[tempIndex] == ""):
                    tempIndex -= 1    
                row[tempIndex] = row[tempIndex].strip() + row[columnIndex].strip()
                row[columnIndex] = ""
                
            if(row[columnIndex].strip() == "$"):
                row[columnIndex] = row[columnIndex].strip() + row[columnIndex+1].strip()
                row[columnIndex + 1] = ""
           
            columnIndex += 1
            
    """Delete empty columns """
    keepColumns = []
    for columnIndex in range(0,len(table[0])):
        empty = 0
        for row in table:
            cell = row[columnIndex].strip()
            if(cell == ""):
                empty += 1
                continue
        """If all empty, do not keep """
        if(empty == len(table)):
            continue
        keepColumns.append(columnIndex)
        
    new = []
    for row in table:
        temp = []
        for columnIndex in range(0, len(row)):
            if(columnIndex in keepColumns):
                temp.append(row[columnIndex])
        new.append(temp)
    
    table = new 
    
    """Delete empty rows""" 
    new = []
    for row in table:
        empty = 0
        for cell in row:
            if(cell == ""):
                empty += 1
             
        if(empty == len(row)):
            continue
        new.append(row)
     
    table = new
            
    
    """If column is spit into two, merge to one. 
    etc:
    x
    5
    4
        3
        3
    
    Merge this into one column. Other condition is the right column wouldn't have a title. 
    """
    indexColumn = len(table[0]) - 1
    while(indexColumn > 0):
        fitIn = True
        for row in table:
            """Compare indexColumn to indexColumn - 1. If it cannot merg, fitIn is false"""   
            if(row[indexColumn - 1] != "" and row[indexColumn] != ""):
                fitIn = False
                break
            
        """If indexColumn and indexColumn - 1 can merge, merge them and delete indexColumn - 1 """
        if(fitIn == True):
            for row in table:
                if(row[indexColumn] != ""):
                    row[indexColumn-1] = row[indexColumn]
                
                del row[indexColumn]
            
        indexColumn -= 1
        
    """Remove extra spaces"""
    for i in range(0, len(table)):
        for j in range(0, len(table[i])):
            table[i][j] = Utility.removeExtraSpaces(table[i][j])
            

#     Utility.makeTable(table)   
#     for i in table:
#         print(len(i))
#         print(i)
#     print("*****************")
    return table

def findTableTitle(html, index):
    """Get all text for 150 lines back or until a table is hit """
#     print("*****************************************")
#     for i in range(0,50):
#         print(html[index-50+i])
#     print("END")
      
    start = index
    textInFont = ""
    while(True):
        tempLine = html[start].strip()
        """If lines hits end of another table, break."""
        if((textInFont != "" and "</table" in tempLine) or "page-break" in tempLine):
            break
        
        if("<b>" in tempLine or "bold" in tempLine):
            endTag = Utility.returnEndTag(tempLine)
            indexT = start + 1
            temp = html[indexT].strip()
            while(endTag not in temp):
                if(temp == ""):
                    indexT += 1
                    temp = html[indexT].strip()
                    continue   
                
                if(temp[0] == "<"):
                    indexT += 1
                    temp = html[indexT].strip()
                    continue   
                
                textInFont += temp + " "
                indexT += 1
                if(indexT >= index):
                    break
                temp = html[indexT].strip()
                
        if(("consolidated" in tempLine.lower() or "consolidated balance" in tempLine.lower())
           and len(tempLine) < 100):
            textInFont += tempLine + " "
        
        start -= 1
        """Go back a maximum of 50 lines"""
        if(start < index - 50):
            break
    
    return textInFont

"""Finds "\\x in line, replaces it with a '-' """
def removeUTFChar(line):
    """Replace \\xc or \\xe with - """
    while("\\xc" in line or "\\xe" in line):
        index = -1
        try:
            index = line.index("\\xc")
        except:
            pass
        if(index < 0):
            index = line.index("\\xe")
        line = line[:index] + "  " + line[index+4:]
    
    """Remove \\x00 """
    while("\\x" in line or "\\x" in line):
        index = line.index("\\x")
        line = line[:index-1] + line[index+4:]
    
    return line 
 
def getAllTables(tickerName, year):   
    directory = str(os.getcwd()) + "\\html-files\\" 
    fileName = directory + tickerName + "-10k-" + year + ".html"
    
    try:
        file = open(fileName, 'r').read()
    except:
        return None, None
    html = BeautifulSoup(file, "lxml").prettify()
    htmlLines = html.splitlines()
    html = []
    
    """Encode html into "utf-8. Anything that cannot be encoded in manually converted to approximate character  """
    for i in range(0, len(htmlLines)):
        temp = str(htmlLines[i].encode("utf-8", "ignore")).strip()
        """At this point, temp has b' at front and ' at end """
        temp = temp[2:len(temp)-1]
        temp = removeUTFChar(temp)
        temp = temp.replace("&amp;", "&")
        temp = temp.strip()
        html.append(temp)
    
    """Tables has [title, table] """
    tables = []
    titles = []
    tempTable = ""
    tempTitle = ""
    tempHTML = ""
    """Find all table tags. Everything inside table tags. Ignore all other tags other than <table and </table"""
    for i in range(0, len(html)): 
#         text = html[i]
#         if("<b>" in text or "bold" in text):
#             for j in range(1, 50):
#                 boldText = html[i + j].lower()
#                 if("independent" in boldText and "registered" in boldText and "accounting" in boldText):
#                     print(tickerName + " : " + str(year) + " : " + "TRUE")
#                     return
        if("<table" in html[i]):
            tempTitle = findTableTitle(html,i).lower()
            if("consolidated" in tempTitle):
                tempTitle = tempTitle[tempTitle.find("consolidated"):]
            continue
  
        if("</table" in html[i]):
            tempTable = htmlTable(tempHTML ,"tr", "td")
              
            if(tempTable != None and len(tempTable) > 3):
                tables.append(tempTable)
                titles.append(tempTitle)
#                 print(tempTitle)
#                 Utility.makeTable(tempTable)
                tempTitle = ""
            tempHTML = ""
            continue
          
        tempHTML += html[i] + "\n"
         
    """-------------------------------------------------------
    Sometimes tables get split into two because they span over two pages. 
    Join tables if they have similar first rows. Go forward in a two array chain and
    compare first two rows. 
    -------------------------------------------------------"""
    i = 0
    while(i < len(tables)):
        first = Utility.combineArray(tables[i-1][0]).lower().strip()
        firstLength = len(tables[i-1][0])
        firstTitle = titles[i-1].lower()
          
        second = Utility.combineArray(tables[i][0:2]).lower().strip()
        secondLength = len(tables[i][0])
        secondTitle = titles[i].lower()
        continuedInTitle = False
        if("(continue" in second.lower() or "(continue" in secondTitle):
            continuedInTitle = True
          
#         print(firstTitle + " : " + secondTitle)
#         print(str(firstLength) + " : " + str(secondLength))
        if(firstLength == secondLength and continuedInTitle == True):
            tables[i-1] = tables[i-1] + tables[i]
            del tables[i]
            del titles[i]
            i -= 1
          
        i += 1
        continueInTitle = False
      
 
    return titles, tables

def foundConsolidated(tickerName, date):
    titles, tables = getAllTables(tickerName, date)
    if(titles == None or tables == None):
        return False
    consolidatedStatement = False
    consolidatedBalance = False
    
    for i in range(0, len(tables)):
        title = titles[i]
        table = tables[i]
        
        """Sometimes title is in first row of table. If "Consolidated" is in, move it to title """
        for j in table:
            row = Utility.combineSingleArray(j)
            if("consolidated" in row.lower().replace(" ","")):
                title = title + row
                titles[i] = title
                break
            
        title = title.lower().replace(" ", "")
        
        if("consolidatedstatement" in title):
            consolidatedStatement = True
            
        if("consolidatedbalance" in title):
            consolidatedBalance = True
            
    if(consolidatedStatement == True and consolidatedBalance == True):
        return True
    return False



# list = ['ALGT', 'AHGP', 'ARLP', 'GOOGL', 'AMWD', 'AMGN', 'ANSS', 'AAPL', 'ATRI', 'OZRK', 'BIIB', 'BOFI', 'CBOE', 'CERN', 'CTSH', 'CPRT', 'CACC', 'DORM', 'EGBN', 'EBIX', 'EXPO', 'FFIV', 'FB', 'FAST', 'FFIN', 'GNTX', 'THRM', 'GILD', 'GBCI', 'HNNA', 'HSIC', 'IDXX', 'ISRG', 'IPGP', 'JBHT', 'JKHY', 'LKFN', 'MANH', 'MKTX', 'EGOV', 'NFBK', 'ODFL', 'ORLY', 'ORIT', 'PRXL', 'PSMT', 'QCOM', 'ROST', 'SEIC', 'SFBS', 'SWKS', 'SYNT', 'TROW', 'TLGT', 'TCBI', 'TXRH', 'CAKE', 'ULTA', 'UTMD', 'WASH', 'WDFC', 'WINA', 'ACN', 'AYI', 'AMP', 'APH', 'AZO', 'CHE', 'CMG', 'CHD', 'CMI', 'DG', 'DPZ', 'DCI', 'FDS', 'GPS', 'GPC', 'HXL', 'HD', 'HRL', 'KNX', 'LCI', 'MMP', 'MMS', 'MCO', 'MSM', 'NEU', 'NKE', 'NUS', 'PII', 'PRLB', 'RHT', 'RMD', 'ROL', 'SBH', 'SNA', 'LUV', 'TJX', 'TMK', 'TYL', 'UVE', 'USNA', 'GWW', 'WDR', 'DIS', 'WAB', 'WLK', 'MMM', 'ABT', 'ABBV', 'ATVI', 'ADBE', 'AAP', 'AFL', 'ALK', 'ALXN', 'MO', 'AMZN', 'AIG', 'ADI', 'AMAT', 'ADSK', 'AVY', 'BCR', 'BAX', 'BBBY', 'BBY', 'HRB', 'BA', 'BMY', 'AVGO', 'CHRW', 'CA', 'CELG', 'CB', 'CINF', 'CTAS', 'CSCO', 'CTXS', 'CLX', 'COH', 'CL', 'COST', 'DLPH', 'DAL', 'DFS', 'DLTR', 'DPS', 'DD', 'DNB', 'EMR', 'EL', 'EXPE', 'EXPD', 'FITB', 'FLIR', 'FL', 'GRMN', 'GD', 'HAS', 'HON', 'HPQ', 'HBAN', 'ITW', 'ILMN', 'INTC', 'IBM', 'IFF', 'INTU', 'JNJ', 'JNPR', 'KEY', 'KMB', 'KLAC', 'LB', 'LRCX', 'LLY', 'LMT', 'LOW', 'LYB', 'MAR', 'MMC', 'MAS', 'MA', 'MAT', 'MCD', 'MCK', 'MJN', 'MRK', 'MTD', 'KORS', 'MCHP', 'MU', 'MSFT', 'MON', 'MNST', 'MSI', 'NTAP', 'NFLX', 'JWN', 'NOC', 'NVDA', 'OMC', 'ORCL', 'PFE', 'PM', 'PPG', 'PFG', 'PGR', 'PSA', 'PHM', 'RTN', 'REGN', 'RAI', 'RHI', 'ROK', 'COL', 'CRM', 'SNI', 'STX', 'SHW', 'SPGI', 'SBUX', 'SYMC', 'TEL', 'TDC', 'TXN', 'HSY', 'TSCO', 'TRIP', 'FOX', 'USB', 'UPS', 'UTX', 'URBN', 'VFC', 'VAR', 'VRSN', 'VRSK', 'VRTX', 'V', 'WMT', 'WAT', 'WDC', 'XLNX', 'YHOO', 'YUM', 'ZTS', 'DISH', 'INCY', 'MXIM', 'SHPG', 'SIRI', 'ABMD', 'ACIW', 'AEIS', 'AMD', 'ALGN', 'ANAT', 'ACGL', 'ARCC', 'ARRS', 'BEAV', 'TECH', 'BLKB', 'BRCD', 'BRKR', 'CDNS', 'CALM', 'CFFN', 'CAVM', 'CBPO', 'CMPR', 'CRUS', 'CGNX', 'COHR', 'CBSH', 'CVLT', 'CBRL', 'CREE', 'CVBF', 'CY', 'DXCM', 'EWBC', 'EFII', 'EXEL', 'FNSR', 'FIVE', 'FTNT', 'LOPE', 'HCSG', 'HOMB', 'HOPE', 'IDTI', 'IDCC', 'ISBC', 'IONS', 'JJSF', 'JACK', 'JAZZ', 'LANC', 'LSTR', 'LGND', 'LECO', 'LOGI', 'LOGM', 'LULU', 'MRVL', 'MASI', 'MDSO', 'MLNX', 'MELI', 'MSTR', 'MPWR', 'MORN', 'FIZZ', 'NATI', 'NTCT', 'NDSN', 'OTEX', 'OPK', 'PZZA', 'PEGA', 'PPC', 'POOL', 'POWI', 'PTC', 'RP', 'RGLD', 'SAFM', 'SANM', 'SGEN', 'SLAB', 'SAVE', 'STMP', 'SHOO', 'SNPS', 'TTWO', 'TFSL', 'PCLN', 'ULTI', 'TRMB', 'UBNT', 'UCBI', 'UTHR', 'OLED', 'WWD', 'ALX', 'AEO', 'NLY', 'AHL', 'AGO', 'ALV', 'BOH', 'BKU', 'BIG', 'BAH', 'EAT', 'BR', 'BC', 'BWXT', 'BXMT', 'CRI', 'CIM', 'CHH', 'CIEN', 'CNX', 'CLB', 'DRI', 'DLX', 'DKS', 'DLB', 'DRQ', 'ELLI', 'EPAM', 'EQM', 'EVR', 'RE', 'FICO', 'FII', 'FIG', 'FSIC', 'GME', 'IT', 'GMED', 'GGG', 'GWRE', 'HLF', 'ITT', 'JBT', 'KKR', 'LVS', 'LAZ', 'LCII', 'LEA', 'LII', 'MFA', 'MTG', 'MSA', 'MSCI', 'NRZ', 'ORI', 'PRA', 'Q', 'RDN', 'RYN', 'RGA', 'RNR', 'RLI', 'AOS', 'STWD', 'SNV', 'DATA', 'TEN', 'TER', 'TNH', 'TPL', 'THO', 'TTC', 'TUP', 'VC', 'VMW', 'GRA', 'WBC', 'WBS', 'WAL', 'WTM', 'WSM', 'YELP', 'NVR', 'TREX']
# for i in list:
#     for j in range(2010, 2018):
#         getAllTables(i, str(j))


     
    
