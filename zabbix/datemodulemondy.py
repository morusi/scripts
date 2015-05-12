from datetime import *
ismon = []
for i in range(1901,2001):
    for j in range(1,13):
        nowdate = date(i,j,01)
        ismonday = nowdate.weekday()
        if ismonday == 0 :
            ismon.append(nowdate)
