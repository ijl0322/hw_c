import ply.yacc as yacc
from scanner import tokens

def p_expression_1(t):
    '''expression : expression_additive'''
    print "expression"
    t[0] = t[1]

def p_expression_2(t):
    '''expression : expression SHIFTLEFT expression_additive'''
    t[0] = 'SHIFTLEFT', t[1], t[3]

def p_expression_3(t):
    '''expression : expression SHIFTRIGHT expression_additive'''
    t[0] = 'SHIFTRIGHT', t[1], t[3]

### expression_additive

def p_expression_additive_1(t):
    '''expression_additive : expression_multiplicative'''
    print "add"
    t[0] = t[1]

def p_expression_additive_2(t):
    '''expression_additive : expression_additive PLUS expression_multiplicative'''
    t[0] = ('PLUS', t[1], t[3])

def p_additive_expression_3(t):
    'expression_additive : expression_additive MINUS expression_multiplicative'
    t[0] = ('MINUS', t[1], t[3])

### expression_multiplicative

def p_expression_multiplicative_1(t):
    'expression_multiplicative : unary_expression'
    print "mult"
    t[0] = t[1]

def p_expression_multiplicative_2(t):
    'expression_multiplicative : expression_multiplicative MULTI unary_expression'
    t[0] = 'MUL', t[1], t[3]

def p_expression_multiplicative_3(t):
    'expression_multiplicative : expression_multiplicative DIV unary_expression'
    t[0] = 'DIV', t[1], t[3]

def p_multiplicative_expression_4(t):
    'expression_multiplicative : expression_multiplicative MODULO unary_expression'
    t[0] = 'MODULO', t[1], t[3]

### unary_expression

def p_unary_expression_1(t): #numeric values? 
    '''unary_expression : postfix_expression'''
    print "unary"
    t[0] = t[1]

def p_unary_expression_2(t): #negative numeric values? 
    '''unary_expression : MINUS unary_expression'''
    t[0] = ('NEG',t[2])
    
### postfix_expression

def p_postfix_expression_1(t):
    '''postfix_expression : primary_expression'''
    print "postfix"
    t[0] = t[1]

def p_postfix_expression_2(t):
    '''postfix_expression : IDENT L_PARENTHESIS argument_expression_list R_PARENTHESIS'''
    t[0] = ('CALL_FUNC',t[1], t[3])    
    print "Calling function %s" %(t[1])
    
def p_postfix_expression_3(t):
    '''postfix_expression : IDENT L_PARENTHESIS R_PARENTHESIS'''
    t[0] = ('CALL_FUNC',t[1], None)    
    print "Calling function %s" %(t[1])    

### argument_expression

def p_argument_expression_list_1(t):
    '''argument_expression_list : expression'''
    t[0] = [t[1]]
    
def p_argument_expression_list_2(t):
    '''argument_expression_list : argument_expression_list COMMA expression'''
    #put the expressions into one list ?
    t[0] = t[1] + [t[3]]
    
### primary_expression

def p_primary_expression_1(t):
    '''primary_expression : IDENT'''
    t[0] = ('IDENT', t[1])

def p_primary_expression_2(t):
    '''primary_expression : CONST_INT'''
    t[0] = ('CONST_INT',t[1])
    
def p_primary_expression_3(t):
    '''primary_expression : CONST_STRING'''
    t[0] = ('CONST_STRING', t[1])

def p_primary_expression_4(t):
    '''primary_expression : L_PARENTHESIS expression R_PARENTHESIS'''
    t[0] = ('PRIME_EXPRESS',t[2])
    
### test_case remove later
#def p_expression(t):
#    '''expression : primary_expression'''
#    t[0] = t[1]
    
def p_error(t):
    if t:
         print("Syntax error at token", t[0])
         parser.errok()
    else:
         print("Syntax error at EOF")


if __name__ == '__main__':
    S = raw_input("Input expression: ")
    parser = yacc.yacc()
    print(parser.parse(S))