echo "Running 99 RHC"
echo "================"
for i in 1 2 3 4 5
do
jy nncc.py $ABAGAIL_PATH RHC $i
done
