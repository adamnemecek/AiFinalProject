

def getTecSetRep(T):
    patternList = list()
    for pattern, translators in T:
        for translator in translators:
            newPattern = tuple([vectorAddition(p, translator) for p in pattern])
            patternList.append(newPattern)
    patternList.sort()
    return tuple(patternList)


def vectorAddition(V1, V2):
    return tuple(v1 + v2 for v1, v2 in zip(V1, V2))


def vectorSubtraction(V1, V2):
    return tuple(v2 - v1 for v1, v2 in zip(V1, V2))


def isEquivTecSets(T1, T2):
    return getTecSetRep(T1) == getTecSetRep(T2)
