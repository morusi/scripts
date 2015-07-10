#!/bin/sh
# Create by Mo..
# MAIL:
# QQ群:78156746
# Centos 6.6
cat << EOF
+--+
|=== Welcome to Centos System init ===|
+--+
+--by Mo..--+
EOF

# set ntp
#yum install ntp  -y
#echo "00 00 * * * /usr/sbin/ntpdate cn.pool.ntp.org >/dev/null 2>&1" >> /var/spool/cron/root
#service crond start
#/sbin/chkconfig --level 35 crond on

# install base Package
yum install vim -y

# config vi 
cat >> ~/.vimrc << EOF
colorscheme darkblue
set tabstop=4
set expandtab
set shiftwidth=4
set softtabstop=4 
EOF
# disable selinux
setenforce 0
sed -i '/SELINUX/s/enforcing/disabled/' /etc/selinux/config

# disable iptables 
iptables -F 
/sbin/chkconfig --level 35 iptables off 

# close ctrl+alt+del
sed -i 's@start on@stop on@' /etc/init/control-alt-delete.conf

# disable ipv6
echo "alias net-pf-10 off" >> /etc/modprobe.conf
echo "alias ipv6 off" >> /etc/modprobe.conf
/sbin/chkconfig --level 35 ip6tables off




