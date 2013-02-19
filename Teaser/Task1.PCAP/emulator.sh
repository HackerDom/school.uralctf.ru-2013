#!/bin/bash
if [ -z $1 ]; then
    echo "Usage: $0 <message>"
    exit 1
fi

hosts="google.ru e1.ru vk.com ructf.org hackerdom.ru kontur.ru 8.8.8.8"
for host in $hosts; do
    echo $host
    if [ $host == '8.8.8.8' ]; then
        ./icmp_echo.sh $host $1
    else
        ping -c 5 $host
    fi
    sleep 5
done
