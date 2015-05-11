#!/usr/bin/env python
#coding=utf-8

import json
import urllib2

#based url and requeired header

url = "http://192.168.1.17/zabbix/api_jsonrpc.php"
header = {"Content-Type": "application/json"}

data = json.dumps(
    {
    "jsonrpc": "2.0",
    "method": "host.get",
    "params": {
        "output": ["hostid","name","status","host"],
        "filter": {"host": ""}
    },
    "auth": "f97a0ce75aa0e59b115ea4dab0de7142",
    "id": 1
})

request = urllib2.Request(url,data)
for key in header:
    request.add_header(key,header[key])

try:
    result = urllib2.urlopen(request)
except urllib2.URLError as e:
    if hasattr(e,'reason'):
        print 'We failed to reach a server.'
        print 'Reason:', e.reason
    elif hasattr(e,'code'):
        print 'The server could not fulfill the request.'
        print 'Error code:', e.code
else:
    response = json.loads(result.read())
    result.close()

    print "Number Of Hosts:", len(response['result'])
    for host in response['result']:
        print "Host ID:",host['hostid'], "Host Name:", host['name']
        
