import numpy as np

# minSize = the smallest set that will be generated
# maxSize = the largest set that can be generated
# step = the number of samples to add between sets
# density = points per unit of area
# yRange = max height of y values
# returns a List of Lists containing tuples representing points
# max height of points is 12, min is 0

def randomSampleSetsLinear(minSize, maxSize, step, density, yRange=12):
	
	result = []
	numSteps = (maxSize - minSize) / step

	for i in range(numSteps+1):

		numPoints = minSize + (step * i)
		xRange = (int) (numPoints / (yRange * density))
		print "XRANGE = " + str(xRange)

		matrix = [(x,y) for x in range(xRange) for y in range(yRange)]
		ind = np.random.choice(len(matrix), numPoints, replace=False)

		outputList = []
		for j in ind:
			outputList.append(matrix[j])
			
		result.append(outputList)

	return result


"""
def main():
    test = randomSampleSetsLinear(10, 20, 10, 0.1)
    print(str(test))

if __name__== "__main__":
	main()
"""




