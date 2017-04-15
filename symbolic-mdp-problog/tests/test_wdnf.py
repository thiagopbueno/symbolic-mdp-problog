import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))

import unittest
import parser
from literal import Literal
import wdnf


class TestWeightedDNF(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.parser = parser.Parser()

        filename1 = os.path.join(os.path.dirname(__file__), 'models/value.pl')
        with open(filename1, 'r') as input:
            cls.value = input.read()
        cls.atoms1, cls.rules1 = cls.parser.parse(cls.value)

        filename2 = os.path.join(os.path.dirname(__file__), 'models/transition.pl')
        with open(filename2, 'r') as input:
            cls.transition = input.read()
        cls.atoms2, cls.rules2 = cls.parser.parse(cls.transition)

    def test_add_term(self):
        # value function
        wdnf1 = wdnf.WeightedDNF(self.atoms1)
        self.assertEqual(len(wdnf1), 0)
        for index, rule in enumerate(self.rules1):
            wdnf1.add_term(rule.body, int(rule.head[2:-1]))
            self.assertEqual(len(wdnf1), index + 1)

        fluents = ['running(c1,1)', 'running(c2,1)', 'running(c3,1)']
        for fluent in fluents:
            pos = Literal.positive(fluent)
            neg = Literal.negative(fluent)
            t1 = set(wdnf1.terms_by_literals([pos]))
            t2 = set(wdnf1.terms_by_literals([neg]))
            self.assertEqual(len(t1), len(wdnf1) / 2)
            self.assertEqual(len(t2), len(wdnf1) / 2)
            self.assertEqual(t1 & t2, set())
            self.assertEqual(t1 | t2, set(wdnf1.terms))

        values = [0, 1, 2, 3]
        terms_sets = [ set(wdnf1.terms_by_weight(v)) for v in values ]
        self.assertEqual(sum([len(s) for s in terms_sets]), len(wdnf1))
        for i in range(len(terms_sets[-1])):
            for j in range(i + 1, len(terms_sets)):
                self.assertEqual(terms_sets[i] & terms_sets[j], set())

        # transition function
        wdnf2 = wdnf.WeightedDNF(self.atoms2)
        self.assertEqual(len(wdnf2), 0)
        for index, rule in enumerate(self.rules2):
            pos_term = tuple([Literal.positive(rule.head)] + list(rule.body))
            wdnf2.add_term(pos_term, rule.probability)
            neg_term = tuple([Literal.negative(rule.head)] + list(rule.body))
            wdnf2.add_term(neg_term, 1 - rule.probability)
        self.assertEqual(len(wdnf2), 2 * len(self.rules2))

        next_state_fluents = ['running(c1,1)', 'running(c2,1)', 'running(c3,1)']
        for fluent in next_state_fluents:
            pos = Literal.positive(fluent)
            neg = Literal.negative(fluent)
            t1 = set(wdnf2.terms_by_literals([pos]))
            t2 = set(wdnf2.terms_by_literals([neg]))
            self.assertEqual(len(t1), len(t2))

            inter = set(term for _, term in t1 & t2)
            self.assertTrue(pos not in inter)
            self.assertTrue(neg not in inter)

        actions = ['reboot(c1)', 'reboot(c2)', 'reboot(c3)']
        for action in actions:
            pos = Literal.positive(action)
            neg = Literal.negative(action)
            t1 = set(wdnf2.terms_by_literals([pos]))
            t2 = set(wdnf2.terms_by_literals([neg]))
            inter = set(term for _, term in t1 & t2)
            self.assertTrue(pos not in inter)
            self.assertTrue(neg not in inter)

            if action == actions[0]:
                self.assertEqual(len(t1), len(wdnf2) - 6)
                self.assertEqual(len(t2), len(wdnf2) - 2)

            if action == actions[2]:
                self.assertEqual(len(t1), len(wdnf2) - 6)
                self.assertEqual(len(t2), len(wdnf2) - 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
