

def vectorAddition(V1, V2):
    return tuple(v1 + v2 for v1, v2 in zip(V1, V2))


def vectorSubtraction(V1, V2):
    return tuple(v1 - v2 for v1, v2 in zip(V1, V2))


# Vector table computation for SIATEC and HashTEC
def compute_vector_table(D):
    V = list()
    W = list()
    for i, start in enumerate(D):
        vec_list = list()
        for j, end in enumerate(D):
            diff = tuple([e - s for s, e in zip(start, end)])
            res = (diff, i)
            vec_list.append(res)
            if j > i:
                V.append(res)
        W.append(vec_list)
    return sorted(V), W
