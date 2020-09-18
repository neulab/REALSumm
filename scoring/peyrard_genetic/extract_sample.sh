echo "taking every 10th line from each file in $1 and writing to corresponding files in $2"
mkdir $2
for f in $1/*; do
  out_f=$2/"$(basename $f)"
  echo "input: $f , output: $out_f"
  awk 'NR % 10 == 0' $f > $out_f
done