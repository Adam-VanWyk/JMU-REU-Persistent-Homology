from functools import reduce
import numpy as np
def cycleDist(i,j,n): return min((i-j)%n,(j-i)%n) # Distance between points i and j in a cycle of size n
def cycleMatrix(n): return np.array([[cycleDist(i,j,n) for i in range(n)] for j in range(n)]) # Distance matrix for the cycle graph of size n
def prism(M): return np.block([[M,M+1],[M+1,M]]) # Applies the prism operator we defined to a distance matrix (in other words, take the product of that metric space with the interval matric space using the sum metric
def plot(n): return ripser(prism(cycleMatrix(n)), distance_matrix=True)['dgms'] # gives a plot of the persistent homology of the P(C_n); this doesn't show multiplicity so it's probably not what we want
def saveCSV(M, name="out.csv"): np.savetxt(name, M, delimiter=",") #saves an adjacency matrix as a CSV
def product(M, N): # computes the distance matrix of the product of two matrix spaces using the sum metric
	return np.block([[M + n for n in column] for column in N])
def cyclePower(n,k): return functools.reduce(product, [cycleMatrix(n) for _ in range(k)] )#returns C_n^k
saveCSV(product(cycleMatrix(7),cycleMatrix(8)))
