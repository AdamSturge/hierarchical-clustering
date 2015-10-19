#from scipy.stats.stats import pearsonr
import math 

def readfile(filename) :
	lines=[line for line in file(filename)]
	
	colnames = lines[0].strip().split('\t')[1:]
	rownames = []
	data = []
	for line in lines[1:]:
		p = line.strip().split('\t')
		rownames.append(p[0])
		data.append([float(x) for x in p[1:]])
	return rownames,colnames,data
	


def average(x):
	assert len(x) > 0
	return float(sum(x)) / len(x)

def pearson(x, y):
	assert len(x) == len(y)
	n = len(x)
	assert n > 0
	avg_x = average(x)
	avg_y = average(y)
	diffprod = 0
	xdiff2 = 0
	ydiff2 = 0
	for idx in range(n):
		xdiff = x[idx] - avg_x
		ydiff = y[idx] - avg_y
		diffprod += xdiff * ydiff
		xdiff2 += xdiff * xdiff
		ydiff2 += ydiff * ydiff

	
	denom = math.sqrt(xdiff2 * ydiff2)
	assert denom != 0
	return 1.0 - (diffprod / denom)
	

print(pearson([2,2,1], [1,2,1]))