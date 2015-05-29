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
        return res
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
        return res
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
        res = self.get_data(data)
        print res
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
        res = self.get_data(data)
        print res 
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
    for i in inhost:
        for j in allhosts:
            if i.lower() == j.get('name').lower():
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
        -s 'screen', -h/-H 'host' -g/-G 'Graphs'
            # create screen
            #-G/H: 模糊查找
            #-g/h: 精确匹配
    -U -h 'host,' 'status'
        # update host and update host into group template
    -D -h 'host'
        # delete host
    """ %(sys.argv[0])
    sys.exit()
def showscreen(inscreen):
    allscreen = zabbixapi.screen_get()
    screen = {}
    for i in inscreen:
        for j in  allscreen:
            if i.lower() == j.get('name').lower():
                screen[j.get('name')] = j.get('screenid')
    return screen

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
            reshost = showhost(hosts)
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
def createscreen(argv):
    searchhost = 0
    searchgraph = 0
    try:
        opts, args = getopt.getopt(argv[2:], "s:h:H:g:G:")
    except getopt.GetoptError:
        showmenu()
    if not opts or len(args) > 0:
        showmenu()
    for name, value in opts:
        if name in "-s":
            screen = value.split(',')
            rescreen = showscreen(screen)
            if rescreen:
                print "screen is already exists!"
                sys.exit()
            screenname = screen[0]
        if name in "-h":
            hosts = value.split(',')
        if name in "-H":
            hosts = value.split(',')
            searchhost = 1
        if name in "-g":
            graphs = value.split(',')
        if name in "-G":
            graphs = value.split(',')
            searchgraph = 1
    if hosts and graphs:
        if searchhost == 0:
            reshost = showhost(hosts)
        elif searchhost == 1:
            reshost = newshowhost(hosts)
        if searchgraph == 0:
            resall = showgraphs(reshost,graphs)
        elif searchgraph == 1:
            resall = searchgraphs(reshost,graphs)
        # resall = showgraphs(hosts,graphs)
        print "screen name: %s" %(screenname)
        for k,v in resall.items():
            print "host name: %s host id: %s " % (k.split('=')[0],k.split('=')[1])
            for j in v:
                print "     graph name: %s graph id: %s" %(j.get('name'),j.get('graphid'))
        iscreate = raw_input("are you sure create?(y/n:").lower()
            # ifiscreate == "y":
            #     pass



def showgraphs(inhosts,ingraphs):
    reshost = inhosts
    hostids = reshost.values()
    graphs = {}
    allgraphs = {}
    for m,i in reshost.items():
        allgraphs[m + "=" + i] = zabbixapi.graph_get(i)

    for i in ingraphs:
        for k,v in allgraphs.items():
            graphs[k] = []
            for j in v:
                if i.lower() == j.get("name").lower():
                    graphs[k].append(j)
    return graphs
def searchgraphs(inhosts,ingraphs):
    reshost = inhosts
    hostids = reshost.values()
    graphs = {}
    allgraphs = {}
    for m,i in reshost.items():
         allgraphs[m + "=" + i] = zabbixapi.graph_get(i)
    for i in ingraphs:
        for k,v in allgraphs.items():
            graphs[k] = []
            for j in v:
                if re.search(i.lower(),j.get("name").lower()):
                    graphs[k].append(j)
    return graphs

def main():
    global hosts
    hosts = []
    global groups
    groups = []
    global templateid
    templateid = []
    global groupid
    groupid = []
    if len(sys.argv) <= 2:
        showmenu()
    if sys.argv[1].lower() == "-h" or len(sys.argv) <= 2:
        showmenu()

    url = "http://192.168.1.17/zabbix/api_jsonrpc.php"
    user = "yige.han"
    passwd = "hanyige"

    global zabbixapi
    zabbixapi = ZabbixTools(url,user,passwd)

    zabbixapi.screenitem_create()
    sys.exit()

    #print zabbixapi.host_get()
    if sys.argv[1].lower() == "-c":
        if sys.argv[2].lower() == "-h":
            createhost(sys.argv)
        elif sys.argv[2].lower() == "-g":
            pass
            #create group
        elif sys.argv[2].lower() == "-t":
            #create template
            pass
        elif sys.argv[2].lower()== "-s":
            #create screen
            createscreen(sys.argv)

    elif sys.argv[1].lower() == "-u":
        #update object
        if sys.argv[2].lower() =="-h":
            updatehosts = sys.argv[3].split(',')
            if sys.argv[4]:
                updatestatus = sys.argv[4]
                reshost = newshowhost(updatehosts)
                for i,j in reshost.items():
                    print "host name: %s  host id: %s " %(i,j)
                isupdate = raw_input('update all host(y/n):').lower()
                if isupdate == 'y':
                    print "update plase wait"
                    print reshost
                    hostids = []
                    for i in reshost.values():
                        hostids.append({"hostid": i})

                    # hostids = reshost.values()
                    # print hostids,updatestatus
                    print zabbixapi.host_update(hostids,updatestatus)
                    sys.exit()
                else:
                    sys.exit()

    elif sys.argv[1].lower() == "-d":
        #delete object
        try:
            opts, args = getopt.getopt(sys.argv[2:],"h:t:g:s:")
        except getopt.GetoptError:
            showmenu()
        for name,value in opts:
            if name in "-h":
                deletehost(value)
            if name in "-t":
                pass
    else:
        showmenu()


if __name__ == '__main__':
    main()
    
