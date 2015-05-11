#!/usr/bin/env python2.7
#coding=utf-8

import json
import urllib2

url = "http://192.168.1.17/zabbix/api_jsonrpc.php"
header = {"Content-Type": "application/json"}

#auth user and password
data = json.dumps(
{
    "jsonrpc": "2.0",
    "method": "user.login",
    "params": {
    "user": "yige.han",
    "password": "hanyige"
    },
    "id":1,
})

# create request object
request = urllib2.Request(url,data)
for key in header:
    request.add_header(key,header[key])

# auth and get authid
try:
    result = urllib2.urlopen(request)
except urllib2.URLError as e:
    print "Auth Failed, Please Check Your Name And Password:" ,e.errno
else:
    response = json.loads(result.read())
    result.close()
    print "Auth Successful. The Auth ID is:", response['result']
