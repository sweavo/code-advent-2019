#!/bin/bash
find . -name \*.py -type f| while read a; do (cd $(dirname $a); py -m doctest $(basename $a)); done

