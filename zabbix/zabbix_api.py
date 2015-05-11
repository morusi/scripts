#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import urllib2
import sys

class ZabbixTools:
    def __init__(self,url,header,user,passwd):
        self.url = url
        self.header = header
        self.user = user
        self.passwd = passwd
        self.authID = self.user_login()
    def showauth(self):
        print self.authID

    def user_login(self):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "user.login",
                "params": {
                "user": self.user,
                "password": self.passwd
                },
                "id":1, 
            })
        # create request object
        request = urllib2.Request(self.url,data)
        for key in self.header:
            request.add_header(key,self.header[key])

        # auth and get authid
        try:
            result = urllib2.urlopen(request)
        except urllib2.URLError as e:
            return 0
        else:
            response = json.loads(result.read())
            result.close()
            authID = response['result']
            return  authID
    def user_logout(self):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "user.logout",
                "params": [],
                "id": 1,
                "auth": self.authID 
            })
        # create request object
        request = urllib2.Request(self.url,data)
        for key in self.header:
            request.add_header(key,self.header[key])

        # auth and get authid
        try:
            result = urllib2.urlopen(request)
        except urllib2.URLError as e:
            return 0
        else:
            response = json.loads(result.read())
            result.close()
            self.authID = response['result']

    def get_data(self,data,hostip=""):
        request = urllib2.Request(self.url,data)
        for key in self.header:
            request.add_header(key,self.header[key])
        try:
            result = urllib2.urlopen(request)
        except urllib2.URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server could not fulfill the request.'
                print 'Error code: ', e.code
            return 0
        else:
            response = json.loads(result.read())
            result.close()

            return response
    def host_get(self):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "host.get",
                "params": {
                    "output": ["hostid","name","status","host"],
                    "filter": {"host":""}
                },
                "auth": self.authID,
                "id": 1             
            })
        res = self.get_data(data)['result']
        if (res !=0 ) and (len(res) != 0):
            for host in res:
                print "Host ID:" ,host['hostid'], "Host Name:", host['name']
        else:
            print '\t',"\033[1;31;40m%s\033[0m" % "Get Host Error or cannot find this host,please check !"
            return 0
    def hostgroup_get(self):
        data =  json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "hostgroup.get",
                "params": {
                    "output": "extend",
                    },
                "auth": self.authID,
                "id": 1
            })
        res = self.get_data(data)['result']
        if (res != 0) and (len(res) != 0):
            for group in res:
                print "Group ID:", group['groupid'], "Group name:" ,group['name']
        else:
            print '\t',"\033[1;31;40m%s\033[0m" % "Get Group  Error or cannot find this group,please check !"
            return 0
    def template_get(self):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "template.get",
                "params": {
                    "output": "extend",
                    },
                "auth": self.authID,
                "id": 1
            })
        res = self.get_data(data)['result']
        if (res != 0) and (len(res) != 0):
            for template in res:
                print "template ID:", template['templateid'], "template name:" ,template['name']
        else:
            print '\t',"\033[1;31;40m%s\033[0m" % "Get template  Error or cannot find this template,please check !"
            return 0
    def host_create(self):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "host.create",
                "params": {
                    "host": '15test',
                    "interfaces": [
                        {
                            "type": 1,
                            "main": 1,
                            "useip": 1,
                            "ip": "192.168.1.15",
                            "dns": "",
                            "port": "10050"
                        }
                    ],
                    "groups": [
                        {
                            "groupid": "2"
                        }
                    ],
                    "templates": [
                        {
                            "templateid": "10001"
                        }
                    ],  
                },
                "auth": self.authID,
                "id": 1                
            })
#        res = self.get_data(data)['result']
        res = self.get_data(data)
        print res

def main():
    url = "http://192.168.1.17/zabbix/api_jsonrpc.php"
    header = {"Content-Type": "application/json"}
    user = "yige.han"
    passwd = "hanyige"
    test = ZabbixTools(url,header,user,passwd)

    #test.user_login()

    #test.host_get()
    #test.hostgroup_get()
    #test.template_get()
    #test.host_create()
    test.showauth()
    test.user_logout()
    test.showauth()
    #test.host_get()
if __name__ == '__main__':
    main()
    
