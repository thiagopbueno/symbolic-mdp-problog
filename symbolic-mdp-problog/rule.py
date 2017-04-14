class Rule(object):

    def __init__(self, head, body=[], probability=None):
        self._head = head
        self._body = body
        self._probability = probability

    def __repr__(self):
        rule_repr = ''

        if self._probability:
            rule_repr += str(self._probability) + '::'

        rule_repr += str(self._head)

        if len(self._body) > 0:
            body = []
            for literal in self._body:
                b = str(literal[1])
                if literal[0] == '-':
                    body.append('not ' + b)
                else:
                    body.append(b)
            rule_repr += ' :- ' + ', '.join(body) + '.'

        return rule_repr