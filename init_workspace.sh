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
    if [[ $1 == *.cpp ]]; then
        if [[ $1 == *11* ]]; then
            g++ ${1} -static -DONLINE_JUDGE -lm -s -x c++ -Wl,--stack=268435456 -O2 -std=c++11 -o ${1/.*}
        elif [[ $1 == *14* ]]; then
            g++ ${1} -static -DONLINE_JUDGE -lm -s -x c++ -Wl,--stack=268435456 -O2 -std=c++14 -o ${1/.*}
        elif [[ $1 == *17* ]]; then
            g++ ${1} -static -DONLINE_JUDGE -lm -s -x c++ -Wl,--stack=268435456 -O2 -std=c++17 -o ${1/.*}
        else
            g++ ${1} -static -DONLINE_JUDGE -lm -s -x c++ -Wl,--stack=268435456 -O2 -o ${1/.*}
        fi
        mv ${1/.c*} ${WORKSPACE_DIR}
    elif [[ $1 == *.c ]]; then
        gcc -static -fno-optimize-sibling-calls -fno-strict-aliasing -DONLINE_JUDGE -fno-asm -lm -s -Wl,--stack=268435456 -O2 -o ${1/.*}
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

compile ${GENERATOR} &> /dev/null
compile ${CHECKER} &> /dev/null
compile ${CORRECT_SOURCE} &> /dev/null

echo "Workspace is ready!!"
printf "${NC}"

exit 0