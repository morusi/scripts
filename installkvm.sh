#!/bin/bash
# Create by Mo..
# MAIL:
# QQ群:78156746
# Centos 6.6 mini

cat << EOF
+--+
|=== Welcome to KVM install scripts ===|
+--+
+--by Mo..--+
EOF

help(){
    echo "$0 useage:"
    echo "\t -i net name \te.g: -i eth0 "
    echo "\t -p ipaddress \te.g: -p 192.168.6.100 "
    echo "\t -m netmask  \te.g: -m 255.255.255.0"
    echo "\t -g gateway ip \te.g: -g 192.168.6.254 "
    exit 0
}

while [ -n $1 ]
do
    case "$1" in
        -h|--help)
            help
        -i|-I)
            let intername=$2
                
        -p|-P)
        -m|-M)
        -g|-G)
        *)
#check the VT
grep -E 'svm|vmx' /proc/cpuinfo >/dev/null 2>&1
if [ $? -eq 0 ] ;then
    echo "VT enable"
else
    echo 'VT disable, Please check BIOS config!'
    exit 1
fi

yum install qemu-kvm libvirt libvirt-python libguestfs-tools virt-install -y >/dev/null 2>&1

if [ $? -eq 0 ] ;then
    echo 'all install ok!'
else
    echo 'yum isntall error! Please check yum config!'
fi



 