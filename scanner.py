import ply.lex as lex
import project1_preprocessor as preprocessor
   
reserved = {
   'int' : 'INT',
   'string' : 'STRING',
   'extern' : 'EXTERN',
   'if' : 'IF',
   'else' : 'ELSE',
   'while' : 'WHILE',
   'do' : 'DO',
   'return' : 'RETURN',
   'for' : 'FOR',
   'then' : 'THEN',
   'const': 'CONST'
}

tokens = ["CONST_INT", "PLUS", "MULTI", "DIV","L_PARENTHESIS",
        "MINUS", "IDENT", "MODULO", "ADD_ASSIGN", "SUB_ASSIGN", 
        "MUL_ASSIGN", "DIV_ASSIGN", "MOD_ASSIGN", "R_PARENTHESIS", "SHIFTLEFT", 
        "SHIFTRIGHT", "EGAL", "DIFF", "INF",
        "SUP", "INFEQUAL", "SUPEQUAL", 
        "SEMI_COL", "ASSIGNMENT", "LEFT_BRACKET", "RIGHT_BRACKET",
        "COMMA", "CONST_STRING"] + list(reserved.values())


def t_IDENT(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'IDENT')    # Check for reserved words
    if len(t.value) > 31:
        raise SyntaxError("%s is longer than 31 characters.\n" % (t.value))
        
    return t

t_ignore = ' \t'

t_PLUS = r'\+'

t_MULTI = r'\*'

t_MINUS = r'-'

t_DIV = r'/'

t_MODULO = r'%'

t_ADD_ASSIGN = r'\+='

t_SUB_ASSIGN = r'-='

t_MUL_ASSIGN = r'\*='

t_DIV_ASSIGN = r'/='

t_MOD_ASSIGN = r'%='

t_L_PARENTHESIS = r'\('

t_R_PARENTHESIS = r'\)'

t_CONST_INT = r'[0-9]+'

t_SHIFTLEFT = r'<<'

t_SHIFTRIGHT = r'>>'

t_EGAL = r'=='

t_DIFF = r'!='

t_INF = r'<'

t_SUP = r'>'

t_INFEQUAL = r'<='

t_SUPEQUAL = r'>='

t_SEMI_COL = r';'

t_ASSIGNMENT = r'='

t_LEFT_BRACKET = r'{'

t_RIGHT_BRACKET = r'}'

t_COMMA = r','

t_CONST_STRING = r'".*"'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    raise SyntaxError("There is an issue on line %d near '%s'\n" % (t.lineno, t.value))

lexer = lex.lex()

if __name__ == '__main__':
    #s = sys.argv[-1]
    #s = "hello.py"
    #source = open(s, "r").read()
    #print source
    source = raw_input()
    source = preprocessor.delete_comments(source)
    source = preprocessor.replace_macro(source)
    lexer = lex.lex()
    lex.input(source)

    print "Lex             Token"
    print "------------------------------"
    while True:
        t = lex.token()
        if not t:
            break
        print t.value, (14-len(t.value))*" ", t.type
