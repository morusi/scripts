#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import urllib2
import sys
import getopt
import re

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
        if (res !=0) and (len(res) != 0):
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
        res = self.get_data(data)
        return res
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
    def scrrenitem_create(self):
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

def showtemplate(intemplate):
    alltemplates = zabbixapi.template_get()
    templates = {}
    for i in intemplate:
        for j in alltemplates:
            if i.lower() == j.get('name').lower():
                templates[j.get('name')] = j.get('templateid')
                print """template id: %s template name: %s""" %(j.get('templateid'),j.get('name'))
    if not templates:
        print "template not exists!\n"
        #print alltemplates
        return 0
    else:
        return templates
def showgroup(ingroup):
    allgroups = zabbixapi.hostgroup_get()
    groups = {}
    for i in ingroup:
        for j in  allgroups:
            if i.lower() == j.get('name').lower():
                groups[j.get('name')] = j.get('groupid')
                print "group id: %s group name: %s" %(j.get('groupid'),j.get('name'))
    if not groups:
        print "group not exists"
        return 0
    else:
        return groups
def showhost(inhost):
    allhosts = zabbixapi.host_get()
    hosts = {}
    for j in allhosts:
        if inhost.lower() == j.get('name').lower():
            hosts[j.get('name')] = j.get('hostid')
    return hosts
def newshowhost(inhost):
    allhosts = zabbixapi.host_get()
    hosts = {}
    for i in inhost:
        for j in allhosts:
            if re.search(i.lower(),j.get('name').lower()):
                hosts[j.get('name')] = j.get('hostid')
    if hosts:
        return hosts
    else:
        print "not host"
        sys.exit()
        return 0
def showmenu():
    print """print useage:
    %s  -H print the help!
    -C 
        -h 'host,hostip' -g 'group1,group2' -t 'Template1,Template2'
            # create host in group  templat
        -t 'Template1,Template2'(no)
            # create template
        -g 'group1,group2' (no)
            # create group
        -s 'screen1', -h 'host' -t 'Graphs'
            # create screen
    -U -h 'host,' 'staus'
        # update host and update host into group template
    -D -h 'host'
        # delete host
    """ %(sys.argv[0])
    sys.exit()
def createhost(argv):
    try:
        opts,args = getopt.getopt(argv[2:], "h:t:g:")
    except getopt.GetoptError:
        showmenu()
    if not opts or len(args) > 0:
        showmenu()
    for name,value in opts:
        if name in "-h":
            hosts = value.split(',')
            reshost = showhost(hosts[0])
            if reshost:
                print "the host name already exists!"
                sys.exit()
            hostname = hosts[0]
            hostip = hosts[1]
        if name in "-t":
            templates = value.split(',')
            restemp = showtemplate(templates)
            if restemp:
                templateid = restemp.values()
            else:
                sys.exit()
        if name in "-g":
            groups = value.split(',')
            resgroup = showgroup(groups)
            if resgroup:
                groupid = resgroup.values()
            else:
                sys.exit() 
    if not groups:
        print "must have a group!" 
        sys.exit()      
    iscreate = raw_input("host name:" + hosts[0] + " host ip:" + hosts[1] + '\n' + "please input (Y/N):").lower()
    if iscreate == 'y':
        print "plase wait creating"
        print zabbixapi.host_create(hostname,hostip,groupid,templateid)
def deletehost(argv):
    hosts = argv.split(',')
    delhosts = newshowhost(hosts)
    for i,j in delhosts.items():
        print "host name: %s  host id: %s " %(i,j)
    isdel = raw_input('delete all host(y/n):').lower()
    if isdel == 'y':
        print "deleting plase wait"
        hostids = delhosts.values()
        print zabbixapi.host_delete(hostids)
        sys.exit()
    else:
        sys.exit()
#def updatehost(argv):
def main():
    url = "http://192.168.1.17/zabbix/api_jsonrpc.php"
    user = "yige.han"
    passwd = "hanyige"
    zabbixapi = ZabbixTools(url,user,passwd)
    zabbixapi.graph_get()
if __name__ == '__main__':
    main()