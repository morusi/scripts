#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import urllib2
import sys

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
                    "host": '15test',
                    "interfaces": [
                        {
                            "type": 1,
                            "main": 1,
                            "useip": 1,
                            "ip": '192.168.1.15',
                            "dns": "",
                            "port": "10050"
                        }
                    ],
                    "groups": groupid,
                
                    "templates": templateid,

                },
                "auth": self.authID,
                "id": 1                
            })
        res = self.get_data(data)
        return res
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
    def graph_get(self):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "graph.get",
                "params": {
                    "output": ["id","name","status","host"],
                    "hostids": 10107
                },
                "auth": self.authID,
                "id": 1             
            })
        res = self.get_data(data)['result']
        print res
    def scrren_get(self):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "screen.get",
                "params": {
                    "output": ["scrrenid", "name",]
                },
                "auth": self.authID,
                "id": 1   
            })
        res = self.get_data(data)['result']
        print res
    def scrren_create(self):
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
        res = self.get_data(data)
        print res
    def screenitem_create(self):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "screenitem.create",
                "params": {
                    "screenid": 26,
                    "resourcetype": 0,
                    "resourceid": 590,
                    "width": 500,
                    "Height": 100,
                    "x": 0,
                    "y": 0
                },
                "auth": self.authID,
                "id": 1
            })
        res = self.get_data(data)
        print res 
    def scrrenitem_get(self):
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
        print res

def showmenu():
    print """print useage:
    """ + sys.argv[0] + """ -h print the help
    -CH 'host,hostip' -G 'group1,goup2' -T 'Template1,Template2'

    """
def main():
    url = "http://192.168.1.17/zabbix/api_jsonrpc.php"
    user = "yige.han"
    passwd = "hanyige"
    test = ZabbixTools(url,user,passwd)
    if len(sys.argv) <= 2 or sys.argv[1].lower() == '-h':
        showmenu()
        exit(0)
    elif sys.argv[1][1:].lower() == "ch" and sys.argv[3][1:].lower() == "g" and sys.argv[5][1:].lower() == "t":
        #host creat    
        hosts = []
        hosts = sys.argv[2].split(',') #get in put hosts
        templates = {} 
        templatesvalues = ''
        alltemplates = test.template_get() #get zabbix server all templates
        groups = {}
        groupsvalues =''
        allgroups =test.hostgroup_get() # get zabbix server all groups
        for i in sys.argv[4].split(','):
            # get input  goups
            for j in  allgroups:
                if i.lower() == j.get('name').lower():
                    groups[j.get('name')] = j.get('groupid')
                    groupsvalues += "\ngroup id:" + j.get('groupid') + " group name: " + j.get('name')

        for i in sys.argv[6].split(','):
            #get input templates
            for j in alltemplates:
                if i == j.get('name'):
                    templates[j.get('name')] = j.get('templateid') 
                    templatesvalues += "\ntemplate id:" + j.get('templateid') + "  template name:" + j.get('name')
        iscreate = raw_input(" hosts name:" + hosts[0] + " hosts ip:" + hosts[1] + templatesvalues + groupsvalues + '\n' + "please input (Y/N):").lower()
        if iscreate == 'y':
            # is it create?
            print "plase wait creating"
            hostname = hosts[0]
            hostip = hosts[1]
            groupid = groups.values()
            templateid = templates.values()
            print test.host_create(hostname,hostip,groupid,templateid)
    else:
        print sys.argv[2][1:].lower() , sys.argv[3][1:].lower() , sys.argv[5][1:].lower() 
        for i in range(0,len(sys.argv)):
            print  str(i) + " : " + sys.argv[i]

if __name__ == '__main__':
    main()
    
