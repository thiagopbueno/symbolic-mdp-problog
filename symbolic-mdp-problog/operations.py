from wdnf import WeightedDNF


def combine(wdnf1, wdnf2, op):
    wdnf = WeightedDNF(wdnf1.atoms | wdnf2.atoms)
    for wterm1 in wdnf1:
        weight1, literals1 = wterm1
        for wterm2 in wdnf2.terms_by_literals(literals1):
            w, t = combine_step(wterm1, wterm2, op)
            wdnf.add_term(t, w)
    return wdnf


def combine_step(wterm1, wterm2, op):
    val1, term1 = wterm1
    val2, term2 = wterm2
    return (op(val1, val2), join(term1, term2))


def join(term1, term2):
    if len(term1) == 0 and len(term2) == 0:
        return []
    if len(term1) == 0:
        return term2
    if len(term2) == 0:
        return term1

    term = []
    i = 0
    j = 0
    while True:
        l1 = term1[i]
        l2 = term2[j]
        if l1 == l2:
            term.append(l1)
            i += 1
            j += 1
        elif l1 < l2:
            term.append(l1)
            i += 1
        elif l2 < l1:
            term.append(l2)
            j += 1

        if i == len(term1):
            term += term2[j:]
            break
        if j == len(term2):
            term += term1[i:]
            break

    return term
