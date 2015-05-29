#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re
from zabbix_api import ZabbixTools
from optparse import OptionParser


def main():
#     url = "http://192.168.1.17/zabbix/api_jsonrpc.php"
#     user = "yige.han"
#     passwd = "hanyige"
#     global  zabbixapi
#     zabbixapi = ZabbixTools(url,user,passwd)
    parser = OptionParser()
    parser.add_option("-C", "--create", dest = "iscreate", action = "store_true", default = False
                    , help = "create the object" )
    parser.add_option("-U", "--update", dest = "isupdate", action = "store_true", default = False
                    , help = "update the object" )
    parser.add_option("-D", "--delete", dest = "isdelete", action = "store_true", default = False
                    , help = "delete the object" )
        
    parser.add_option("-a", "--host", dest = "host", help = "HOST:'hostname, hostip' exact a host")
    parser.add_option("-A", dest = "hosts", help = "hosts:'hostname1,hostname2' search host in zabbix")
    parser.add_option("-t", "--template", dest = "templates", help = "templates: 'template1,template2'exact a template" )
    parser.add_option("-T", "--templats", dest = )
#     parser.add_option()
#     parser.add_option()
    (options, args) = parser.parse_args()
if __name__ == '__main__':
    main()