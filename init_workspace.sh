#!/bin/bash

if [[ $# -ne 4 ]]; then
    echo "Program must be run with the following arguments: <small-generator-source> <big-generator-source> <checker-source> <answer-source>"
    exit -1
fi

GREEN='\033[1;32m'
NC='\033[0m'

printf "${GREEN}"
echo "Initializing workspace..."

SMALL_GENERATOR=$1
BIG_GENERATOR=$2
CHECKER=$3
CORRECT_SOURCE=$4

WORKSPACE_DIR=workspace

mkdir -p ${WORKSPACE_DIR} && rm -rf ${WORKSPACE_DIR}/*

compile() {
    if [[ $1 == *.cpp ]]; then
        g++ ${1} -o ${1/.*}
        mv ${1/.c*} ${WORKSPACE_DIR}
    elif [[ $1 == *.c ]]; then
        gcc ${1} -o ${1/.*}
        mv ${1/.c*} ${WORKSPACE_DIR}
    elif [[ $1 == *.java ]]; then
        cp $1 ${WORKSPACE_DIR}
        javac ${WORKSPACE_DIR}/$1
    elif [[ $1 == *.py ]]; then
        cp $1 ${WORKSPACE_DIR}
    else
        echo "not supported"
        printf "${NC}"
    fi
}

compile ${SMALL_GENERATOR} 
compile ${BIG_GENERATOR} 
compile ${CHECKER} 
compile ${CORRECT_SOURCE} 

echo "Workspace is ready!!"
printf "${NC}"

exit 0