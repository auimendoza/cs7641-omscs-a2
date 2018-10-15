import sys
import os
import timeit
import csv

def Usage():
    print "Usage: %s </path/to/ABAGAIL.jar> <RHC|GA|SA|MMC> <args>" % (sys.argv[0])
    print "    if RHC, args = iterations,nthtry"
    print "    if GA, args = n_population,n_mate,n_mutate"
    print "    if SA, args = t,cooling"
    print "    if MMC, args = samples,tokeep"
    sys.exit(1)

if len (sys.argv) != 4:
  Usage()

sys.path.append(sys.argv[1])

import java.io.FileReader as FileReader
import java.io.File as File
import java.lang.String as String
import java.lang.StringBuffer as StringBuffer
import java.lang.Boolean as Boolean
import java.util.Random as Random

import dist.DiscreteDependencyTree as DiscreteDependencyTree
import dist.DiscreteUniformDistribution as DiscreteUniformDistribution
import dist.Distribution as Distribution
import opt.DiscreteChangeOneNeighbor as DiscreteChangeOneNeighbor
import opt.EvaluationFunction as EvaluationFunction
import opt.GenericHillClimbingProblem as GenericHillClimbingProblem
import opt.HillClimbingProblem as HillClimbingProblem
import opt.NeighborFunction as NeighborFunction
import opt.RandomizedHillClimbing as RandomizedHillClimbing
import opt.SimulatedAnnealing as SimulatedAnnealing
import opt.example.FourPeaksEvaluationFunction as FourPeaksEvaluationFunction
import opt.ga.CrossoverFunction as CrossoverFunction
import opt.ga.SingleCrossOver as SingleCrossOver
import opt.ga.DiscreteChangeOneMutation as DiscreteChangeOneMutation
import opt.ga.GenericGeneticAlgorithmProblem as GenericGeneticAlgorithmProblem
import opt.ga.GeneticAlgorithmProblem as GeneticAlgorithmProblem
import opt.ga.MutationFunction as MutationFunction
import opt.ga.StandardGeneticAlgorithm as StandardGeneticAlgorithm
import opt.ga.UniformCrossOver as UniformCrossOver
import opt.prob.GenericProbabilisticOptimizationProblem as GenericProbabilisticOptimizationProblem
import opt.prob.MIMIC as MIMIC
import opt.prob.ProbabilisticOptimizationProblem as ProbabilisticOptimizationProblem
import shared.FixedIterationTrainer as FixedIterationTrainer
import opt.example.ContinuousPeaksEvaluationFunction as ContinuousPeaksEvaluationFunction
from array import array

def solveit(oaname, params):
    N=60
    T=N/10
    fill = [2] * N
    ranges = array('i', fill)
    iterations = 10000
    tryi = 1

    ef = ContinuousPeaksEvaluationFunction(T)
    odd = DiscreteUniformDistribution(ranges)
    nf = DiscreteChangeOneNeighbor(ranges)
    mf = DiscreteChangeOneMutation(ranges)
    cf = SingleCrossOver()
    df = DiscreteDependencyTree(.1, ranges)
    hcp = GenericHillClimbingProblem(ef, odd, nf)
    gap = GenericGeneticAlgorithmProblem(ef, odd, mf, cf)
    pop = GenericProbabilisticOptimizationProblem(ef, odd, df)

    #  fit = FixedIterationTrainer(rhc, 200000)
    #  fit.train()

    if oaname == 'RHC':
        iterations = int(params[0])
        tryi = int(params[1])
        oa = RandomizedHillClimbing(hcp)
    if oaname == 'SA':
        oa = SimulatedAnnealing(float(params[0]), float(params[1]), hcp)
    if oaname == 'GA':
        oa = StandardGeneticAlgorithm(int(params[0]), int(params[1]), int(params[2]), gap)
    if oaname == 'MMC':
        oa = MIMIC(int(params[0]), int(params[1]), pop)

    print "Running %s using %s for %d iterations, try %d" % (oaname, ','.join(params), iterations, tryi)
    print "="*20
    starttime = timeit.default_timer()
    output = []
    for i in range(iterations):
        oa.train()
        if i%10 == 0:
            optimal = oa.getOptimal()
            score = ef.value(optimal)
            elapsed = float(timeit.default_timer()-starttime)
            output.append([str(i), str(score), str(elapsed)])

    print 'score: %.3f' % score
    print 'train time: %.3f secs' % (int(timeit.default_timer()-starttime))

    scsv = 'cp-%s-%s.csv' % (oaname, '-'.join(params))
    print "Saving to %s" % (scsv),
    with open(scsv, 'w') as csvf:
        writer = csv.writer(csvf)
        for row in output:
            writer.writerow(row)
    print "saved."
    print "="*20

oaname = sys.argv[2]
params = sys.argv[3].split(',')

if oaname == 'GA':
    if len(params) != 3:
        Usage()

if oaname in ('SA', 'MMC', 'RHC'):
    if len(params) != 2:
        Usage()

solveit(oaname, params)
