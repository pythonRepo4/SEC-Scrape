

import time

"""--------------------------------------------------------------------------------------------------------------------------------------
With an array in the form 

''   WMT   TGT   
PE ...
PB ...

Will make a table to format data.  
-----------------------------------------------------------------------------"""

def makeTable(data):
    columnLength = []
    for i in range(0,len(data[0])):
        longestLength = 0
        for j in range(0,len(data)):
            if(len(data[j][i]) > longestLength):
                longestLength = len(data[j][i])
        longestLength += 5
        columnLength.append(longestLength)

    for i in data:
        formatText = ""
        count = 0

        for j in range(0, len(i)):
            colLength = columnLength[count] 
            count += 1
            formatText += i[j].ljust(colLength) + " | "
        print(formatText)

'''-----------------------------------------------------------------------------------

Utility float 

-----------------------------------------------------------------------------------'''
def myFloat(input):
    try:
        input = input.replace(",","")
    except:
        pass
    if(input == ''  or input == ' '):
        return 0 
    else:
        return float(input)


'''-----------------------------------------------------------------------------------

This function returns current date in MM/DD/YYYY formate. If month is april, m = 4 not 04

-----------------------------------------------------------------------------------'''
def getTodaysDate():
    dateStr = time.strftime("%m/%d/%Y")
    dateSplit = dateStr.split("/")
    
    # strftime gets month and date in MM, DD. If month is april, m = 04. This removes
    # the zero before the actual date. 
    if(dateSplit[0][0] == '0'):
        dateSplit[0] = dateSplit[0][1:]
    if(dateSplit[1][0] == '0'):
        dateSplit[1] = dateSplit[1][1:]
    
    return dateSplit[0] + '/' + dateSplit[1] + '/' + dateSplit[2]

"""---------------------------------------------------------

Checks to see if two strings are mostly similar

---------------------------------------------------------"""
def similarity(str1,str2):
    similarityCount = 0
    largerIndex = 0
    
    if(len(str1) == 0  or len(str2) == 0):
        return False
        
    for i in range(0,len(str1)):
        try:
            if(str1[i] in str2[i-1:i+1]):
                similarityCount += 1
        except:
            pass
    
    if(len(str1) > len(str2)):
        largerIndex = len(str1)
    else:
        largerIndex = len(str2)

    if(similarityCount/largerIndex > .7):   
        return True
    return False

"""-----------------------------------------------------------------------------
Finds tag and returns whatever is in tag
-----------------------------------------------------------------------------"""
def returnInTags(html, tagInput):
    tag = "<" + tagInput
    endTag = "</" + tagInput + ">"
    returnInTags = ""
    
    foundTag = False
    for i in html.splitlines():
        if(endTag in i):
            break 
        
        if(foundTag == True):
            returnInTags += i + " \n"
            
        if(tag in i):
            foundTag = True
    
    return returnInTags

"""-----------------------------------------------------------------------------
Delete outer tags whatever they are 
-----------------------------------------------------------------------------"""
def deleteOuterTags(html):
    split = html.split(">")
    html = ">".join(split[1:])
    
    split = html.split("<")
    html = "<".join(split[:len(split)-1])
    
    return html         
    
"""---------------------------------------------------------

remove Tags

Ex: <div>Hello</div>
returns Hello

---------------------------------------------------------"""
def removeTags(string):
    firstTag = string.find('>')
    if(firstTag < 0):
        return None
    
    string = string[firstTag + 1:]
    
    secondTag = string.find('<')
    if(secondTag < 0):
        return None
    
    string = string[:secondTag]
    
    return string

"""-----------------------------------------------------------------------------
Delete all tags
-----------------------------------------------------------------------------"""
def deleteAllTags(html):
    returnString = ""
    foundTag = False

    for i in range(0, len(html)):
        if(html[i] == ">"):
            foundTag = False
            continue
        
        if(foundTag == True):
            continue
        
        if(html[i] == "<"):
            foundTag = True
            continue
        
        returnString += html[i]
    
    return returnString

"""-----------------------------------------------------------------------------
Line and variables are both arrays. If certain percentage of variables are in line, return True. Otherwise false
-----------------------------------------------------------------------------"""
def matches(line, variables, total = None):
    match = 0
    for i in variables:
        if(i.lower().replace(" ","") in line):
            match += 1
            
#     print(line)
#     print(str(match) + " : " + str(len(variables)))

    if(total != None):
        if(match == len(variables)):
            return True
        else:
            return False
    
    if(match/len(variables) >= .5):
        return True
    
    return False 


"""-----------------------------------------------------------------------------
Line and variables are both arrays. If certain percentage of variables are in line, return True. Otherwise false
-----------------------------------------------------------------------------"""
def singleMatch(line, variables):
    match = 0
    for i in variables:
        if(i.lower().replace(" ","") in line and len(line) < len(i) + 2):
            match += 1
            
#     print(line)
#     print(str(match) + " : " + str(len(variables)))

    if(match >= 1):
        return True
    return False 

"""-----------------------------------------------------------------------------
Combine array into a string
-----------------------------------------------------------------------------"""
def combineArray(array):
    returnArray = ""        
    for i in array: 
        for j in i:
            returnArray += j + " "
            
    return returnArray


"""-----------------------------------------------------------------------------
Combine single array into a string
-----------------------------------------------------------------------------"""
def combineSingleArray(array):
    returnArray = ""
    if(len(array) == 1):
        return array[0]
    for i in array:
        returnArray += i + " "
    return returnArray

"""-----------------------------------------------------------------------------
Remove Parenthesis
-----------------------------------------------------------------------------"""
def removeParenth(text):
    i = 0 
    commaFound = False
    
    while(i < len(text)):
        if(text[i] == "("):
            commaFound = True
        
        if(commaFound == True):
            text = text[:i] + text[i+1:]
            continue
        
        if(text[i] == ")"):
            commaFound = False
        
        i += 1
    
    return text


"""-----------------------------------------------------------------------------
Remove Extra Spaces
-----------------------------------------------------------------------------"""
def removeExtraSpaces(text):
    text = text.strip()
    
    i = 0 
    spaceFound = False
    while(i < len(text)):
        if(spaceFound == True and text[i] == " "):
            text = text[:i] + text[i+1:]
            continue
        
        if(spaceFound == True and text[i] != " "):
            spaceFound = False
            continue
            
        if(text[i] == " "):
            i += 1
            spaceFound = True
            continue
                
        i += 1
    
    return text

"""-----------------------------------------------------------------------------
Find endTag
-----------------------------------------------------------------------------"""
def returnEndTag(tag):
    split = tag.split("<")
    return "<" + "/" + split[1]

"""----------------------------------------------------------------------------
Sees if titleMatch (lower() with no spaces) is in title 
-----------------------------------------------------------------------------"""
def titleMatch(title , titleMatch):
    title = title.lower().replace(" ", "")
    for i in titleMatch:
        possibleTitle = i.lower().replace(" ", "")
        if(possibleTitle in title):
            return True
        
    return False

"""---------------------------------------------------------------------------
Sees if two numbers are close. Within 5% of each other
---------------------------------------------------------------------------"""
def numbersClose(num1, num2):
    if(num1 * .95 < num2 and num2 < num1 *1.05):
        return True
    elif(num2 *.95 < num1 and num1 < num2 *1.05):
        return True
    else: 
        return False












    