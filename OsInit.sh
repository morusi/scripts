#!/bin/sh
# Create by Mo..
# MAIL:
# QQ群:78156746
# Centos 6.6
cat << EOF
+--+
|=== Welcome to Centos System init ===|
+--+
+--Please use root to do !--+
+--by Mo..--+
EOF


show(){
#print the result 
if [ $1 -eq 0 ] ;then
    echo " The $2 is OK!"
else
    echo " The $2 is error!"
fi

}

# install base Package

[ $(ping -c 1 -w 1 www.baidu.com 2>&1| grep "unknown host" |wc -l) -eq 1 ] && echo "nameserver 114.114.114.114" >> /etc/resolv.conf

yum makecache >/dev/null 2>&1
if [ $? -eq 0 ];then
    yum install vim  -y >/dev/null 2>&1
    show $? "base Package install" 
else
    echo 'yum not used,base Package not install!'
fi

# set ntp
#yum install ntp  -y /dev/null 2>&1
#echo "00 00 * * * /usr/sbin/ntpdate cn.pool.ntp.org >/dev/null 2>&1" >> /var/spool/cron/root
#service crond start
#/sbin/chkconfig --level 35 crond on

#config vi 
if [ ! -f ~/.vimrc ] ;then
cat >> ~/.vimrc << EOF
colorscheme darkblue
set tabstop=4
set expandtab
set shiftwidth=4
set softtabstop=4 
EOF
else
    [ $(cat ~/.vimrc | grep  colorscheme |wc -l) = 0 ]  && echo  "colorscheme darkblue" >> ~/.vimrc 
    [ $(cat ~/.vimrc | grep  tabstop |wc -l) = 0 ]      && echo  "set tabstop=4" >> ~/.vimrc 
    [ $(cat ~/.vimrc | grep  expandtab |wc -l) = 0 ]    && echo  "set expandtab" >> ~/.vimrc 
    [ $(cat ~/.vimrc | grep  shiftwidth |wc -l) = 0 ]   && echo  "set shiftwidth=4" >> ~/.vimrc 
    [ $(cat ~/.vimrc | grep  softtabstop |wc -l) = 0 ]  && echo  "set softtabstop=4 " >> ~/.vimrc 
fi

# disable selinux
setenforce 0
sed -i '/SELINUX/s/enforcing/disabled/' /etc/selinux/config
show $? "selinux"

# disable iptables 
iptables -F 
/sbin/chkconfig --level 35 iptables off 
show $? "iptables"

# close ctrl+alt+del
sed -i 's@start on@stop on@' /etc/init/control-alt-delete.conf
show $? " close ctrlaltdel "

# disable ipv6
if [ ! -f /etc/modprobe.conf ] ; then
    echo "alias net-pf-10 off" >> /etc/modprobe.conf
    echo "alias ipv6 off" >> /etc/modprobe.conf
else
    [ $(cat /etc/modprobe.conf | grep  net-pf-10 |wc -l) = 0 ]  && echo  "alias net-pf-10 off" >> /etc/modprobe.conf
    [ $(cat /etc/modprobe.conf | grep  ipv6 |wc -l) = 0 ]       && echo  "alias ipv6 off" >> /etc/modprobe.conf
fi

/sbin/chkconfig --level 35 ip6tables off
show $? "disable ipv6"
