#!/bin/bash

if [[ $# -ne 5 ]]; then
    echo "Program must be run with the following arguments: <generator-source> <checker-source> <answer-source> <for-hack-source> <for-hack-source-language>"
    exit -1
fi

GREEN='\033[1;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

printf "${YELLOW}"

GENERATOR=$1
CHECKER=$2
CORRECT_SOURCE=$3
NOT_SURE_SOURCE=$4
LANGUAGE=$5

WORKSPACE_DIR=workspace
FAILED_TEST=failed.txt
EXIT_CODE=0
TEST_NUMBERS=10

cd ${WORKSPACE_DIR}

compile() {
    if [[ $1 == *.c* ]]; then
        g++ ${1} -o ${1/.*} -DONLINE_JUDGE
    elif [[ $1 == *.java ]]; then
        javac $1
    elif [[ $1 == *.py ]]; then
        continue
    else
        echo "not supported"
        clean
        exit -1
    fi
}

execute() {
    if [[ $1 == *.c* ]]; then
        if [[ $# -eq 2 ]]; then
            ./${1/.*} $2
        elif [[ $# -eq 3 ]]; then
            ./${1/.*} < $2 > $3
        else
            ./${1/.*} ${@:2}
        fi
    elif [[ $1 == *.java ]]; then
        if [[ $# -eq 2 ]]; then
            java -DONLINE_JUDGE=true ${1/.*} $2
        elif [[ $# -eq 3 ]]; then
            java -DONLINE_JUDGE=true ${1/.*} < $2 > $3
        else
            java -DONLINE_JUDGE=true ${1/.*} ${@:2}
        fi
    elif [[ $1 == *.py ]]; then
        if [[ ${LANGUAGE} == *2* ]]; then
            exec=python2
        else
            exec=python3
        fi
        if [[ $# -eq 2 ]]; then
            ${exec} $1 $2
        elif [[ $# -eq 3 ]]; then
            ${exec} $1 < $2 > $3
        else
            ${exec} $1 ${@:2}
        fi
    else
        echo "not supported"
        clean
        exit -1
    fi
}

clean() {
    rm -rf test*.in test*.out test*.ans
    printf "${NC}"
}

compile ${NOT_SURE_SOURCE} &> /dev/null

execute ${GENERATOR} ${TEST_NUMBERS} &> /dev/null

for i in test*.in; do
    if [[ -f ${i} ]]; then
        execute ${NOT_SURE_SOURCE} ${i} ${i/.in/.out} &> /dev/null
        if [[ $? -ne 0 ]]; then
            echo "Execution error!!"
            exit -1
        fi
        execute ${CORRECT_SOURCE} ${i} ${i/.in/.ans} &> /dev/null
        execute ${CHECKER} ${i} ${i/.in/.out} ${i/.in/.ans} &> /dev/null
        EXIT_CODE=$?
        if [[ ${EXIT_CODE} -ne 0 ]]; then
            printf "${GREEN}"
            cat ${i} > ${FAILED_TEST}
            echo "Can be Hacked, trying..."
            clean
            exit ${EXIT_CODE}
        fi
    fi
done

echo "$TEST_NUMBERS tests passed :/"

clean

exit ${EXIT_CODE}