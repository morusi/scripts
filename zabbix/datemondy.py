#!/usr/bin/env python
firstyear = 1900
allday = 0
ismon = []
def isleapyear(year):
    if not year % 4  and  year % 100:
        return 1
    elif not year % 400:
        return 1
    else:  
        return 0
def itismon(data):
    if data >365 and (data) % 7 == 0 :
        ismon.append(str(i) + "," + str(j))

for i in range(1900,2001):
    for j in range(1,13):
#        print " yearis:" + str(i) + " monis:" + str(j) + " days:" + str(allday)

        if j in (1,3,5,7,8,10,12):
            itismon(allday)
            allday = allday + 31
        elif j == 2:
            itismon(allday)
            if isleapyear(i):
                allday = allday + 29
            else: 
                allday = allday + 28
        elif j in (4,6,9,11):
            itismon(allday)
            allday = allday +30   

print ismon
