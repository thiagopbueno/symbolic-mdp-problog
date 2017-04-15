class Literal(object):

    def __init__(self, atom, positive):
        self._atom = atom
        self._positive = positive

    @classmethod
    def positive(cls, atom):
        return Literal(atom, True)

    @classmethod
    def negative(cls, atom):
        return Literal(atom, False)

    @property
    def atom(self):
        return self._atom

    def is_positive(self):
        return self._positive

    def is_negative(self):
        return not self._positive

    def __str__(self):
        if self._positive:
            literal_repr = str(self._atom)
        else:
            literal_repr = 'not ' + str(self._atom)
        return literal_repr

    def __repr__(self):
        if self._positive:
            literal_repr = ('+', self._atom)
        else:
            literal_repr = ('-', self._atom)
        return str(literal_repr)

    def __hash__(self):
        return hash(repr(self))

    def __cmp__(self, other):
        if self < other:
            return -1
        if self == other:
            return 0
        return 1

    def __eq__(self, other):
        return self._positive == other._positive and \
            self._atom == other._atom

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if self._positive and not other._positive:
            return True
        if not self._positive and other._positive:
            return False
        return self._atom < other._atom

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other
