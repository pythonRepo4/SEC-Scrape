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
    
    tempLease = []
    foundMult = False
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

            """See what the multiplier is (thousands, millions, or billions) """
            multiplier = 1
            if("inthousands" in title or "inthousands" in tableVars or "000" in title or "'000" in title or "thousandsof" in title or
               "thousandsof" in tableVars):
                multiplier = 1000
                foundMult = True
            elif("inmillions" in title or "inmillions" in tableVars or "millionsof" in title or "millionsof" in tableVars):
                multiplier = 1000000
                foundMult = True
            elif("inbillions" in title or "inbillions" in tableVars or "billionsof" in title or "billionsof" in tableVars):
                multiplier = 1000000000
                foundMult = True
            
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
                    or ("lease" in temp and "capital" not in temp and "property" in temp and "receivable" not in temp)
                    or ("leased" in temp and "capital" not in temp and "receivable" not in temp)):
                    row = []
                    for h in table[k]:
                        try:
                            row.append(Utility.myFloat(h) * multiplier)
                        except:
                            row.append(h)
                    
                    if(len(row) > 4):
                        tempLease.append(row)
                
            """Now goes across column and sees if "lease" or "obligation" or "commitment" is in row title """
            for k in range(1, len(table[0])):
                temp = ""
                temp += table[0][k].lower()
                temp += table[1][k].lower()
                if(("leases" in temp and "capital" not in temp and "operat" in temp and "receivable" not in temp)
                    or ("lease" in temp and "capital" not in temp and "operat" in temp and "receivable" not in temp)
                    or ("lease" in temp and "capital" not in temp and "property" in temp and "receivable" not in temp)
                    or ("leased" in temp and "capital" not in temp and "receivable" not in temp)):
                    column = []
                    for h in table:
                        try:
                            column.append(Utility.myFloat(h[k]) * multiplier)
                        except:
                            column.append(h[k])
                        
                    if(len(column) > 4):
                        tempLease.append(column)
                    
                    

    """At this point have a collection of possible operating leases, other lease commitments. """
    leaseCommitment = []
    for i in tempLease:
        """Sometimes the commitment is a duplicate. Don't add if it is a duplicate"""
        leaseTitles = ""
        for j in leaseCommitment:
            leaseTitles += j[0].lower()
        
        if(isinstance(i[0], str) == False):
            continue
        if(i[0].lower() in leaseTitles):
            continue
        
        """If title is broken into different arrays, consolidated. EX: ["op", "lease", "commit", "500", ....] """
        k = 1 
        while(isinstance(i[k], str) == True):
            i[0] += i[k] + " "
            del i[k]
            if(len(i) == 1):
                break
        if(len(i) <=1 ):
            continue
        """Remove trailing zeros in array if GREATER than 8"""
        temp = i 

        j = len(temp) - 1
        while(temp[j] == 0 and j >= 8):
            del temp[j]
            j -= 1
            
        """After first index, if cannot be converted to number,  delete it """
        j = 1
        while(j < len(temp)):
            try:
                float(temp[j])
                j += 1
            except:
                del temp[j]

        leaseCommitment.append(temp) 

    
    otherDebt = [0, 0, 0, 0, 0, 0]
    possibleDebt = []
    allDebts = 0
    """At this point, only return operating leases. If there is no operating lease, return everything else"""
    """Delete empty arrays, and arrays with "total" or "net" in row title"""
    """Other Debt will have [yr1, yr2, yr3, yr4, yr5, thereafter] """
    for i in leaseCommitment:
        print(i)
        rowTitle = i[0].lower()
        debtNumbers = i[1:]

        if("net" in rowTitle or "total" in rowTitle):
            continue
        if(len(debtNumbers) < 3):
            continue

        try:
            float(debtNumbers[0])
        except:
            continue
        try:
            float(debtNumbers[1])
        except:
            continue
        
        firstSum = sum(debtNumbers[:len(debtNumbers)-1])
        secondSum = sum(debtNumbers[1:])
        total = 0
        """Either very first one or last column is the total. Delete this """
        if(Utility.numbersClose(firstSum, debtNumbers[-1]) == True):
            debtNumbers = debtNumbers[0:len(debtNumbers)-1]
            total = firstSum
        elif(Utility.numbersClose(secondSum, debtNumbers[0] ) == True):
            debtNumbers = debtNumbers[1:]
            total = secondSum
        else:
            pass
        allDebts += total
        
        """ Debt obligations are generally projected for 5 years out and then has a thereafter number. If length is less than 6, 
        spread out 2 and 3rd over two years"""
        if(len(debtNumbers) == 3):
            split = debtNumbers[1] / 3
            debtNumbers[1] = split
            debtNumbers.insert(1, split)
            debtNumbers.insert(1, split)
        
        j = 1
        while(len(debtNumbers) < 6):
            split = debtNumbers[j] / 2
            debtNumbers[j] = split 
            debtNumbers.insert(j, split)
            j += 2
        
        """Sometimes you will get the same operating lease numbers. If the first year is the exact same, do not add it"""
        firstNum = float(debtNumbers[0])
        alreadyAdded = False
        for j in possibleDebt:
            possibleDebtNum = float(j[0])
            if(possibleDebtNum * .95 <= firstNum  and firstNum <= possibleDebtNum * 1.05 ):
                alreadyAdded = True
        if(alreadyAdded == True):
            continue
        else:
            possibleDebt.append(debtNumbers)
            
        if("operating lease" in rowTitle.lower()):
            possibleDebt = []
            possibleDebt.append(debtNumbers)
            break

    for i in possibleDebt:
        for j in range(0, len(otherDebt)):
            otherDebt[j] += i[j]
            
    """If sum is less than 99,999, multiply by 1000. If less than 999, multiply by million"""
    if(foundMult == False):
        temp = []
        multiplier = 1
        if(allDebts < 5999):
            multiplier = 1000000
        elif(allDebts < 399999):
            multiplier = 1000
    
        old = otherDebt
        otherDebt = []
        for i in old:
            otherDebt.append(i * multiplier)
    print(otherDebt)
            
