echo "Solving continuous peaks..."

echo
echo RHC
for t in 1 2 3 4 5
do
 for i in 20000 10000
 do
  jy continuouspeaks.py $ABAGAIL_PATH RHC $i,$t
 done
done

echo
echo SA
for c in 0.15 0.35 0.55 0.75 0.95
do 
jy continuouspeaks.py $ABAGAIL_PATH SA 1E10,$c
done

echo
echo GA
for p in 200 100
do 
 for ma in 100 50 10
 do 
  for mu in 50 10
  do 
   jy continuouspeaks.py $ABAGAIL_PATH GA $p,$ma,$mu
  done
 done
done

echo
echo MIMIC
for s in 200 100
do
 for k in 50 20 10
 do 
  jy continuouspeaks.py $ABAGAIL_PATH MMC $s,$k
 done
done
