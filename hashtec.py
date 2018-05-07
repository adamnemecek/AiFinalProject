import utils as util
# from itertools import chain, combinations


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


        # pointSets = powerset(points)
        #
        # for pointSet in pointSets:
        #     if len(pointSet) > 1:
        #         curDict = results
        #         for i in range(len(pointSet) - 1):
        #             patPart = util.vectorSubtraction(pointSet[i], pointSet[i+1])
        #             if patPart not in curDict.keys():
        #                 curDict[patPart] = {None: (pointSet[0], {(0, 0): 1, vector: 1})}
        #             else:
        #                 if curDict[patPart][None][0] == pointSet[0]:
        #                     curDict[patPart][None][1][vector] = 1
        #                 elif util.vectorAddition(pointSet[0], vector) == curDict[patPart][None][0]:
        #                     newVector = tuple(- el for el in vector)
        #                     curDict[patPart][None][1][newVector] = 1
        #                 else:
        #                     pointDiff = util.vectorSubtraction(curDict[patPart][None][0], pointSet[0])
        #                     newVector = util.vectorAddition(pointDiff, vector)
        #                     curDict[patPart][None][1][pointDiff] = 1
        #                     curDict[patPart][None][1][newVector] = 1
        #             curDict = curDict[patPart]

    # output = dict()
    # for patPart, topLevelDict in results.items():
    #     firstPoint = topLevelDict[None][0]
    #     curPattern = [firstPoint, util.vectorAddition(firstPoint, patPart)]
    #     (treeMax, newTecs) = buildTECset(0, curPattern, {}, topLevelDict)
    #     output.update(newTecs)
    #
    # return output


# def buildTECset(curMax, curPattern, tecs, curDict):
    # if len(curDict.keys()) == 1:
    #     translators = list(curDict[None][1].keys())
    #     return len(translators), {tuple(curPattern): translators}
    #
    # iterMax = curMax
    # for nextPat, newDict in curDict.items():
    #     if nextPat is not None:
    #         newPat = curPattern + [util.vectorAddition(curPattern[-1], nextPat)]
    #         (newMax, newTecs) = buildTECset(curMax, newPat, tecs, newDict)
    #         tecs.update(newTecs)
    #         iterMax = max(iterMax, newMax)
    #
    # translators = list(curDict[None][1].keys())
    # if len(translators) > iterMax:
    #     tecs.update({tuple(curPattern): translators})
    #     return len(translators), tecs
    # return iterMax, tecs


# def powerset(iterable):
#     "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
#     s = list(iterable)
#     return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def hashTEC(D):
    V = compute_vector_table(D)
    # print("V done")
    mHash = mtpHashTable(D, V)
    # print("mHash done")
    TECs = equivClassHashTable(mHash)
    # print("TECs done")
    return TECs
