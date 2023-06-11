#!/bin/bash

EXPAND=true
while getopts 'hef:' OPTION; do
    case "$OPTION" in
        f)
            FILE_VAL="$OPTARG"
            ;;
        e)
            EXPAND=false
            ;;
        h)
            echo "usage: ./$(basename $0) -f <file with ips> [optional -e]"
            echo "f: specify the file containing either cidr addresses or expanded ips"
            echo "e: if set then the stage of expanding cidr addresses into individual ips will be SKIPPED"
            exit 0
            ;;
        ?)
            echo "usage: ./$(basename $0) -f <file with cidr ips> [optional -e]"
            exit 1
            ;;

    esac
done
shift "$(($OPTIND -1))"

if [ -z "$FILE_VAL" ]; then
    echo 'Missing -f flag' >&2
    exit 1
fi


if [ $EXPAND == true ]; then
    #expanding the CIDR values in the file into individual ips
    IFS=$'\n' read -d '' -r -a ip < $FILE_VAL
    expanded_file="expanded_$FILE_VAL"
    touch $expanded_file
    for i in "${ip[@]}" # and yes even in bash I use "i" in for loops ;)
    do
        python3 CIDR_EXPAND.py $i >> $expanded_file
    done
else
    expanded_file="$FILE_VAL"
fi
httpx_out="httpx.out"
if [ -f "final.txt" ]; then
    httpx_out="$httpx_out.new"
fi

cat $expanded_file | naabu -p - -silent -rate | httpx -silent -cl -wc -title -json | python3 httpx_json_formatter.py - > $httpx_out 