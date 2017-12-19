#!/bin/bash

if [[ $1 == *.py ]]; then
	name=${1/.py}
	echo "Testing problem $name"
	for i in $name*.in; do
		echo "Running on file $i"
		if [[ $2 == "-v" ]]; then
			time python $1 < $i > ${i/.in/.out}
		else
			python $1 < $i > ${i/.in/.out}
		fi
	done
else
	echo "Testing problem $1"
	for i in $1*.in; do
		echo "Running on file $i"
		if [[ $2 == "-v" ]]; then
			time "./$1" < "$i" > "${i/.in/.out}"
		else
			"./$1" < "$i" > "${i/.in/.out}"
		fi
		"diff" "-b" "${i/.in/.out}" "${i/.in/.ans}"
	done
fi
