from analysis.siatec.tec import Tec, make_contiguous_TEC
import analysis.siatec.dataset_utils as utils
from math import ceil
import sys
from tqdm import tqdm


# =============================================================================
# CORE SIATEC
# =============================================================================
def compute_vector_table(D):
    V = list()
    W = list()
    for i, start in enumerate(D):
        vec_list = list()
        for j, end in enumerate(D):
            res = (utils.data_diff(start, end), i)
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
            Q.append(utils.data_diff(strt_pt, end_pt))
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
        # print("{}\n{}\n\n".format(pat_set, trans_set))
        T.append(Tec(p=pat_set, v=trans_set))

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
    D.sort()
    V, W = compute_vector_table(D)
    Y = compute_vector_representations(D, V)
    T = compute_TEC_set(D, V, W, Y)
    T_corrected = contiguous_wildcard_splitting(D, T)
    return T_corrected


def simple_siatec(D):
    tecs = siatec(D)
    filtered_tecs = utils.get_top_tecs(tecs, D)
    patterns = [[p for _, p in tec.pattern] for tec in filtered_tecs]
    print(patterns)
    return [[p - patt[0] for p in patt] for patt in patterns]


def retrograde_siatec(D):
    # Prep offset tracking
    retro_offset = float(ceil(D[-1][0]) + 1)
    first_point = (retro_offset, D[-1][1])
    r2o = {first_point: D[-1]}
    offset_pts = [first_point]

    # Make offset datapoints and associate with original points
    for i in range(len(D) - 1, 0, -1):
        new_offset = offset_pts[-1][0] + (D[i][0] - D[i-1][0])
        nxt_point = (new_offset, D[i-1][1])
        offset_pts.append(nxt_point)
        r2o[nxt_point] = D[i-1]

    # Make extended dataset
    rD = sorted(D + offset_pts)

    # Compute SIATEC sets
    V, W = compute_retro_vector_table(D, rD)
    Y = compute_retro_vector_representations(rD, V, r2o, retro_offset)
    T = compute_retro_TEC_set(rD, V, W, Y, retro_offset, r2o)

    rT = []
    for tec in T:
        new_tec = Tec(p=tec.pattern, v=[])
        bad_tec = False
        for vector in tec.vectors:
            points = sorted(tec.get_norm_vector_set(vector))
            x_min, x_max = points[0][0], points[-1][0]
            if x_min < retro_offset and x_max >= retro_offset:
                bad_tec = True
            elif x_min >= retro_offset:
                x_val = r2o[points[-1]][0] - tec.pattern[0][0]
                y_val = points[-1][1] - tec.pattern[-1][1]
                new_tec.retro_vectors.append((x_val, y_val))
            else:
                new_tec.vectors.append(vector)

        if not bad_tec:
            duplicate = False
            new_tec_data_vectors = set(new_tec.get_all_vector_sets())
            for cur_tec in rT:
                cur_tec_data_vectors = set(cur_tec.get_all_vector_sets())
                if new_tec_data_vectors == cur_tec_data_vectors:
                    duplicate = True
                    break
            if not duplicate:
                rT.append(new_tec)

    print("Total original TECs: {}\nTotal correct/unique TECs: {}".format(len(T), len(rT)))
    return rT


def retro_inverse_siatec(D):
    max_line = float(ceil(max(D, key=lambda pt: pt[1])[1]) + 1)
    offset_line = float(ceil(max(D, key=lambda pt: pt[0])[0]) + 1)

    x_val = offset_line + (offset_line - D[-1][0])
    y_val = max_line + (max_line - D[-1][1])
    new_pts = [(x_val, y_val)]
    for (x_cur, y_cur), (x_prv, y_prv) in zip(reversed(D[1:]), reversed(D[:-1])):
        x_val += (x_cur - x_prv)
        y_val += (y_cur - y_prv)
        new_pts.append((x_val, y_val))

    ri2o = {ret_inv: orig for ret_inv, orig in zip(new_pts, reversed(D))}
    riD = sorted(D + new_pts)

    # Compute SIATEC sets
    V, W = compute_retro_vector_table(D, riD)
    Y = compute_retro_vector_representations(riD, V, ri2o, offset_line)
    T = compute_retro_TEC_set(riD, V, W, Y, offset_line, ri2o)

    riT = []
    for tec in T:
        new_tec = Tec(p=tec.pattern, v=[])
        bad_tec = False
        for vector in tec.vectors:
            points = sorted(tec.get_norm_vector_set(vector))
            x_min, x_max = points[0][0], points[-1][0]
            if x_min < offset_line and x_max >= offset_line:
                bad_tec = True
            elif x_min >= offset_line:
                anchor_pt = ri2o[points[-1]]
                new_tec.ret_inv_vectors.append(anchor_pt)
            else:
                new_tec.vectors.append(vector)

        if not bad_tec:
            duplicate = False
            new_tec_data_vectors = set(new_tec.get_all_vector_sets())
            for cur_tec in riT:
                cur_tec_data_vectors = set(cur_tec.get_all_vector_sets())
                if new_tec_data_vectors == cur_tec_data_vectors:
                    duplicate = True
                    break
            if not duplicate:
                riT.append(new_tec)

    return riT


