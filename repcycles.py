# This is pretty messy; if you want to use it lmk and I can clean it up a bit
import numpy as np
import dionysus as d
import prismComputations as p
from itertools import combinations, product
from functools import reduce
import operator
def prod(list):
	return reduce(operator.mul, list, 1)
def convertIterCoordsToIterInt(coords, dims):
	return map(lambda tuple: sum([tuple[i]*prod(dims[:i]) for i in range(len(dims))]), coords)
def convertIntToCoord(intToConvert, dims):
	coords = []
	for dim in dims:
		coords.append(intToConvert % dim)
		intToConvert //= dim
	return tuple(coords)
def diam(n, coords): #given an iterable of integers, this returns the diameter of it in C_n
	return max([p.cycleDist(a,b,n) for a,b in combinations(coords,2)], default=0)
def proj(iterable, index): #gives a generator which gives the projections of the elements of iterable onto the index axis
	return (element[index] for element in iterable)
def predictedDiam(dims, coords): #returns the "diameter" of a set in the predicted situation
	return sum([diam(dims[index],proj(coords,index)) for index in range(len(dims))])
def predictedFiltration(n,m):
	f = d.Filtration()
	for dim in range(4): #We only care about the simplices up to dimension 3 in order to compute the 2-homology
		for simplex in combinations(product(range(n),range(m)),dim+1):
			#print(simplex, predictedDiam([n, m], simplex))
			f.append(d.Simplex(convertIterCoordsToIterInt(simplex, [n,m]),predictedDiam([n,m], simplex)))
	return f
def drawSimplex(simplex, n, m): #takes a simplex as an iterable of vertices and draws it
	for j in range(m):
		print(''.join(["#" if (i,j) in simplex else "." for i in range(n)]))
a = int(input("What is the first cycle graph dimension you want?"))
b = int(input("What is the second cycle graph dimension you want?"))
f=predictedFiltration(a,b)
f.sort()
"""m = d.homology_persistence(f, prime=2)
dgms = d.init_diagrams(m, f)
for i, dgm in enumerate(dgms):
    #print("Dimension:", i)
    for p in dgm:
        #print(p)"""
m = d.homology_persistence(f, prime=2)
dgms = d.init_diagrams(m,f)

dim = 2     # dimension of the diagram we want
for pt in dgms[dim]:
	print("----------------------------------------------------------------")
	print(pt)
	x = m.pair(pt.data)
	for sei in m[x]:
	    s = f[sei.index]    # simplex
	    vertices = [convertIntToCoord(x, [a,b]) for x in s]
	    #print('#',s)
	    #print(vertices)
	    drawSimplex(vertices, a, b)
	    print()
