import ply.yacc as yacc
from scanner import tokens

precedence = ( ('nonassoc', 'IF_STATE'), ('nonassoc', 'IF_ELSE')) 

def p_program_1(t):
    'program : external_declaration'
    t[0] = [t[1]]
    return t[0]

def p_program_2(t):
    'program : program external_declaration'
    t[0] = t[1] + [t[2]]
    return t[0]

### external-declaration:

def p_external_declaration_1(t):
    '''external_declaration : declaration'''
    t[0] = t[1]

def p_external_declaration_2(t):
    'external_declaration : EXTERN declaration'
    t[0] = ('EXTERN', t[2])

def p_external_declaration_3(t):
    '''external_declaration : function-definition'''
    t[0] = t[1]

### function

def p_function(t):
    '''function-definition : type function_declarator compound_instruction''' 
    t[0] = 'DEF_FUNC', t[1], t[2], t[3]
    print "Declaring function %s which returns type %s and take parameters" %(t[2][1], t[1][1]), t[2][2] 
    
### declaration

def p_declaration(t): # multiple variable declaration on the same line ??? 
    '''declaration : type declarator_list SEMI_COL'''
    t[0] = (t[1], t[2])

### type

def p_type(t):
    '''type : INT
            | STRING'''
    t[0] = ('TYPE', t[1])    

### declarator list

def p_declarator_list_1(t):
    '''declarator_list : declarator'''
    t[0] = [t[1]]
    
def p_declarator_list_2(t):
    '''declarator_list : declarator_list COMMA declarator'''
    t[0] = t[1] + [t[3]]    

### declaration_list

def p_declaration_list_1(t):
    '''declaration_list : declaration'''
    t[0] = [t[1]]

def p_declaration_list_2(t):
    '''declaration_list : declaration_list declaration'''
    t[0] = t[1] + [t[2]]
    
### declarator 

def p_declarator(t):
    '''declarator : IDENT
                    | function_declarator'''
    t[0] = t[1]

### function_declare

def p_function_declarator_1(t):
    '''function_declarator : IDENT L_PARENTHESIS parameter_list R_PARENTHESIS'''
    t[0] = ('IDENT', t[1], t[3])

def p_function_declarator_2(t):
    '''function_declarator : IDENT L_PARENTHESIS R_PARENTHESIS'''
    t[0] = ('IDENT', t[1], None)

### parameter_list

def p_parameter_list_1(t):
    '''parameter_list : parameter_declaration'''
    t[0] = [t[1]]

def p_parameter_list_2(t):
    '''parameter_list : parameter_list COMMA parameter_declaration'''
    t[0] = t[1] + [t[3]]

### parameter_declaration

def p_parameter_declaration(t):
    '''parameter_declaration : type IDENT'''
    t[0] = t[1], t[2]
    
### ---------- code under is probably working ? ---- 

### instruction
def p_instruction_1(t):
    '''instruction : SEMI_COL'''
    t[0] = ('STATE', None)

def p_instruction_2(t):
    '''
    instruction : expression_instruction
              | compound_instruction
              | select_instruction
              | iteration_instruction
              | jump_instruction
              '''
    t[0] = ('STATE', t[1])

### expression_instruction
def p_expression_instruction_1(t):
    '''expression_instruction : expression SEMI_COL'''
    t[0] = t[1]

def p_expression_instruction_2(t):
    '''expression_instruction : assignment SEMI_COL'''
    t[0] = t[1]
    
### assignment

def p_assignment(t):
    '''assignment : IDENT ASSIGNMENT expression'''
    t[0] = ('ASSIGN', t[1], t[3])

### compound_instruction

def p_compound_instruction_1(t):
    '''compound_instruction : block_start declaration_list instruction_list block_end'''
    t[0] = ('COMP_STATE', t[2] + t[3])

def p_compound_instruction_2(t):
    '''compound_instruction : block_start declaration_list block_end'''
    t[0] = ('COMP_STATE', t[2])

def p_compound_instruction_3(t):
    '''compound_instruction : block_start instruction_list block_end'''
    t[0] = ('COMP_STATE', t[2])
    
def p_compound_instruction_4(t):
    '''compound_instruction : block_start block_end'''
    t[0] = ('COMP_STATE', [])
    
### block

def p_block_start(t):
    '''block_start : LEFT_BRACKET'''
    t[0] = t[1]

def p_block_end(t):
    '''block_end : RIGHT_BRACKET'''
    t[0] = t[1]

### instruction_list:

def p_instruction_list_1(t):
    '''instruction_list : instruction'''
    t[0] = [t[1]]

def p_instruction_list_2(t):
    '''instruction_list : instruction_list instruction'''
    t[0] = t[1] + [t[2]]

### select_instruction

def p_select_instruction_1(t):
    '''select_instruction : cond_instruction instruction %prec IF_STATE'''
    t[0] = (t[1], t[3]) 
    
def p_select_instruction_2(t):
    '''select_instruction : cond_instruction instruction ELSE instruction %prec IF_ELSE'''
    t[0] = ('ELSE', t[1], t[2], t[4])


### condition_instruction

def p_cond_instruction(t):    
    '''cond_instruction : IF L_PARENTHESIS condition R_PARENTHESIS''' 
    t[0] = ('IF', t[3])

### iteration_instruction

def p_iteration_instruction_1(t):
    '''iteration_instruction : WHILE L_PARENTHESIS condition R_PARENTHESIS instruction'''
    t[0] = ('WHILE', t[3], t[5])
    print "While loop"

def p_iteration_instruction_2(t):
    '''iteration_instruction : DO instruction WHILE L_PARENTHESIS condition R_PARENTHESIS'''
    t[0] = ('DO_WHILE', t[2], t[5])
    print "Do while"
    
def p_iteration_instruction_3(t):
    '''iteration_instruction : FOR L_PARENTHESIS expression SEMI_COL condition SEMI_COL expression R_PARENTHESIS instruction '''
    t[0] = ('FOR', t[3], t[5], t[7], t[9])
    print "For loop"
    
### jump_instruction

def p_jump_instruction(t):
    '''jump_instruction : RETURN expression SEMI_COL'''
    t[0] = ('RETURN', t[2])
    
### condition

def p_condition(t):
    '''condition : expression comparison_operator expression'''
    t[0] = (t[2], t[1], t[3])
    
### comparison_operator
    
def p_comparison_operator(t):
    '''comparison_operator : EGAL
                        | DIFF
                        | INF 
                        | SUP 
                        | INFEQUAL
                        | SUPEQUAL '''
    print "comp"
    t[0] = t[1]

### expression

def p_expression_1(t):
    '''expression : expression_additive'''
    print "expression"
    t[0] = t[1]

def p_expression_2(t):
    '''expression : expression SHIFTLEFT expression_additive'''
    t[0] = ('SHIFTLEFT', t[1], t[3])

def p_expression_3(t):
    '''expression : expression SHIFTRIGHT expression_additive'''
    t[0] = ('SHIFTRIGHT', t[1], t[3])

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
    parser = yacc.yacc(method='LALR')
    print(parser.parse(S))