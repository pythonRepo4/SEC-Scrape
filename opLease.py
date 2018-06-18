import scrapHTML
import Utility

"""Attempts to approximate other debt commitments not present on balance sheets such as:
operating leases, other purchase commitments, manufacturing commitments,  """         
                
def opLease(tickerName, year):
#     print(tickerName + ' : ' + str(year))
#     Main.download(tickerName, year)
    try:
        titles, tables = scrapHTML.getAllTables(tickerName, year)
    except:
        return

    if(titles == None or tables == None):
        return
    
    leaseCommitment = []
    
    for i in range(0, len(tables)):
        title = titles[i]
        table = tables[i]
        
        tableVars = ""
        for j in table:
            for k in j:
                tableVars += k
        
        """Table variables (row titles) and title of table """
        tableVars = tableVars.lower().replace(" ", "")
        title = title.lower().replace(" ", "")
        """Get Operating Leases"""
        if("leases" in tableVars or "leases" in title or "lease" in tableVars or "lease" in title):
#             Utility.makeTable(table)    
#             print(title)
#             print(tableVars)
            totalIndex = 0 
            tempLease = []
            """Goes down row and sees if "lease" or "obligation" is in the row title"""
            for k in range(1, len(table)):
                temp = ""
                try:
                    temp += table[k][0].lower()
                    temp += table[k][1].lower()
                except:
                    continue
                
                if(("leases" in temp and "capital" not in temp and "operat" in temp and "receivable" not in temp)
                    or ("lease" in temp and "capital" not in temp and "operat" in temp and "receivable" not in temp)
                    or ("lease" in temp and "capital" not in temp and "property" in temp and "receivable" not in temp)):
                    for h in table[k]:
                        tempLease.append(h)

                
            """Now goes across column and sees if "lease" or "obligation" or "commitment" is in row title """
            for k in range(1, len(table[0])):
                temp = ""
                temp += table[0][k].lower()
                temp += table[1][k].lower()
                
                if(("leases" in temp and "capital" not in temp and "operat" in temp and "receivable" not in temp)
                    or ("lease" in temp and "capital" not in temp and "operat" in temp and "receivable" not in temp)
                    or ("lease" in temp and "capital" not in temp and "property" in temp and "receivable" not in temp)):
                    for h in table:
                        tempLease.append(h[k])
                        
            if(len(tempLease) < 3):
                continue
            
            """See what the multiplier is (thousands, millions, or billions) """
            multiplier = 1000000
            if("inthousands" in title or "inthousands" in tableVars):# or "000" in tableVars or "'000" in title):
                multiplier = 1000
            elif("inmillions" in title or "inmillions" in tableVars):
                multiplier = 1000000
            elif("inbillions" in title or "inbillions" in tableVars):
                multiplier = 1000000000
#             print(tempLease)
#             print(multiplier)
            for l in range(0, len(tempLease)):
                try:
                    if(tempLease[l].strip() == "" or tempLease[l].strip() == "-"):
                        tempLease[l] = 0
                        continue
                    tempLease[l] = Utility.myFloat(tempLease[l]) * multiplier 
                except:
                    pass

            """Sometimes the commitment is a duplicate. Don't add if it is a duplicate"""
            rowTitles = ""
            for l in leaseCommitment:
                rowTitles += l[0]
                
            if(tempLease[0] not in rowTitles):
                leaseCommitment.append(tempLease)
    
    otherDebt = [0, 0, 0, 0, 0, 0]
    """At this point, leaseCommitment has varying leases, obligations, and commitments. Need to consolidate"""
    """Delete empty arrays, and arrays with "total" or "net" in row title"""
    """Other Debt will have [yr1, yr2, yr3, yr4, yr5, thereafter] """
    for i in leaseCommitment:
#         print(i)
        rowTitle = i[0].lower()
        if("net" in rowTitle or "total" in rowTitle):
            continue
        tempDebt = i[1:]
        debtNumbers = []
        for j in tempDebt:
            try:
                debtNumbers.append(Utility.myFloat(j))
            except:
                continue
        if(len(debtNumbers) < 3):
            continue
    
        firstSum = sum(debtNumbers[:len(debtNumbers)-1])
        secondSum = sum(debtNumbers[1:])
        """Either very first one or last column is the total. Delete this """
        if(Utility.numbersClose(firstSum, debtNumbers[-1]) == True):
            debtNumbers = debtNumbers[0:len(debtNumbers)-1]
            if(0 in debtNumbers):
                debtNumbers.remove(0)
        elif(Utility.numbersClose(secondSum, debtNumbers[0] ) == True):
            debtNumbers = debtNumbers[1:]
            if(0 in debtNumbers):
                debtNumbers.remove(0)
        else:
            continue
        
        if(len(debtNumbers) < 3):
            continue
#         print(debtNumbers)

        """ Debt obligations are generally projected for 5 years out and then has a thereafter number. If length is less than 6, 
        spread out 2 and 3rd over two years"""
        if(len(debtNumbers) == 3):
            split = debtNumbers[1] / 3
            debtNumbers[1] = split
            debtNumbers.insert(1, split)
            debtNumbers.insert(1, split)
        
        i = 1
        while(len(debtNumbers) < 6):
            split = debtNumbers[i] / 2
            debtNumbers[i] = split 
            debtNumbers.insert(i, split)
        
            i += 2
        
        for i in range(0, len(otherDebt)):
            otherDebt[i] += debtNumbers[i]
            

    return otherDebt

# list = ["HD", "NKE", "AZO", "SWKS", "FB", "FFIV", "FAST", "UTMD", "ULTA", "IPGP", "RHT", "GPS", "WMT", "COST", "GILD"] 
list = ["AMAT"]
for i in list:
    print(i)
    for j in range(2017, 2018):
        print(j)
        print(opLease(i, str(j)))




                
