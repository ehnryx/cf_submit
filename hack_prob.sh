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
        if [[ $1 == *11* ]]; then
            g++ ${1} -static -DONLINE_JUDGE -lm -s -x c++ -Wl,--stack=268435456 -O2 -std=c++11 -o ${1/.*}
        elif [[ $1 == *14* ]]; then
            g++ ${1} -static -DONLINE_JUDGE -lm -s -x c++ -Wl,--stack=268435456 -O2 -std=c++14 -o ${1/.*}
        elif [[ $1 == *17* ]]; then
            g++ ${1} -static -DONLINE_JUDGE -lm -s -x c++ -Wl,--stack=268435456 -O2 -std=c++17 -o ${1/.*}
        else
            g++ ${1} -static -DONLINE_JUDGE -lm -s -x c++ -Wl,--stack=268435456 -O2 -o ${1/.*}
        fi
    elif [[ $1 == *.c ]]; then
        gcc -static -fno-optimize-sibling-calls -fno-strict-aliasing -DONLINE_JUDGE -fno-asm -lm -s -Wl,--stack=268435456 -O2 -o ${1/.*}
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
            java -Xmx512M -Xss64M -DONLINE_JUDGE=true -Duser.language=en -Duser.region=US -Duser.variant=US ${1/.*} $2
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
        EXIT_CODE=$?
        if [[ ${EXIT_CODE} -ne 0 ]]; then
            printf "${YELLOW}"
            echo "Execution error - code $EXIT_CODE !!"
            echo -en "\007"
            clean
            if [[ ${EXIT_CODE} -eq -1 ]]; then
                exit -1
            else
                exit 1
            fi
        fi
        execute ${CORRECT_SOURCE}  ${i} ${i/.in/.ans} &> /dev/null
        execute ${CHECKER} ${i} ${i/.in/.out} ${i/.in/.ans} &> /dev/null
        EXIT_CODE=$?
        if [[ ${EXIT_CODE} -ne 0 ]]; then
            printf "${GREEN}"
            cat ${i} > ${FAILED_TEST}
            echo "Can be Hacked"
	        echo -en "\007"
            clean
            exit ${EXIT_CODE}
        fi
    fi
done

echo "All tests passed!!"

clean

exit ${EXIT_CODE}
