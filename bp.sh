echo "Running BP"
echo "================"
#jy nncc.py $ABAGAIL_PATH BP 99
for i in 1 2 3 4 5
do
jy nncc.py $ABAGAIL_PATH BP $i
done
