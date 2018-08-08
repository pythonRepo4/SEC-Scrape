from urllib import request
import os
import Utility
import scrapHTML

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

"""-----------------------------------------------------------------------------
Join html files. fileName is current HTML while htmlLink is what will be joined. 
-----------------------------------------------------------------------------"""
def joinHTML(fileName, htmlLink):
    htmlLink = htmlLink.replace("ix?doc=/", "")

    try:
        request.urlretrieve(htmlLink, fileName)
    except:
        print("Download failed")

  
#     """If fileName (tickerName-10K-yr) already exists, add htmlLink to that file """
#     """Read current file, Encode html into "utf-8. Anything that cannot be encoded in manually converted to approximate character  """
#     newFile = ""
#     currentFile = open(fileName, "r").read().splitlines()
#     for i in range(0, len(currentFile)):
#         temp = str(currentFile[i].encode("utf-8", "ignore")).split("'")[1]
#         temp = removeUTFChar(temp)
#         temp = temp.replace("&amp;", "&")
#         temp = temp.strip()
#         newFile += temp + "\n"
#       
#     request.urlretrieve(htmlLink , str(os.getcwd()) + "\\temp.html")
#     addFile = open(os.getcwd() + "\\temp.html", "r").read().splitlines()
#     for i in range(0, len(addFile)):
#         temp = str(addFile[i].encode("utf-8", "ignore")).split("'")[1]
#         temp = removeUTFChar(temp)
#         temp = temp.replace("&amp;", "&")
#         temp = temp.strip()
#         newFile += temp + "\n"
#       
#     currentFile = open(fileName, "w")
#     for i in newFile.splitlines():
#         currentFile.write(i)
#   
#     currentFile.close()
                 
"""-----------------------------------------------------------------------------
Converts html table into arrays
-----------------------------------------------------------------------------"""
def htmlTable(html, rowTagInput):
    rowTag = "<" + rowTagInput + ">"
    endTag = "</" + rowTagInput + ">"
    
    row = ""
    rowFound = False
    rowArray = []
    for i in html.splitlines():
        """HTML line may have <rowTagInput class=...>. Remove everything after space."""
        firstTag = i.strip().split(" ")[0]
        if(firstTag[-1] != ">"):
            firstTag += ">"

        if(rowTag in firstTag):
            rowFound = True
            continue
            
        if(endTag in i):
            rowFound = False
            temp = []
            
            for j in row.splitlines():
                temp.append(Utility.deleteOuterTags(j))
            rowArray.append(temp)
            
            row = ""
            continue
                    
        if(rowFound == True):
            row += i + "\n"

    return rowArray
    

"""-----------------------------------------------------------------------------------------------------------

Start by downloading past ten 10Ks from 2017 as html document 

-----------------------------------------------------------------------------------------------------------"""
def documentList(tickerName, date):
    count = 10 #Num of documents to display
    """base_url gets table of 10k -> link to 10k + other items -> actual 10k """
    
    base_url = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=" + str(tickerName) + \
     "&type=10-K&dateb="  + str(date) + "&owner=exclude&output=xml&count=" + str(count)
#     print(base_url)
    tempWebFile = request.urlopen(base_url).read().decode('utf-8')
    """In tempWebFile, table with 
    link | dates | 10k-link | Annual report | 10-k.
       
    This table is inside tags <results> </results>     
     """
    tableWithLinks = Utility.returnInTags(tempWebFile, "results") 
    tableArray = htmlTable(tableWithLinks, "filing")
        
    """Got link to 10ks, now get link to actual 10k and then download """
    preDirectory = str(os.getcwd()) + "\\" 
    directory = preDirectory + "html-files\\"
    date10k = ""
    fileName = ""
      
    for i in tableArray:
#         print(i)
        if(i[-1] == "10-K/A"):
            continue
        link10k = ""
   
        for j in i:            
            """Link to 10-k documents has substring "/www.sec.gov/Archives". Works as of 17 Apr 2018 """
            if("/www.sec.gov/Archives" in j):
                link10k = j
                break   
             
        if(link10k == ""):
            continue
                         
        """link10k has link to 10k of specific year. The 10k is broken into further html links which will
        all be downloaded the combined into 1 html."""
        tempWebFile = request.urlopen(link10k).read().decode('utf-8')
        tableWithLinks = Utility.returnInTags(tempWebFile, "table")
        tableArrayWithLinks = htmlTable(tableWithLinks, "tr")
               
        date = ""
        payload = ">Period of Report"
        """Period of Report (date)"""
        for j in range(0, len(tempWebFile.splitlines())):
            line = tempWebFile.splitlines()[j]
            if(payload in line):
                date = Utility.removeTags(tempWebFile.splitlines()[j+1])
                break   
        """If the month is early in the year, the period of report is probably for last year."""
        month = int(date.split("-")[1])
        year = int(date.split("-")[0])
        if(month < 4):           
            date = year - 1
        else:
            date = year
                   
        """10K is broken into many different links. At this point put them all into one html """
        for j in tableArrayWithLinks:
#             print(j)
            payload = '<a href="/'
            for k in j:
                if(payload in k and ".htm" in k):
                    url_split = k.split('"')
                    temp_url = "http://www.sec.gov" + str(url_split[1])         
#                     print(temp_url)          
                    fileName = directory + tickerName + "-10k-" + str(date) + ".html"
                    joinHTML(fileName, temp_url)
              
            if(scrapHTML.foundConsolidated(tickerName, str(date)) == True):
#                 print("True")
                break


