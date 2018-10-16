Assignment 2: Randomized Optimization
CS7641 - Machine Learning
OMSCS Fall 2018

How to run scripts:
Requirements: 
1. unix-like system

2. jython.jar
3. ABAGAIL.jar built from pushkar's latest code from https://github.com/pushkar/ABAGAIL

Steps
1. define your abagail path
$ export ABAGAIL_PATH=/path/to/ABAGAIL.jar

2. define jython alias jy
$ alias jy="java -jar /path/to/jython.jar"

3. go to student main directory, mmendoza32. 
   this should contain the following files:

$ ls
README.txt		cpeaks.sh		rhc.sh
bp.sh			ga.sh			sa.sh
cctest.csv		knack.sh		travelingsalesman.py
cctrain.csv		knapsack.py		tsp.sh
ccvalid.csv		mmendoza32-analysis.pdf
continuouspeaks.py	nncc.py

4. run each script:

for part 1:

$ . ./ga.sh
$ . ./sa.sh
$ . ./rhc.sh

for part 2:

$ . ./knack.sh
$ . ./tsp.sh
$ . ./cpeaks.sh


EOF
