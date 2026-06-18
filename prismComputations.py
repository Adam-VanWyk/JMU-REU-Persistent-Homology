from functools import reduce
import numpy as np
def cycleDist(i,j,n): return min((i-j)%n,(j-i)%n) # Distance between points i and j in a cycle of size n
def cycleMatrix(n): return np.array([[cycleDist(i,j,n) for i in range(n)] for j in range(n)]) # Distance matrix for the cycle graph of size n
def prism(M): return np.block([[M,M+1],[M+1,M]]) # Applies the prism operator we defined to a distance matrix (in other words, take the product of that metric space with the interval matric space using the sum metric
def plot(n): return ripser(prism(cycleMatrix(n)), distance_matrix=True)['dgms'] # gives a plot of the persistent homology of the P(C_n); this doesn't show multiplicity so it's probably not what we want
def saveCSV(M, name="out.csv"): np.savetxt(name, M, delimiter=",") #saves an adjacency matrix as a CSV
def product(M, N): # computes the distance matrix of the product of two matrix spaces using the sum metric
	return np.block([[M + n for n in column] for column in N])
def maxProduct(M, N): # computes the distance matrix using the max matric rather than the sum metric
	return np.block([[np.maximum(M,n)  for n in column] for column in N])
def minProduct(M, N): # computes the distance matrix using the min distance (which notably isn't a metric rather than the sum metric
	return np.block([[np.minimum(M,n)  for n in column] for column in N])
def cyclePower(n,k): return reduce(product, [cycleMatrix(n) for _ in range(k)] )#returns C_n^k
if __name__ == "__main__":
	cycleList = []
	newVal = None
	while newVal != 'q':
		newVal = input("Type a cycle size that you'd like to include in your product, or q to be done. ")
		if newVal != 'q':
			cycleList.append(int(newVal))
	metricToUseInput = input("Type max if you'd like to use the maximum metric, min if you'd like to use the min metric, and anything else if you'd like to use the sum metric. ").strip()
	match metricToUseInput:
		case "min":
			metricToUse = minProduct
		case "max":
			metricToUse = maxProduct
		case _:
			metricToUse = product
	filename = input("What filename do you want? (If you don't enter one, it'll default to out.csv) ").strip() or "out.csv"
	saveCSV(reduce(metricToUse, map(cycleMatrix, cycleList)), name=filename)
