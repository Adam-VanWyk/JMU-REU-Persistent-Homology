from predictedPersistentComputations import *
from collections import Counter
from math import pi
from prismComputations import *
from ripser import ripser
import numpy as np
def persOfFamily(family, maxDim, edgeScale, maxN, minN=3):
	# family should take in an integer n>=minN and return a distance matrix for that size
	# maxDim is the maximum dimension to calculate the PH for
	# edgeScale is a function which takes in an integer which is the parameter to family and gives us the amount by which to scale the edges. For example, it's 2pi/n for the circle.
	# minN and maxN are the minimum and maximum values of N to compute
	# returns: a dictionary where the keys are homology dimensions, and for each homology dimension, we get a dict of the scaled PH for each value of n
	PHDict = [dict() for n in range(maxDim + 1)]
	for size in range(minN, maxN + 1):
		PH = ripser(family(size), maxDim, distance_matrix = True)['dgms']
		for dim in range(maxDim + 1):
			PHDict[dim][size]=PH[dim]*edgeScale(size)
	return PHDict
	# for each element of the family, compute its PH, and then scale by the appropriate amount
def stabilized(family, dim, edgeScale, precision = 0.05, consecWithinPrecision = 4, minN = 3, tries = 12, printUpdates = False):
	# Gives us a PH that's within precision of the previous consecWithinPrecision values
	# this method could give us a problem if, say, there was a pattern based on powers of two, but it's a good start
	# might have a problem with infinity
	startingValToTry = minN + consecWithinPrecision
	for i in range(tries):
		if printUpdates:
			print('trying ' + str(2**i * startingValToTry))
		PHs = persOfFamily(family, dim, edgeScale, 2**i * startingValToTry, 2**i * startingValToTry - consecWithinPrecision)[dim]
		closeEnough = True
		for j in range(2**i * startingValToTry - consecWithinPrecision, 2**i * startingValToTry):
			if PHs[j].shape != PHs[2**i * startingValToTry].shape or np.max(np.abs(PHs[j] - PHs[2**i * startingValToTry]), initial = 0) > precision:
				closeEnough = False
		if closeEnough: return PHs[2**i * startingValToTry]
#print(persOfFamily(cycleMatrix, 1, lambda n : 2*pi/n, 60))
#print(stabilized(cycleMatrix, 2, lambda n : 2*pi/n, printUpdates = True))
P = Counter(persOfFamily(lambda n : cyclePower(n,2), 2, lambda n : 2 * pi / n, 25)[2])
for i in range(3, 26):
	print(i)
	print(predictedPersistentOfProduct([i,i], 2))
	print(P[i])
