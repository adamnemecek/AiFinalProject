import utils as util
from itertools import chain


def mtpHashTable(D, V):
    results = dict()
    for (vector, idx) in V:
        if vector in results.keys():
            results[vector].append(D[idx])
        else:
            results[vector] = [D[idx]]

    return results


def equivClassHashTable(M):
    results = dict()

    for vector, points in M.items():
        if len(points) == 1:
            continue

        patHash = list()
        for i in range(len(points) - 1):
            patHash.append(util.vectorSubtraction(points[i], points[i+1]))

        if patHash not in results.keys():
            results[patHash] = (points[0], {(0, 0): 1, vector: 1})
        else:
            if results[patHash][0] == points[0]:
                results[patHash][1][vector] = 1
            elif util.vectorAddition(points[0], vector) == results[patHash][0]:
                newVector = tuple(- el for el in vector)
                results[patHash][1][newVector] = 1
            else:
                pointDiff = util.vectorSubtraction(points[0], results[patHash][0])
                invertedPointDiff = tuple(- p for p in pointDiff)
                newVector = util.vectorAddition(invertedPointDiff, vector)
                results[patHash][1][newVector] = 1

    output = dict()
    for patHash, (firstPoint, transDict) in results.items():
        output[patHash] = list(transDict.keys())

    return output


def hashTEC(D):
    Vtable = util.compute_vector_table(D)
    V = list(chain.from_iterable(Vtable))
    mHash = mtpHashTable(D, V)
    TECs = equivClassHashTable(mHash)
    return TECs
