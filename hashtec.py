import utils as util


def compute_vector_table(D):
    V = list()
    for i, start in enumerate(D[:-1]):
        for j, end in enumerate(D[i+1:]):
            V.append((util.vectorSubtraction(start, end), i))
    return V


def mtpHashTable(D, V):
    results = dict()
    for vector, idx in V:
        if vector in results:
            results[vector].append(D[idx])
        else:
            results[vector] = [D[idx]]
    return results


def equivClassHashTable(M):
    results = dict()

    for vector, points in M.items():
        if len(points) > 1:
            MaxVecShift = [(0, 0)]
            for idx in range(1, len(points)):
                diff = util.vectorSubtraction(points[idx-1], points[idx])
                MaxVecShift.append(util.vectorAddition(MaxVecShift[-1], diff))
            results[tuple(MaxVecShift)] = 0

    return list(results.keys())


def hashTEC(D):
    V = compute_vector_table(D)
    mHash = mtpHashTable(D, V)
    pTypes = equivClassHashTable(mHash)
    return pTypes
