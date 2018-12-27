#!/bin/bash

if [[ $# -ne 3 ]]; then
    echo "Program must be run with the following arguments: <generator-source> <checker-source> <answer-source>"
    exit -1
fi

GREEN='\033[1;32m'
NC='\033[0m'

printf "${GREEN}"
echo "Initializing workspace..."

GENERATOR=$1
CHECKER=$2
CORRECT_SOURCE=$3

WORKSPACE_DIR=workspace

mkdir -p ${WORKSPACE_DIR} && rm -rf ${WORKSPACE_DIR}/*

compile() {
    if [[ $1 == *.c* ]]; then
        g++ ${1} -o ${1/.*}
        mv ${1/.*} ${WORKSPACE_DIR}
    elif [[ $1 == *.java ]]; then
        javac $1
        mv ${1/.*} ${WORKSPACE_DIR}
    elif [[ $1 == *.py ]]; then
        cp $1 ${WORKSPACE_DIR}
    else
        echo "not supported"
        printf "${NC}"
    fi
}

compile ${GENERATOR} &> /dev/null
compile ${CHECKER} &> /dev/null
compile ${CORRECT_SOURCE} &> /dev/null

echo "Workspace is ready!!"
printf "${NC}"

exit 0