#     print(otherDebt)
    return otherDebt

# list = ['AMWD', 'BIIB', 'EXPO', 'FB', 'FAST', 'IPGP', 'LNTH', 'ORLY', 'SWKS', 'ULTA', 'AZO', 'FDS', 'GPS', 'HD', 'OOMA', 'PSTG', 'ROL', 'TSE', 'UNH', 'AMAT', 'BBY', 'HRB', 'CHRW', 'CELG', 'CI', 'CLX', 'CL', 'EW', 'EA', 'GRMN', 'HAS', 'HUM', 'KLAC', 'LB', 'LRCX', 'LYB', 'MAS', 'MCD', 'MTD', 'MU', 'MSFT', 'MNST', 'MSI', 'NVDA', 'REGN', 'RHI', 'ROK', 'SHW', 'TXN', 'HSY', 'UPS', 'VAR', 'INCY', 'MXIM', 'SIRI', 'ABMD', 'AZPN', 'CDNS', 'CDK', 'CBPO', 'CRUS', 'CGNX', 'FIVE', 'LOPE', 'HA', 'HQY', 'LSTR', 'LOGI', 'LULU', 'LITE', 'MTCH', 'PZZA', 'PPC', 'SAFM', 'STMP', 'BIO', 'BURL', 'BWXT', 'CC', 'ENR', 'EPAM', 'GDDY', 'GGG', 'HLF', 'LPI', 'LEA', 'LII', 'LPX', 'RES', 'NOW', 'TNH', 'THO', 'TTC', 'VEEV', 'VC', 'WBC', 'WSM', 'YELP', 'PZZA', 'PZZA', 'DENN', 'IRBT', 'KBAL', 'QLYS', 'RUTH', 'PRSC', 'UCTT', 'WING']
# 
# for i in list:
#     print(i)
#     for j in range(2012, 2018):
#         print(j)
#         print(opLease(i, str(j)))




                

