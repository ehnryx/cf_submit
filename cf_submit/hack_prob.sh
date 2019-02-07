#!/bin/bash

if [[ $# -ne 6 ]]; then
    echo "Program must be run with the following arguments: <generator-source> <checker-source> <answer-source>
                <for-hack-source> <for-hack-source-language> <test-number>"
    exit -1
fi

GREEN='\033[32m'
YELLOW='\033[33m'
NC='\033[0m'

printf "${YELLOW}"

GENERATOR=$1
CHECKER=$2
CORRECT_SOURCE=$3
NOT_SURE_SOURCE=$4
LANGUAGE=$5
TEST_NUMBERS=$6

WORKSPACE_DIR=workspace
FAILED_TEST=failed.txt
EXIT_CODE=0

cd ${WORKSPACE_DIR}

compile() {
    if [[ $1 == *.cpp ]]; then
        g++ ${1} -DONLINE_JUDGE -O2 -o ${1/.*}
    elif [[ $1 == *.c ]]; then
        echo "${2} c"
        gcc ${1} -DONLINE_JUDGE -O2 -o ${1/.*}
    elif [[ $1 == *.java ]]; then
        echo "${2} java"
        javac $1
    elif [[ $1 == *.py ]]; then
        echo "${2} python"
    else
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
            java -Xmx512M -Xss64M -DONLINE_JUDGE=true -DLOCAL=true -Duser.language=en -Duser.region=US -Duser.variant=US ${1/.*} $2
        elif [[ $# -eq 3 ]]; then
            java -Xmx512M -Xss64M -DONLINE_JUDGE=true -Duser.language=en -Duser.region=US -Duser.variant=US ${1/.*} < $2 > $3
        else
            java -Xmx512M -Xss64M -DONLINE_JUDGE=true -Duser.language=en -Duser.region=US -Duser.variant=US ${1/.*} ${@:2}
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
        clean
        exit -1
    fi
}

clean() {
    rm -rf test*.in test*.out test*.ans
    printf "${NC}"
}

compile ${NOT_SURE_SOURCE} ${LANGUAGE} &> /dev/null

execute ${GENERATOR} ${TEST_NUMBERS} &> /dev/null

for i in test*.in; do
    if [[ -f ${i} ]]; then
        execute ${NOT_SURE_SOURCE} ${i} ${i/.in/.out} &> /dev/null
        EXIT_CODE=$?
        if [[ ${EXIT_CODE} -ne 0 ]]; then
            printf "${YELLOW}"
            echo "error ${EXIT_CODE}"
            clean
            exit -1
        fi
        execute ${CORRECT_SOURCE} ${i} ${i/.in/.ans} &> /dev/null
        execute ${CHECKER} ${i} ${i/.in/.out} ${i/.in/.ans}
        EXIT_CODE=$?
        if [[ ${EXIT_CODE} -ne 0 ]]; then
            cat ${i} > ${FAILED_TEST}
            # if [[ ${i} == "test0.in" ]]; then
            #     exit -1
            # fi
	        echo -en "\007"
            clean
            exit ${EXIT_CODE}
        fi
    fi
done

clean

exit ${EXIT_CODE}
