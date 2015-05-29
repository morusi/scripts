#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import urllib2
from msilib.schema import ReserveCost

class ZabbixTools:
    def __init__(self,url,user,passwd):
        """
        useage:
            plase input url,username,userpassword
        """
        self.url = url
        self.header = {"Content-Type": "application/json"}
        self.user = user
        self.passwd = passwd
        self.authID = self.user_login()          
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
        if (res !=0) and (len(res) != 0):
            return res
        else:
            return 0
    def host_exists(self,hostname):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "host.exists",
                "params": {
                    "host": hostname
                },
                "auth": self.authID,
                "id": 1
            })
        res = self.get_data(data)['result']
        if (res != 0 ) and (len(res) != 0 ):
            return res
        else:
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
            return res
            # for group in res:
            #     print "Group ID:", group['groupid'], "Group name:" ,group['name']
        else:
            print '\t',"\033[1;31;40m%s\033[0m" % "Get Group  Error or cannot find this group,please check !"
            return 0
    def host_create(self,hostname,hostip,groupid,templateid):
        """ the input data  hostname , hostip , groupid, templateid """
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "host.create",
                "params": {
                    "host": hostname,
                    "interfaces": [
                        {
                            "type": 1,
                            "main": 1,
                            "useip": 1,
                            "ip": hostip,
                            "dns": "",
                            "port": "10050"
                        }
                    ],
                    "groups": groupid,                
                    "templates":templateid,

                },
                "auth": self.authID,
                "id": 1                
            })
        res = self.get_data(data)['result']
        if (res !=0) and (len(res) != 0):
            return res
        else:
            return 0
    def host_delete(self,hostids):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "host.delete",
                "params":hostids,
                "auth": self.authID,
                "id":1
            })
        res = self.get_data(data)['result']
        if (res != 0) and (len(res) != 0):
            return res
        else:
            return 0
    def host_update(self,hostids,status):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "host.massupdate",
                "params": {
                    "hosts": hostids,
                    "status": status
                },
                "auth": self.authID,
                "id":1
            })
        res = self.get_data(data)
        #res = self.get_data(data)['result']
        if (res != 0) and (len(res) != 0):
            return res
        else:
            return 0        
    def template_get(self):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "template.get",
                "params": {
                    "output": ["name", "templateid"],
                    },
                "auth": self.authID,
                "id": 1
            })
        res = self.get_data(data)['result']

        if (res != 0) and (len(res) != 0):
            return res
            # for template in res:
            #     print "template ID:", template['templateid'], "template name:" ,template['name']
        else:
            print '\t',"\033[1;31;40m%s\033[0m" % "Get template  Error or cannot find this template,please check !"
            return 0
    def graph_get(self,hostids):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "graph.get",
                "params": {
                    "output": ["id","name","status","host"],
                    "hostids": hostids
                },
                "auth": self.authID,
                "id": 1             
            })
        res = self.get_data(data)['result']
        if (res !=0) and (len(res) != 0):
            return res
        else:
            return 0
    def screen_get(self):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "screen.get",
                "params": {
                    "output": ["screenid", "name",]
                },
                "auth": self.authID,
                "id": 1   
            })
        res = self.get_data(data)['result']
        if (res !=0) and (len(res) != 0):
            return res
        else:
            return 0
    def screen_create(self):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "screen.create",
                "params":{
                    "name": "testscreen",
                    "hsize": 3,
                    "vsize": 2
                },
                "auth": self.authID,
                "id": 1
            })
        res = self.get_data(data)['result']
        if (res !=0) and (len(res) != 0):
            return res
        else:
            return 0
    def screenitem_create(self):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "screenitem.isreadable",
                "params": {
                    "screenid": 26,
                    "resourcetype": 0,
                    "resourceid": [590,550,564],
                    "width": 500,
                    "Height": 100,
                    "x": 0,
                    "y": 0
                },
                "auth": self.authID,
                "id": 1
            })
        res = self.get_data(data)['result']
        if (res !=0) and (len(res) != 0):
            return res
        else:
            return 0
    def screenitem_get(self):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "screenitem.get",
                "params": {
                    "output": "extend",
                    "screenids": "16"
                },
                "auth": self.authID,
                "id": 1   
            })
        res = self.get_data(data)['result']
        if (res !=0) and (len(res) != 0):
            return res
        else:
            return 
    def screenexists(self,screenname):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "screen.exists",
                "params": {
                    "host": screenname
                },
                "auth": self.authID,
                "id": 1
            })
        res = self.get_data(data)['result']
        if (res != 0 ) and (len(res) != 0 ):
            return res
        else:
            return 0
     
def main():
    url = "http://192.168.1.17/zabbix/api_jsonrpc.php"
    user = "yige.han"
    passwd = "hanyige"
    zabbixapi = ZabbixTools(url,user,passwd)
    print zabbixapi.host_get()

if __name__ == '__main__':
    main()