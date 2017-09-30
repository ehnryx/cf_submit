echo "Testing problem $1"
for i in $1*.in; do
	echo "Running on file $i"
	"./$1" < "$i" > "${i%.in}.out"
	"diff" "-b" "${i%.in}.out" "${i%.in}.ans"
done
