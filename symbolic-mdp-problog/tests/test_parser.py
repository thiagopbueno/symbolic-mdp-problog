
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))

import unittest
import parser


class TestParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        filename1 = os.path.join(os.path.dirname(__file__), '../models/value.pl')
        with open(filename1, 'r') as input:
            cls.value = input.read()

        filename2 = os.path.join(os.path.dirname(__file__), '../models/transition.pl')
        with open(filename2, 'r') as input:
            cls.transition = input.read()

        cls.parser = parser.Parser()

    def test_lex(self):
        data1 = 'V(0) :- running_c1_1, running_c2_1, running_c3_1.'
        tokens = self.parser.tokens(data1)
        self.assertEqual(tokens['NAME'], ['V', 'running_c1_1', 'running_c2_1', 'running_c3_1'])
        self.assertEqual(tokens['INTEGER'], [0])
        self.assertTrue('FLOAT' not in tokens)
        self.assertTrue('COLONCOLON' not in tokens)
        self.assertEqual(len(tokens['COLONMINUS']), 1)
        self.assertEqual(len(tokens['LPAREN']), 1)
        self.assertEqual(len(tokens['RPAREN']), 1)
        self.assertEqual(len(tokens['COMMA']), 2)
        self.assertEqual(len(tokens['PERIOD']), 1)
        self.assertEqual(sum(len(token_lst) for token_lst in tokens.values()), 11)

        data2 = 'V(0) :- running(c1,1), running(c2,1), running(c3,1).'
        tokens = self.parser.tokens(data2)
        self.assertEqual(tokens['NAME'], ['V', 'running', 'c1', 'running', 'c2', 'running', 'c3'])
        self.assertEqual(tokens['INTEGER'], [0, 1, 1, 1])
        self.assertTrue('FLOAT' not in tokens)
        self.assertTrue('COLONCOLON' not in tokens)
        self.assertEqual(len(tokens['COLONMINUS']), 1)
        self.assertEqual(len(tokens['LPAREN']), 4)
        self.assertEqual(len(tokens['RPAREN']), 4)
        self.assertEqual(len(tokens['COMMA']), 5)
        self.assertEqual(len(tokens['PERIOD']), 1)
        self.assertEqual(sum(len(token_lst) for token_lst in tokens.values()), 26)

        data3 = '1.000::running_c1_1 :- reboot_c1.'
        tokens = self.parser.tokens(data3)
        self.assertEqual(tokens['NAME'], ['running_c1_1', 'reboot_c1'])
        self.assertEqual(tokens['FLOAT'], [1.000])
        self.assertTrue('INTEGER' not in tokens)
        self.assertEqual(len(tokens['COLONCOLON']), 1)
        self.assertEqual(len(tokens['COLONMINUS']), 1)
        self.assertTrue('LPAREN' not in tokens)
        self.assertTrue('RPAREN' not in tokens)
        self.assertTrue('COMMA' not in tokens)
        self.assertEqual(len(tokens['PERIOD']), 1)
        self.assertEqual(sum(len(token_lst) for token_lst in tokens.values()), 6)

        data4 = '1.000::running(c1,1) :- reboot(c1).'
        tokens = self.parser.tokens(data4)
        self.assertEqual(tokens['NAME'], ['running', 'c1', 'reboot', 'c1'])
        self.assertEqual(tokens['FLOAT'], [1.000])
        self.assertEqual(tokens['INTEGER'], [1])
        self.assertEqual(len(tokens['COLONCOLON']), 1)
        self.assertEqual(len(tokens['COLONMINUS']), 1)
        self.assertEqual(len(tokens['LPAREN']), 2)
        self.assertEqual(len(tokens['RPAREN']), 2)
        self.assertEqual(len(tokens['COMMA']), 1)
        self.assertEqual(len(tokens['PERIOD']), 1)
        self.assertEqual(sum(len(token_lst) for token_lst in tokens.values()), 14)

        data5 = '0.725::running_c1_1 :- not reboot_c1, running_c1_0, not running_c2_0.'
        tokens = self.parser.tokens(data5)
        self.assertEqual(tokens['NAME'], ['running_c1_1', 'reboot_c1', 'running_c1_0', 'running_c2_0'])
        self.assertEqual(len(tokens['NEGATION']), 2)
        self.assertEqual(tokens['FLOAT'], [0.725])
        self.assertTrue('INTEGER' not in tokens)
        self.assertEqual(len(tokens['COLONCOLON']), 1)
        self.assertEqual(len(tokens['COLONMINUS']), 1)
        self.assertTrue('LPAREN' not in tokens)
        self.assertTrue('RPAREN' not in tokens)
        self.assertEqual(len(tokens['COMMA']), 2)
        self.assertEqual(len(tokens['PERIOD']), 1)
        self.assertEqual(sum(len(token_lst) for token_lst in tokens.values()), 12)

        data6 = '0.725::running(c1,1) :- not reboot(c1), running(c1,0), not running(c2,0).'
        tokens = self.parser.tokens(data6)
        self.assertEqual(tokens['NAME'], ['running', 'c1', 'reboot', 'c1', 'running', 'c1', 'running', 'c2'])
        self.assertEqual(len(tokens['NEGATION']), 2)
        self.assertEqual(tokens['FLOAT'], [0.725])
        self.assertEqual(tokens['INTEGER'], [1, 0, 0])
        self.assertEqual(len(tokens['COLONCOLON']), 1)
        self.assertEqual(len(tokens['COLONMINUS']), 1)
        self.assertEqual(len(tokens['LPAREN']), 4)
        self.assertEqual(len(tokens['RPAREN']), 4)
        self.assertEqual(len(tokens['COMMA']), 5)
        self.assertEqual(len(tokens['PERIOD']), 1)
        self.assertEqual(sum(len(token_lst) for token_lst in tokens.values()), 30)

    def test_yacc(self):
        program1 = self.parser.parse(self.transition)
        self.assertEqual(len(program1), len(self.transition.split('\n')))

        program2 = self.parser.parse(self.value)
        self.assertEqual(len(program2), len(self.value.split('\n')))


if __name__ == '__main__':
    unittest.main(verbosity=2)
