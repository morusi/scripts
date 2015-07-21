#!/bin/bash
#

declare -f ifexist 
declare  newpasswd=gumi123
ifexist()
{
    `cat "/etc/passwd" | grep $1 > /dev/null`
    if [ $? = 0 ]; then
        return 1;
    else
        return 2; #no user
    fi
}

if [ $# = 0 ]; then
	echo "Usage: `basename $0` [-A\-D] username -P password
            -A add user  
            -D del user 
            -P set password ,if not -p the default password is gumi123"
    exit 0
fi
if [ $# -gt 0 ] ;then
    case $1 in
    -h|--help)
          echo "Usage: `basename $0` [-A\-D] username -P password
            -A add user (default) 
            -D del user 
            -P set password ,if not -p the default password is gumi123"
             exit 0;;
    -a|-A)
            let user_add=0
            shift ;;
    -d|-D)
            let user_add=1 
            shift ;;
    *)   
        echo "Usage: `basename $0` [-A\-D] username -P password
            -A add user (default) 
            -D del user 
            -P set password ,if not -p the default password is gumi123"
             exit 0;;
    esac
    if [ $user_add = 0 ]; then
        ifexist $1 
        if [ $? = 1 ]; then
            echo "`basename $0`: user '$1' already exists! "
            exit 
        else 
            echo "user not exist"
            case $2 in
                -p|-P)
                echo $1 $2 $3
                newpasswd=$3 ;;
            esac 
            err0=`useradd -s /sbin/nologin -G public  $1 && echo $newpasswd |passwd --stdin $1   2&>1    >/dev/null  `
            if [ $? = 0 ]; then
                echo "`basename $0`: $1 is create succeed and the password is $newpasswd"
                echo "$newpasswd">/tmp/smbpw ;echo "$newpasswd">> /tmp/smbpw 
                err1=`smbpasswd -as $1 < /tmp/smbpw >/dev/null >`
                if [ $? = 0 ]; then
                    echo "`basename $0`: smbuser  $1 create succeed and the password is $newpasswd!"
                    rm -rf /tmp/smbpw
                else
                    echo "`basename $0`: smbuser create failure!"
                    rm -rf /tmp/smbpw
                fi
            else
                echo "`basename $0`: $1 is create failure"
                echo "$err0"
                exit 
            fi
        fi     
    else
        ifexist $1
        if [ $? = 1 ]; then
#            echo "user exit"
            err2=`smbpasswd -n $1 2&>1  >/dev/mull `
            err3=`userdel -r $1  2&>1  >/dev/null`
            if [ $? = 0 ]; then
                echo "`basename $0`: $1 is delete succeed !"
            else
                echo "`basename $0`: $1 is delete failure!"
                echo $err3
                exit 
            fi
        else 
            echo "`basename $0`: $1 is delete failure  user is not exist!"
        fi
    fi
fi