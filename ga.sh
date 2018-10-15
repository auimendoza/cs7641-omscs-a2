echo "Running GA"
echo "================"
for p in 100
do
for ma in 50 20
do
for mu in 10 5
do
jy nncc.py $ABAGAIL_PATH GA 99 $p,$ma,$mu
done
done
done
