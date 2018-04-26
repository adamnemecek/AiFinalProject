from music_management.music_utils import MusicElement


def getTecSetRep(T):
    patternList = list()
    for pattern, translators in T:
        for translator in translators:
            newPattern = tuple([vectorAddition(p, translator) for p in pattern])
            patternList.append(newPattern)
    patternList.sort()
    return tuple(patternList)


def pitch_dataset(score):
    return sorted([(sum(o), p) for (t, p, _, o) in score if t == MusicElement.NOTE])


def vectorAddition(V1, V2):
    return tuple(v1 + v2 for v1, v2 in zip(V1, V2))


def vectorSubtraction(V1, V2):
    return tuple(v2 - v1 for v1, v2 in zip(V1, V2))


def isEquivTecSets(T1, T2, D):
    # sets1 = getTecSetRep(T1)
    # sets2 = getTecSetRep(T2)

    # sortedSets1 = sorted(sets1, key=lambda tup: len(tup))
    # sortedSets2 = sorted(sets2, key=lambda tup: len(tup))

    # inBoth = 0
    # in1 = 0
    # in2 = 0
    # in1NotData = 0
    # in2NotData = 0
    # lengthsMissed = list()
    # for pattern in sets1:
    #     if pattern not in sets2:
    #         in1 += 1
    #         if not (set(pattern) <= set(D)):
    #             in1NotData += 1
    #         lengthsMissed.append(len(pattern))
    #         # print("Found pattern in set 1 and not in set 2: {}".format(pattern))
    #     else:
    #         inBoth += 1
    #
    # for pattern in sets2:
    #     if pattern not in sets1:
    #         in2 += 1
    #         if not (set(pattern) <= set(D)):
    #             in2NotData += 1
    #         # print("Found pattern in set 2 and not in set 1: {}".format(pattern))
    # print("{} patterns were found by both\n{} patterns were found only by method 1\n{} were found only by method 2".format(inBoth, in1, in2))
    # print("{} patterns found in 1 not in 2 are not in D\n{} patterns found in 2 not in 1 are not in D".format(in1NotData, in2NotData))
    # print("Lengths of missed patterns from 1: {}".format(list(set(lengthsMissed))))
    return getTecSetRep(T1) == getTecSetRep(T2)
