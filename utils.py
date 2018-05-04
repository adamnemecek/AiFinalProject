from music_management.music_utils import MusicElement
import numpy as np


def getTecSetRep(T):
    patternList = list()
    for pattern, translators in T:
        for translator in translators:
            newPattern = tuple([vectorAddition(p, translator) for p in pattern])
            patternList.append(newPattern)
    patternList.sort()
    return tuple(patternList)


def randomSampleSetsLinear(minSize, maxSize, step, density, yRange=12):
    """
    minSize = the smallest set that will be generated
    maxSize = the largest set that can be generated
    step = the number of samples to add between sets
    density = points per unit of area
    yRange = max height of y values
    returns a List of Lists containing tuples representing points
    max height of points is 12, min is 0
    """
    result = []
    numSteps = int((maxSize - minSize) / step)

    for i in range(numSteps+1):

        numPoints = minSize + (step * i)
        xRange = int(numPoints / (yRange * density))
        matrix = [(x, y) for x in range(xRange) for y in range(yRange)]
        ind = np.random.choice(len(matrix), numPoints, replace=False)

        outputList = []
        for j in ind:
            outputList.append(matrix[j])

        result.append(outputList)

    return result


def pitch_dataset(score):
    return sorted([(sum(o), p) for (t, p, _, o) in score if t == MusicElement.NOTE])


def vectorAddition(V1, V2):
    return tuple(v1 + v2 for v1, v2 in zip(V1, V2))


def vectorSubtraction(V1, V2):
    return tuple(v2 - v1 for v1, v2 in zip(V1, V2))


def diagnoseDiff(T1, T2, D):
    print("{} total TECs in 1\t{} total TECs in 2".format(len(T1), len(T2)))
    sets1 = getTecSetRep(T1)
    sets2 = getTecSetRep(T2)

    sets1 = sorted(sets1, key=lambda tup: len(tup))
    sets2 = sorted(sets2, key=lambda tup: len(tup))

    inBoth = 0
    in1 = 0
    in2 = 0
    in1NotData = 0
    in2NotData = 0
    lengthsMissed = list()
    for pattern in sets1:
        if pattern not in sets2:
            in1 += 1
            if not (set(pattern) <= set(D)):
                in1NotData += 1
            lengthsMissed.append(len(pattern))
            print("Pattern in 1 not 2: {}".format(pattern))
        else:
            inBoth += 1

    for pattern in sets2:
        if pattern not in sets1:
            in2 += 1
            if not (set(pattern) <= set(D)):
                in2NotData += 1
            print("Pattern in 2 not 1: {}".format(pattern))
    print("{} patterns were found by both\n{} patterns were found only by method 1\n{} were found only by method 2".format(inBoth, in1, in2))
    print("{} patterns found in 1 not in 2 are not in D\n{} patterns found in 2 not in 1 are not in D".format(in1NotData, in2NotData))
    print("Lengths of missed patterns from 1: {}".format(list(set(lengthsMissed))))


def isEquivTecSets(T1, T2):
    return getTecSetRep(T1) == getTecSetRep(T2)
