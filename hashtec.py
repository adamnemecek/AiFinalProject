

# Same vector table computation as SIATEC
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