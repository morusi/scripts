days = 0
weekday = 1
year = 1900
count = 0
num = 0
if  year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
    days = 366
else:
    days = 365
weekday += days % 7

for year in range(1901,2001):

    for month in  range(1,13):
        if month in [1,3,5,7,8,10,12]:
            days = 31
            weekday += days
            if weekday % 7 == 0:
                count += 1
        elif month in [4,6,9,11]:
            days = 30
            weekday += days
            if weekday % 7 == 0:
                count += 1
        elif  year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
                days = 29
                weekday += days
                if weekday % 7 == 0:
                    count += 1
        else:
                days = 28
                weekday += days
                if weekday % 7 == 0:
                    count += 1
print count