from collections import Counter
from math import floor, ceil
def PHCycle(n, k): # Gives the k-dimensional persistent homology of C_n
	if k == 0:
		return Counter({(0, 1) : n - 1, (0, float('inf')): 1})
	if k % 2 == 0:
		if n % (k + 1) == 0:
			return Counter({(k * n / (2 * (k + 1)), k * n / (2 * (k + 1)) + 1) : n / (k + 1) - 1})
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
	return lambda k : PHCycle(n, k)
def stripEphemerals(counter):
	for key, val in counter.items():
		if val[0]==val[1]:
			del counter[key]
print(PHCycle(8, 1))
print(product(PHCycleAll(7),PHCycleAll(4),1))
print(product(PHCycleAll(7),PHCycleAll(8),1))
