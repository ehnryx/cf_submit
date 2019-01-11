#!/bin/bash

if [[ $# -ne 5 ]]; then
    echo "Program must be run with the following arguments: <generator-source> <checker-source> <answer-source>
                <for-hack-source> <for-hack-source-language>"
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

WORKSPACE_DIR=workspace
FAILED_TEST=failed.txt
TEST_TLE=test_tle.in
EXIT_CODE=0

cd ${WORKSPACE_DIR}

compile() {
    if [[ $1 == *.cpp ]]; then
        g++ ${1} -DONLINE_JUDGE -o ${1/.*}
    elif [[ $1 == *.c ]]; then
        echo "${2} c"
        gcc ${1} -DONLINE_JUDGE -o ${1/.*}
    elif [[ $1 == *.java ]]; then
        echo "${2} java"
        javac $1
    elif [[ $1 == *.py ]]; then
        echo "${2} python"
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
    rm -rf test_tle.in test_tle.out test_tle.ans
    printf "${NC}"
}

compile ${NOT_SURE_SOURCE} ${LANGUAGE} &> /dev/null

execute ${GENERATOR} 1 > ${TEST_TLE}

if [[ $? -ne 0 ]]; then
    exit ${EXIT_CODE};
fi

if [[ -f ${TEST_TLE} ]]; then
    execute ${NOT_SURE_SOURCE} test_tle.in test_tle.out &> /dev/null
    EXIT_CODE=$?
    if [[ ${EXIT_CODE} -ne 0 ]]; then
        printf "${YELLOW}"
        echo -en "\007"
        clean
        if [[ ${EXIT_CODE} -eq -1 ]]; then
            exit -1
        else
            exit 1
        fi
    fi
    execute ${CORRECT_SOURCE} test_tle.in test_tle.ans &> /dev/null
    execute ${CHECKER} test_tle.in test_tle.out test_tle.ans
    EXIT_CODE=$?
    if [[ ${EXIT_CODE} -ne 0 ]]; then
        printf "${GREEN}"
        cat ${i} > ${FAILED_TEST}
        echo -en "\007"
        clean
        exit ${EXIT_CODE}
    fi
fi

clean

exit ${EXIT_CODE}
