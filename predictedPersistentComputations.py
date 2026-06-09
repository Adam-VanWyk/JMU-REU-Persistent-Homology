from collections import Counter
from functools import reduce
from math import floor, ceil
def PHCycle(n, k): # Gives the k-dimensional persistent homology of C_n
	if k == 0:
		return Counter({(0, 1) : n - 1, (0, float('inf')): 1})
	if k % 2 == 0:
		if n % (k + 1) == 0 and n != k + 1:
			return Counter({(int(k * n / (2 * (k + 1))), int(k * n / (2 * (k + 1)) + 1)) : int(n / (k + 1) - 1)})
		else:
			return Counter() 
	else:
		return Counter({(floor((k-1) / 2 * n / k) + 1, ceil((k + 1) / 2 * n / (k + 2))): 1})
def PHCycleAll(n):
	return lambda k : PHCycle(n, k)
def tensorOperation(i1, i2): # returns the tensor interval operation on two intervals
	return (i1[0] + i2[0], min(i1[0] + i2[1], i1[1] + i2[0]))
def torOperation(i1, i2):
	return (max(i1[0] + i2[1], i1[1] + i2[0]), i1[1] + i2[1])
def product(ph1, ph2, k): #ph1 and ph2 should be functions that take in K and give a Counter for PHk 
	# Calculate the tensor term
	ans = Counter()
	for i in range(k + 1): # this is the value of i that should add to j and give n
		j = k - i
		for key1, value1 in ph1(i).items():
			for key2, value2 in ph2(j).items():
				ans[tensorOperation(key1, key2)] += value1*value2	
	#tor term
	for i in range(k): # this is the value of i that should add to j and give n-1
		j = k - i - 1
		for key1, value1 in ph1(i).items():
			for key2, value2 in ph2(j).items():
				ans[torOperation(key1, key2)] += value1*value2	
	return ans
def productAll(ph1, ph2):
	return lambda k : product(ph1, ph2, k)
def stripEphemerals(counter):
	return {k: v for k, v in counter.items() if k[0] != k[1]}	
def predictedPersistentOfProduct(cycleSizeList, homologyDim):
	PHCycleFuncs = map(PHCycleAll, cycleSizeList)
	productFunc = reduce(productAll, PHCycleFuncs)
	return productFunc(homologyDim)
if __name__ == '__main__':
	cycleList = []
	newVal = None
	while newVal != 'q':
		newVal = input("Type a cycle size that you'd like to include in your product, or q to be done. ")
		if newVal != 'q':
			cycleList.append(int(newVal))
	dimMin = int(input('What minimum dimension would you like to take the persistent homology in? '))
	dimMax = int(input('What maximum dimension would you like to take the persistent homology in? '))
	for dim in range(dimMin, dimMax + 1):
		print("\nDimension "+str(dim)+":") 
		print("With ephemerals stripped, the persistent homology is: " + str(dict(sorted(stripEphemerals(predictedPersistentOfProduct(cycleList, dim)).items()))))
		print("Without ephemerals stripped, the persistent homology is: " + str(dict(sorted(dict(predictedPersistentOfProduct(cycleList, dim)).items()))))
