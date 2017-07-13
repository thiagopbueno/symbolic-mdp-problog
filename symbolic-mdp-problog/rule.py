class Rule(object):

    def __init__(self, head, body=None, probability=None):
        self._head = head

        if body is None:
            self._body = tuple()
        else:
            self._body = tuple(body)

        if probability is None:
            self._probability = probability
        else:
            self._probability = float(probability)

    @property
    def head(self):
        return self._head

    @property
    def body(self):
        return self._body

    @property
    def probability(self):
        return self._probability

    def __repr__(self):
        rule_repr = ''

        if self._probability:
            rule_repr += str(self._probability) + '::'

        rule_repr += str(self._head)

        if len(self._body) > 0:
            body = [ str(l) for l in self._body ]
            rule_repr += ' :- ' + ', '.join(body) + '.'

        return rule_repr
