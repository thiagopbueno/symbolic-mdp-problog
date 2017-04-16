from literal import Literal


class WeightedDNF():

    def __init__(self, atoms):
        self._atoms = atoms
        self._terms = []
        self._weights = {}
        self.__index = {}
        for atom in self._atoms:
            self.__index[Literal.positive(atom)] = set()
            self.__index[Literal.negative(atom)] = set()

    def __repr__(self):
        wdnf_repr = ''
        for term in self._terms:
            wdnf_repr += str(term) + '\n'
        return wdnf_repr

    def __len__(self):
        return len(self._terms)

    def __getitem__(self, index):
        return self._terms[index]

    @property
    def atoms(self):
        return self._atoms

    @property
    def terms(self):
        return self._terms

    def add_term(self, term, weight):
        self.__update_index(term, len(self))
        self._terms.append((weight, term))
        self._weights[weight] = self._weights.get(weight, [])
        self._weights[weight].append(term)

    def terms_by_weight(self, weight):
        return self._weights.get(weight, [])

    def terms_by_literals(self, literals):
        if len(literals) == 0:
            return self._terms
        all_terms_indexes = set(range(0, len(self._terms)))
        consistent_list = []
        for l in literals:
            consistent_list.append(self.__index.get(l, all_terms_indexes))
        consistent_list = sorted(consistent_list, key=len)
        intersect = consistent_list[0]
        for term_set in consistent_list[1:]:
            intersect &= term_set
        return [ self[index] for index in sorted(intersect) ]

    def __update_index(self, term, index):
        term = set(term)
        for atom in self._atoms:
            positive_literal = Literal.positive(atom)
            negative_literal = Literal.negative(atom)
            if positive_literal in term:
                self.__index[positive_literal].add(index)
                continue
            if negative_literal in term:
                self.__index[negative_literal].add(index)
                continue
            self.__index[positive_literal].add(index)
            self.__index[negative_literal].add(index)
