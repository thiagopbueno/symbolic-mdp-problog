from ply import lex
from ply import yacc

from rule import Rule

# Tokenizer for ProbLog programs ===========================

tokens = (
    'NAME',
    'INTEGER',
    'FLOAT',
    'LPAREN',
    'RPAREN',
    'COMMA',
    'COLONCOLON',
    'COLONMINUS',
    'PERIOD',
    'NEGATION'
)


t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA  = r','
t_COLONCOLON = r'::'
t_COLONMINUS = r':-'
t_PERIOD = '.'

t_ignore = ' \t'

reserved = {
    'not': 'NEGATION'
}


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'NAME')
    return t


def t_FLOAT(t):
    r'\d+.\d+'
    t.value = float(t.value)
    return t


def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lineno += len(t.value)


def t_error(t):
    print("Error: illegal character '{0}'".format(t.value[0]))
    t.lexer.skip(1)


# build the lexer
lex.lex()


# Parser for ProbLog programs ==============================

def p_program(p):
    '''program : rules'''
    p[0] = p[1]


def p_rules(p):
    '''rules : rule rules
             | rule'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]


def p_rule(p):
    '''rule : head COLONMINUS body PERIOD
            | fact'''
    head = p[1]
    probability = None
    if type(head) is tuple:
        probability = head[0]
        head = head[1]
    if len(p) == 5:
        body = p[3]
    else:
        body = []
    p[0] = Rule(head, body, probability)


def p_fact(p):
    '''fact : head PERIOD'''
    p[0] = p[1]


def p_head(p):
    '''head : number COLONCOLON atom
            | atom'''
    if len(p) == 4:
        p[0] = (p[1], p[3])
    else:
        p[0] = p[1]


def p_body(p):
    '''body : literal COMMA body
            | literal '''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_literal(p):
    '''literal : NEGATION LPAREN atom RPAREN
               | NEGATION atom
               | atom'''
    if len(p) == 5:
        p[0] = ('-', p[3])
    elif len(p) == 3:
        p[0] = ('-', p[2])
    else:
        p[0] = ('+', p[1])


def p_atom(p):
    '''atom : NAME LPAREN args RPAREN
            | NAME'''
    if len(p) == 5:
        p[0] = ''.join(p[1:])
    elif len(p) == 2:
        p[0] = p[1]


def p_args(p):
    '''args : NAME COMMA args
            | number COMMA args
            | NAME
            | number'''
    if len(p) == 4:
        p[0] = '{0},{1}'.format(p[1], p[3])
    elif len(p) == 2:
        p[0] = p[1]


def p_number(p):
    '''number : FLOAT
              | INTEGER'''
    p[0] = str(p[1])


def p_error(p):
    print("Error: syntax error when parsing `{}`.".format(p))


# build the parser
yacc.yacc()


class Parser(object):

    def tokens(self, data):
        lex.input(data)
        tokens_dict = {}
        while True:
            tok = lex.token()
            if not tok:
                break
            tokens_dict[tok.type] = tokens_dict.get(tok.type, [])
            tokens_dict[tok.type].append(tok.value)
        return tokens_dict

    def parse(self, data):
        return yacc.parse(data)
