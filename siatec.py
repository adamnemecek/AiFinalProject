

# =============================================================================
# CORE SIATEC
# =============================================================================
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


def compute_vector_representations(D, V):
    X, i = list(), 0
    num_vectors = len(V)
    while i < num_vectors:
        Q = list()
        j = i + 1
        while j < num_vectors and V[j][0] == V[i][0]:
            strt_pt = D[V[j-1][1]]
            end_pt = D[V[j][1]]
            diff = tuple([e - s for s, e in zip(strt_pt, end_pt)])
            Q.append(diff)
            j += 1
        X.append((i, Q))
        i = j

    return sorted(X, key=lambda v_set: (len(v_set[1]), v_set[1], v_set[0]))


def compute_TEC_set(D, V, W, Y):
    T, i = list(), 0
    num_vector_sets = len(Y)
    num_vectors = len(V)

    while i < num_vector_sets:
        j = Y[i][0]
        I = list()
        while j < num_vectors and V[j][0] == V[Y[i][0]][0]:
            I.append(V[j][1])
            j += 1
        pat_set = [D[index] for index in I]
        trans_set = compute_TEC_translators(D, W, I)
        T.append((pat_set, trans_set))

        while True:
            i += 1
            if i >= num_vector_sets or Y[i][1] != Y[i-1][1]:
                break

    return T


def compute_TEC_translators(D, W, I):
    num_points = len(D)
    num_indicies = len(I)

    if num_indicies == 1:
        return [W[I[0]][ind][0] for ind in range(num_points)]

    results = list()
    J = [0 for i in range(num_indicies)]
    fin = False
    k = 1
    while not fin:
        if J[k] <= J[k-1]:
            J[k] = J[k-1] + 1
        while J[k] <= num_points - num_indicies + k and \
                W[I[k]][J[k]][0] < W[I[k-1]][J[k-1]][0]:
            J[k] += 1
        if J[k] > num_points - num_indicies + k:
            fin = True
        elif W[I[k]][J[k]][0] > W[I[k-1]][J[k-1]][0]:
            k = 1
            J[0] += 1
            if J[0] > num_points - num_indicies + 1:
                fin = True
        elif (k+1) == num_indicies:
            results.append(W[I[k]][J[k]][0])
            k = 0
            while (k+1) <= num_indicies:
                J[k] += 1
                if J[k] > num_points - num_indicies + k:
                    fin = True
                    k = num_indicies
                k += 1
            k = 1
        else:
            k += 1
    return results
# =============================================================================


# =============================================================================
# Top-level routines
# =============================================================================
def siatec(D):
    V, W = compute_vector_table(D)
    Y = compute_vector_representations(D, V)
    T = compute_TEC_set(D, V, W, Y)
    return T
