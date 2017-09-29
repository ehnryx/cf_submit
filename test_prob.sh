echo "Testing problem $1"
for i in "$1*.in"; do
	./a < "$i" > "${i%.in}.out"
	diff "${i%.in}.out" "${i%.in}.ans"
done
