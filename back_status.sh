#!/bin/bash

zabbix_sign=/tmp/zabbix_sign_gitback.txt

status = `cat $zabbix_sign`
echo '1' > $zabbix_sign
if [ status -eq 0 ];then
    return 0
else
    return 1
