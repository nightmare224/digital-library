#!/bin/bash
ABSPATH=`readlink -f $0`
DIRPATH=`dirname $ABSPATH`
cd ${DIRPATH}


# run app
python3 main.py