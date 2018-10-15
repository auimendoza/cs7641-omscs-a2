from __future__ import with_statement
"""
assign 2, part 1
sign languange mnist
"""
import os
import csv
import timeit
from time import strftime, localtime
import sys

def Usage():
    print "Usage: %s </path/to/ABAGAIL.jar> <RHC|GA|SA|BP> <label> <args>" % (sys.argv[0])
    print "    if GA, args = n_population,n_mate,n_mutate"
    print "    if SA, args = t,cooling"
    sys.exit(1)

if len(sys.argv) < 4:
    Usage()

sys.path.append(sys.argv[1])

from func.nn.backprop import BackPropagationNetworkFactory
from shared import SumOfSquaresError, DataSet, Instance
from opt.example import NeuralNetworkOptimizationProblem

import opt.RandomizedHillClimbing as RandomizedHillClimbing
import opt.SimulatedAnnealing as SimulatedAnnealing
import opt.ga.StandardGeneticAlgorithm as StandardGeneticAlgorithm
from func.nn.backprop import RPROPUpdateRule, BatchBackPropagationTrainer

INPUT_LAYER = 30
HIDDEN_LAYER = 25
OUTPUT_LAYER = 1
TRAINING_ITERATIONS = 1000

def initialize_instances(filename, i):
    instances = []

    with open(filename, "r") as f:
        reader = csv.reader(f)

        for row in reader:
            instance = Instance([float(value) for value in row[:-1]])
            instance.setLabel(Instance(int(row[-1])))
            instances.append(instance)

    return instances

def train(oa, network, oaName, ttvinstances, measure, label, suffix):
    """Train a given network on a set of instances.

    :param OptimizationAlgorithm oa:
    :param BackPropagationNetwork network:
    :param str oaName:
    :param list[Instance] instances:
    :param AbstractErrorMeasure measure:
    """
    stats = {}
    stats['iteration'] = []
    keys = ttvinstances.keys()
    for key in keys:
        stats[key] = []

    for i in xrange(TRAINING_ITERATIONS):
        oa.train()
        stats['iteration'].append(i)
        if i%100 == 0:
            print "iteration:", i
        for key, instances in zip(ttvinstances.keys(), ttvinstances.values()):
            error = 0.00
            for instance in instances:
                network.setInputValues(instance.getData())
                network.run()

                output = instance.getLabel()
                output_values = network.getOutputValues()
                example = Instance(output_values, Instance(output_values.get(0)))
                error += measure.value(output, example)
            mse = error/float(len(instances))
            stats[key].append(mse)
            if i%100 == 0:
                print "%s error = %0.10f" % (key, error)
                print "%s mse = %0.10f" % (key, mse)

    scsv = 'cc-'+oaName+'-'+label+'-'+suffix+'-mse.csv'
    print
    print "Saving to %s" % (scsv),
    with open(scsv, 'w') as csvf:
        writer = csv.writer(csvf)
        for j in stats['iteration']:
            writer.writerow([j, stats[keys[0]][j], stats[keys[1]][j], stats[keys[2]][j]])
    print "saved."

def main(trainfile, testfile, validfile, oa_name, i, params):
    print ("== [{}] ==".format(oa_name))
    res = {}
    #for i in range(25):
    res[i] = {}
    if i==9:
        print("Invalid i %d" % (i))
        sys.exit(1)
    print("LABEL: {}".format(i))
    traininstances = initialize_instances(trainfile, i)
    testinstances = initialize_instances(testfile, i)
    validinstances = initialize_instances(validfile, i)
    factory = BackPropagationNetworkFactory()
    measure = SumOfSquaresError()
    data_set = DataSet(traininstances)
    rule = RPROPUpdateRule()

    # was networks[]
    classification_network = factory.createClassificationNetwork([INPUT_LAYER, HIDDEN_LAYER, OUTPUT_LAYER])
    nnop = NeuralNetworkOptimizationProblem(data_set, classification_network, measure)

    oa = None
    # was oa = []
    suffix = ""
    if oa_name == "BP":
        oa = BatchBackPropagationTrainer(data_set,classification_network,measure,rule)
    if oa_name == "RHC":
        oa = RandomizedHillClimbing(nnop)
    if oa_name == "SA":
        suffix = '-'+'-'.join(params)
        oa = SimulatedAnnealing(float(params[0]), float(params[1]), nnop)
    if oa_name == "GA":
        suffix = '-'+'-'.join(params)
        oa = StandardGeneticAlgorithm(int(params[0]), int(params[1]), int(params[2]), nnop)

    ttvinstances = {'train': traininstances, 'test': testinstances, 'valid': validinstances}
    train_start = timeit.default_timer()
    train(oa, classification_network, oa_name, ttvinstances, measure, i, suffix)
    train_end = timeit.default_timer()
    print 'train time: %d secs' % (int(train_end-train_start))
    
    if oa_name != "BP":
      optimal_instance = oa.getOptimal()
      classification_network.setWeights(optimal_instance.getData())

    ttvinstances = {'train': traininstances, 'valid': validinstances, 'test': testinstances}
    for key, instances in zip(ttvinstances.keys(), ttvinstances.values()):
        query_start = timeit.default_timer()
        tp = 0.
        fp = 0.
        fn = 0.
        tn = 0.
        precision = 0.
        recall = 0.
        f1 = 0.
        print "scoring %s..." % (key)
        for instance in instances:
            classification_network.setInputValues(instance.getData())
            classification_network.run()

            actual = instance.getLabel().getContinuous()
            predicted = classification_network.getOutputValues().get(0)
            #print ('actual = %.3f, predicted = %.3f' % (actual, predicted))
            if actual == 1.:
                if predicted >= 0.5:
                    tp += 1.
                else: 
                    fn += 1.
            else:
                if predicted >= 0.5:
                    fp += 1.
                else:
                    tn += 1.

        query_end = timeit.default_timer()
        if tp+fp > 0.:
            precision = tp/(tp+fp)
        if fn+tp > 0.:
            recall = tp/(fn+tp)
        if precision+recall > 0.:
            f1 = 2.*precision*recall/(precision+recall)
        correct = tp + tn
        total = correct + fp + fn
        print "%s f1 = %0.10f" % (key, f1)
        print "%s accuracy = %0.10f" % (key, correct/total)
        print "%s query time: %d secs" % (key, int(query_end-query_start))

trainfile = 'cctrain.csv'
validfile =  'ccvalid.csv'
testfile =  'cctest.csv'

params = None
oa_name = sys.argv[2]
label = sys.argv[3]

if oa_name in ['GA', 'SA']:
    if len(sys.argv) != 5:
        Usage()
    params = sys.argv[4].split(',')

if oa_name == 'GA':
    TRAINING_ITERATIONS = 500
    if len(params) != 3:
        Usage()

if oa_name == 'SA':
    if len(params) != 2:
        Usage()

main(trainfile, testfile, validfile, oa_name, label, params)
