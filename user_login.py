#!/usr/bin/env python
import sys
retry_limit = 3
retry_count = 0
user_account = "account.db"
user_lock = "acc_lock.db"

def islock(username):
    f = open(user_lock,'r')
    for i in f.readlines():
        if username == i.split()[0]:
            return 1
    return 0
def isaccount(username,passwd):
    f = open(user_account,'r')
    for i in f.readlines():
        user_name,user_pd = i.split()
        if username == user_name and user_pd == passwd:
            return 1
        else:
            return 0
def lockaccount(username):
    f = open(user_lock,'a')
    f.write(username + '\n')
    f.close

while retry_count < retry_limit:
    user_name = raw_input('PLS input your name:')
    if  islock(user_name):
        sys.exit('your account  locked!')
    user_password = raw_input('PLS input your password:')
    if  isaccount(user_name,user_password):
        print 'welcome in this system'
        break
    else:
        print 'The username or password is wrong'
        retry_count += 1
else:
    print 'the account while  locked'
    lockaccount(user_name)
