#!/bin/bash

watch="$1"

shift

while true
do
    if [[ "$watch" -nt .touchme ]]
    then
        touch .touchme
        echo ">> $@"
        "$@"
    fi
    sleep 1
done

