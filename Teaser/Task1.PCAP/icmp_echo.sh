#!/bin/bash
if [ -z $1 ] || [ -z $2 ]; then
    echo "Usage $0 <address> <message>"
    exit 1
fi;
message=$(echo $2 | fold -w1)
for c in $message; do
    hping2 -1 -c 1 -e "$c" $1 2> /dev/null
    sleep 2
done
