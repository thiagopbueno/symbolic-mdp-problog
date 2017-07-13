import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))

import unittest
from parser import Parser
from wdnf import WeightedDNF
from operations import join, combine_step, combine
from literal import Literal


class TestOperations(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.r1 = 'running(c1,1)'
        cls.r2 = 'running(c2,1)'
        cls.r3 = 'running(c3,1)'
        cls.lp1 = Literal.positive(cls.r1)
        cls.ln1 = Literal.negative(cls.r1)
        cls.lp2 = Literal.positive(cls.r2)
        cls.ln2 = Literal.negative(cls.r2)
        cls.lp3 = Literal.positive(cls.r3)
        cls.ln3 = Literal.negative(cls.r3)

    def test_join(self):
        t0 = []
        self.assertEqual(join(t0, t0), [])

        t1 = [self.lp1]
        self.assertEqual(join(t1, t0), t1)
        self.assertEqual(join(t0, t1), t1)
        self.assertEqual(join(t1, t1), t1)
        t2 = [self.ln1]
        self.assertEqual(join(t2, t0), t2)
        self.assertEqual(join(t0, t2), t2)
        self.assertEqual(join(t2, t2), t2)

        t3 = [self.lp1, self.lp2]
        self.assertEqual(join(t3, t0), t3)
        self.assertEqual(join(t0, t3), t3)
        self.assertEqual(join(t3, t1), t3)
        self.assertEqual(join(t1, t3), t3)

        t4 = [self.lp1, self.lp2]
        t5 = [self.lp3]
        self.assertEqual(join(t4, t5), t4 + t5)
        self.assertEqual(join(t5, t4), t4 + t5)

        t6 = [self.ln1, self.ln2]
        t7 = [self.ln3]
        self.assertEqual(join(t6, t7), t6 + t7)
        self.assertEqual(join(t7, t6), t6 + t7)

        t8 = [self.lp2, self.ln1]
        t9 = [self.lp2, self.ln3]
        self.assertEqual(join(t8, t9), [self.lp2, self.ln1, self.ln3])

        t10 = [self.lp1, self.lp2]
        t11 = [self.lp2, self.ln3]
        self.assertEqual(join(t10, t11), [self.lp1, self.lp2, self.ln3])

    def test_combine_step(self):
        wt1 = (1.0,  [self.lp1])
        wt2 = (-1.0, [self.lp2, self.ln3])
        self.assertEqual(combine_step(wt1, wt2, float.__add__), (0.0, [self.lp1, self.lp2, self.ln3]))

        wt3 = (-21.0, [self.lp1, self.lp2])
        wt4 = (-2.0,  [self.ln3])
        self.assertEqual(combine_step(wt3, wt4, float.__mul__), (42.0, [self.lp1, self.lp2, self.ln3]))

        wt5 = (42.0,  [self.lp1, self.ln3])
        wt6 = (-1000.0, [self.lp2])
        self.assertEqual(combine_step(wt5, wt6, max), (42.0, [self.lp1, self.lp2, self.ln3]))

    def test_combine(self):
        parser = Parser()

        transition_model = '''
            1.000::running(c1, 1) :- running(c1, 0).
        '''
        atoms1, rules1 = parser.parse(transition_model)
        wdnf1 = WeightedDNF(set(atoms1.keys()))
        for index, rule in enumerate(rules1):
            pos_term = tuple(sorted([Literal.positive(rule.head)] + list(rule.body)))
            wdnf1.add_term(pos_term, rule.probability)
            neg_term = tuple(sorted([Literal.negative(rule.head)] + list(rule.body)))
            wdnf1.add_term(neg_term, 1 - rule.probability)

        value_model = '''
            V(0) :- not(running(c1, 1)), not(running(c2, 1)), not(running(c3, 1)).
            V(1) :- running(c1, 1),      not(running(c2, 1)), not(running(c3, 1)).
            V(1) :- not(running(c1, 1)), running(c2, 1),      not(running(c3, 1)).
            V(1) :- not(running(c1, 1)), not(running(c2, 1)), running(c3, 1).
            V(2) :- running(c1, 1),      running(c2, 1),      not(running(c3, 1)).
            V(2) :- running(c1, 1),      not(running(c2, 1)), running(c3, 1).
            V(2) :- not(running(c1, 1)), running(c2, 1),      running(c3, 1).
            V(3) :- running(c1, 1),      running(c2, 1),      running(c3, 1).
        '''
        atoms2, rules2 = parser.parse(value_model)
        wdnf2 = WeightedDNF(set(atoms2.keys()))
        for index, rule in enumerate(rules2):
            wdnf2.add_term(sorted(rule.body), float(rule.head[2:-1]))

        prod = combine(wdnf1, wdnf2, float.__mul__)
        self.assertEqual(len(prod), len(wdnf2))
        pos = Literal.positive('running(c1,1)')
        neg = Literal.negative('running(c1,1)')
        r1 = Literal.positive('running(c1,0)')
        for weight, term in prod:
            self.assertEqual(len(term), 4)
            if neg in term:
                self.assertEqual(weight, 0.0)
            if pos in term:
                count = sum([literal.is_positive() for literal in term if literal != r1])
                self.assertEqual(weight, float(count))


if __name__ == '__main__':
    unittest.main(verbosity=2)
