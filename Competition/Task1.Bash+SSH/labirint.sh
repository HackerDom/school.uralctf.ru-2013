#!/bin/bash
KEY=$1
if [ -z $1 ]; then 
    echo "Usage $0 <key>"
    exit 1
fi

function CreateDir
{
    # set -xv
    typeset -i level="$1"
    typeset    dirname="$2"
    mkdir "$dirname/left"
    if [ $RANDOM == 31337 ] ; then
        echo $KEY > "$dirname/left/$(echo $KEY | md5deep)"
    fi
    mkdir "$dirname/right"
    if [ $RANDOM == 31337 ] ; then
        echo $KEY > "$dirname/right/$(echo $KEY | md5deep)"
    fi
    mkdir "$dirname/forward"
    if [ $RANDOM  == 31337 ] ; then
        echo $KEY > "$dirname/forward/$(echo $KEY | md5deep)"
    fi

    (( level -= 1 )) 
    
    if [ $level -gt 0 ] ; then
        CreateDir $level "$dirname/left"
        CreateDir $level "$dirname/forward"
        CreateDir $level "$dirname/right"
    fi
}

CreateDir 13 jail
echo
