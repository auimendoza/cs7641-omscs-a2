echo "Running 99 SA"
echo "================"
for t in 100. 1E10
do
for c in 0.25 0.5 0.75 0.95
do
jy nncc.py $ABAGAIL_PATH SA 99 $t,$c
done
done
