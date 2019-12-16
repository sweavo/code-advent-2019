#!/bin/bash
find . -name \*.py -type f| while read a
do
    echo $a
    (
        cd $(dirname $a)
        py -m doctest $(basename $a)
    )
done