def inverse_siatec(D):
    max_line = float(ceil(max(D, key=lambda pt: pt[1])[1]) + 1)
    offset = float(ceil(max(D, key=lambda pt: pt[0])[0]) + 1)
    append_pts = [(x + offset, max_line - y) for (x, y) in D]
    i2o = {append_pts[i]: D[i] for i in range(len(D))}
    iD = sorted(D + append_pts)

    V, W = compute_retro_vector_table(D, iD)
    Y = compute_vector_representations(iD, V)
    print("finished making vector sets")
    T = compute_TEC_set(iD, V, W, Y)
    print("finished making TEC sets")
    iT = []

    print(len(T))
    for tec in T:
        new_tec = Tec(p=tec.pattern, v=[])
        bad_tec = False
        for vector in tec.vectors:
            points = sorted(tec.get_norm_vector_set(vector))
            x_min, x_max = points[0][0], points[-1][0]
            if x_min < offset and x_max >= offset:
                bad_tec = True
            elif x_min >= offset:
                anchor_pt = i2o[points[0]]
                new_tec.inverse_vectors.append(anchor_pt)
            else:
                new_tec.vectors.append(vector)

        if not bad_tec:
            duplicate = False
            new_tec_data_vectors = set(new_tec.get_all_vector_sets())
            for cur_tec in iT:
                cur_tec_data_vectors = set(cur_tec.get_all_vector_sets())
                if new_tec_data_vectors == cur_tec_data_vectors:
                    duplicate = True
                    break
            if not duplicate:
                iT.append(new_tec)

    print("Total original TECs: {}\nTotal correct/unique TECs: {}".format(len(T), len(iT)))
    split_iT_TECs = list()
    return iT
    # for tec in iT:
    #     split_iT_TECs.extend(make_contiguous_TEC(tec, D))
    #
    # return split_iT_TECs
# =============================================================================


# =============================================================================
# Wildcard splitting
# =============================================================================
def contiguous_wildcard_splitting(D, T):
    split_TECs = list()
    for tec in T:
        new_tecs = make_contiguous_TEC(tec, D)

        for t1 in new_tecs:
            add_tec = True
            cur_set = set(t1.get_all_vector_sets())
            for t2 in split_TECs:   # TODO: should be both T and split_TECs
                comp_set = set(t2.get_all_vector_sets())
                if cur_set <= comp_set:
                    add_tec = False
                    break
            if add_tec:
                split_TECs.append(t1)

    pattern_hashes = dict()
    for tec in split_TECs:
        pat_hash = tec.pattern_hash()
        if pat_hash in list(pattern_hashes.keys()):
            pattern_hashes[pat_hash].append(tec)
        else:
            pattern_hashes[pat_hash] = [tec]

    combined_TECs = list()
    for tecs in pattern_hashes.values():
        if len(tecs) > 1:
            new_tec = tecs[0]
            first_point = new_tec.pattern[0]
            for tec in tecs[1:]:
                for vector in tec.vectors:
                    vec_set = tec.get_norm_vector_set(vector)
                    translator = utils.data_diff(first_point, vec_set[0])
                    new_tec.vectors.append(translator)
            new_tec.vectors = list(set(new_tec.vectors))
            combined_TECs.append(new_tec)
        else:
            combined_TECs.extend(tecs)
    # print("Length of original TEC set {}\nLength split set {}\nLength comb set {}"
    #       .format(len(T), len(split_TECs), len(combined_TECs)))

    return combined_TECs
# =============================================================================


def vec_inverse_equivalence(v1, v2):
    """
    Assumes positive X corrdinate values
    TODO: Consider if this needs to be changed for the general case
    NOTE: Checks 2nd value inverse
    """
    return (v1[0] + v2[0] == 0) and (v2[1] - v1[1] == 0)


def compute_retro_vector_table(D, rD):
    V = list()
    W = list()
    for i, start in enumerate(D):
        vec_list = list()
        for j, end in enumerate(rD):
            # res = (utils.data_diff(start, end), i)
            res = (utils.data_diff(start, end), i)
            vec_list.append(res)
            if j > i:
                V.append(res)
        W.append(vec_list)
    return sorted(V), W


def compute_retro_vector_representations(D, V, conv_dict, max_len):
    X, i = list(), 0
    num_vectors = len(V)

    while i < num_vectors:
        Q = list()
        visited = list()
        j = i + 1
        while j < num_vectors and V[j][0] == V[i][0]:
            included = True
            if V[i][0][0] >= max_len-1:
                # offset_datapoint = utils.data_sum(D[V[j-1][1]], V[i][0])
                offset_datapoint = utils.data_sum(D[V[j-1][1]], V[i][0])
                related_val = conv_dict[offset_datapoint]
                if related_val not in visited:
                    visited.append(related_val)
                if D[V[j][1]] in visited:
                    included = False
            if included:
                strt_pt = D[V[j-1][1]]
                end_pt = D[V[j][1]]
                Q.append(utils.data_diff(strt_pt, end_pt))
            j += 1
        X.append((i, Q))
        i = j
    # print(X)
    return sorted(X, key=lambda vec_set: (len(vec_set[1]), vec_set[1], vec_set[0]))


def compute_retro_TEC_set(D, V, W, Y, max_len, conv_dict):
    T, i = list(), 0
    num_vector_sets = len(Y)
    num_vectors = len(V)

    while i < num_vector_sets:
        j = Y[i][0]
        I = list()
        visited = list()
        while j < num_vectors and V[j][0] == V[Y[i][0]][0]:
            included = True
            if V[Y[i][0]][0][0] >= max_len-1:
                offset_datapoint = utils.data_sum(D[V[j][1]], V[Y[i][0]][0])
                related_val = conv_dict[offset_datapoint]
                if related_val not in visited:
                    visited.append(related_val)
                if D[V[j][1]] in visited:
                    included = False

            if included:
                I.append(V[j][1])
            j += 1
        pat_set = [D[index] for index in I]
        trans_set = compute_TEC_translators(D, W, I)
        T.append(Tec(p=pat_set, v=trans_set))

        while True:
            i += 1
            if i >= num_vector_sets or Y[i][1] != Y[i-1][1]:
                break

    return T
