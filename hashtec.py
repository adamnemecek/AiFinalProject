import utils as util


def compute_vector_table(D):
    V = list()
    for i, start in enumerate(D[:-1]):
        for end in D[i+1:]:
            V.append((util.vectorSubtraction(start, end), i))
    return V


def mtpHashTable(D, V):
    results = dict()
    for vector, idx in V:
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
        patHash = tuple(patHash)

        if patHash not in results.keys():
            results[patHash] = (points[0], {(0, 0): 1, vector: 1})
        else:
            if results[patHash][0] == points[0]:
                results[patHash][1][vector] = 1
            elif util.vectorAddition(points[0], vector) == results[patHash][0]:
                newVector = tuple(- el for el in vector)
                results[patHash][1][newVector] = 1
            else:
                pointDiff = util.vectorSubtraction(results[patHash][0], points[0])
                # invertedPointDiff = tuple(- p for p in pointDiff)
                newVector = util.vectorAddition(pointDiff, vector)
                results[patHash][1][newVector] = 1

    output = dict()
    for patHash, (firstPoint, transDict) in results.items():
        pattern = [firstPoint]
        for tup in patHash:
            pattern.append(util.vectorAddition(pattern[-1], tup))
        output[tuple(pattern)] = list(transDict.keys())

    return output


def hashTEC(D):
    V = compute_vector_table(D)
    mHash = mtpHashTable(D, V)
    TECs = equivClassHashTable(mHash)
    return TECs
