#!/bin/bash
KEY=$1
if [ -z $1 ] || [ -z $2 ]; then 
    echo "Usage $0 <key> <depth>"
    exit 1
fi
depth=$2
maxrandom=$((3 ** depth -40))
FAKE="THANK YOU MARIO! BUT OUR PRINCESS IS IN ANOTHER CASTLE!"

function CreateDir
{
    # set -xv
    typeset -i level="$1"
    typeset    dirname="$2"
    mkdir "$dirname/left"
    mkdir "$dirname/right"
    mkdir "$dirname/forward"
    rand=$((RANDOM % maxrandom))
    if [ $rand == 301 ] ; then
        echo $KEY > "$dirname/left/$(echo $KEY | md5deep)"
    elif [ $rand == 302 ] ; then
        echo $KEY > "$dirname/right/$(echo $KEY | md5deep)"
    elif [ $rand  == 303 ] ; then
        echo $KEY > "$dirname/forward/$(echo $KEY | md5deep)"
    else
        echo $FAKE > "$dirname/left/$(date +%N | md5deep)"
        echo $FAKE > "$dirname/right/$(date +%N | md5deep)"
        echo $FAKE > "$dirname/forward/$(date +%N | md5deep)"
    fi

    (( level -= 1 )) 
    
    if [ $level -gt 0 ] ; then
        CreateDir $level "$dirname/left"
        CreateDir $level "$dirname/forward"
        CreateDir $level "$dirname/right"
    fi
}
mkdir jail
time CreateDir $depth jail
echo "
Generating of labirint finished.
Please check rights and existing of file
"
