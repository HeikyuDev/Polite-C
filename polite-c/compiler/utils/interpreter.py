import ply.yacc as yacc
from .lexer import tokens, get_lexer

# ----------------------------------------------------------------------
# 1. GRAMÁTICA CON SOPORTE MULTI-PARÁMETRO EN IMPRESIÓN
# ----------------------------------------------------------------------

def p_program(p):
    '''program : class_list main_block'''
    p[0] = ('program', p[1], p[2])

def p_class_list_empty(p):
    '''class_list : empty'''
    p[0] = []

def p_class_list(p):
    '''class_list : class_definition class_list'''
    p[0] = [p[1]] + p[2]

def p_class_definition(p):
    '''class_definition : CLASS ID PLEASE_DO_THIS statement_list FINISH'''
    p[0] = ('class_def', p[2], p[4])

def p_main_block(p):
    '''main_block : HELLO_MAIN PLEASE_DO_THIS statement_list THANKS'''
    p[0] = ('main_block', p[3])

def p_statement_list_empty(p):
    '''statement_list : empty'''
    p[0] = []

def p_statement_list(p):
    '''statement_list : statement statement_list'''
    p[0] = [p[1]] + p[2]

def p_statement(p):
    '''statement : statement_define
                 | statement_say
                 | statement_read
                 | statement_assign
                 | statement_create
                 | statement_ask
                 | statement_if
                 | method_definition'''
    p[0] = p[1]

def p_statement_define(p):
    '''statement_define : PLEASE_DEFINE ID AS type'''
    p[0] = ('define_var', p[2], p[4])

def p_type(p):
    '''type : TYPE_NUMBER
            | TYPE_FLOAT
            | TYPE_WORD
            | ID'''
    p[0] = p[1]

# REGLA ARREGLADA: Ahora acepta listas de parámetros separadas por comas
def p_statement_say(p):
    '''statement_say : PLEASE_SAY expression_list'''
    p[0] = ('say', p[2])

def p_statement_read(p):
    '''statement_read : PLEASE_READ ID'''
    p[0] = ('read', p[2])

def p_statement_assign_conversational(p):
    '''statement_assign : PLEASE MAKE ID EQUALS TO expression
                        | MAKE ID EQUALS TO expression'''
    if len(p) == 7: p[0] = ('assign', p[3], p[6])
    else: p[0] = ('assign', p[2], p[5])

def p_statement_assign_direct(p):
    '''statement_assign : ID ASSIGN expression'''
    p[0] = ('assign', p[1], p[3])

def p_statement_create(p):
    '''statement_create : PLEASE_CREATE ID AS ID'''
    p[0] = ('create_obj', p[2], p[4])

def p_statement_ask(p):
    '''statement_ask : PLEASE_ASK ID TO ID argument_list'''
    p[0] = ('ask_method', p[2], p[4], p[5])

def p_method_definition_no_return(p):
    '''method_definition : ID RECEIVES LPAREN param_list RPAREN PLEASE_DO_THIS statement_list FINISH'''
    p[0] = ('method_def_no_return', p[1], p[4], p[7])

def p_method_definition_with_return(p):
    '''method_definition : ID RECEIVES LPAREN param_list RPAREN TO_GIVE type PLEASE_DO_THIS statement_list PLEASE_GIVE_BACK expression FINISH'''
    p[0] = ('method_def_with_return', p[1], p[4], p[7], p[9], p[11])

def p_param_list_empty(p):
    '''param_list : empty'''
    p[0] = []

def p_param_list(p):
    '''param_list : param resto_param'''
    p[0] = [p[1]] + p[2]

def p_param(p):
    '''param : ID AS type'''
    p[0] = ('param', p[1], p[3])

def p_resto_param_empty(p):
    '''resto_param : empty'''
    p[0] = []

def p_resto_param(p):
    '''resto_param : COMMA param resto_param'''
    p[0] = [p[2]] + p[3]

def p_argument_list_empty(p):
    '''argument_list : empty'''
    p[0] = []

def p_argument_list_single(p):
    '''argument_list : WITH expression'''
    p[0] = [p[2]]

def p_argument_list_multiple(p):
    '''argument_list : WITH LPAREN expression_list RPAREN'''
    p[0] = p[3]

def p_expression_list(p):
    '''expression_list : expression resto_expr'''
    p[0] = [p[1]] + p[2]

def p_resto_expr_empty(p):
    '''resto_expr : empty'''
    p[0] = []

def p_resto_expr(p):
    '''resto_expr : COMMA expression resto_expr'''
    p[0] = [p[2]] + p[3]

def p_statement_if(p):
    '''statement_if : IF_HAPPENS LPAREN expression_relational RPAREN PLEASE_DO_THIS statement_list else_block FINISH'''
    p[0] = ('if_block', p[3], p[6], p[7])

def p_else_block_empty(p):
    '''else_block : empty'''
    p[0] = []

def p_else_block(p):
    '''else_block : IF_NOT PLEASE_DO_THIS statement_list'''
    p[0] = p[3]

def p_expression_relational(p):
    '''expression_relational : expression EQ expression
                             | expression NE expression
                             | expression LT expression
                             | expression GT expression
                             | expression LE expression
                             | expression GE expression'''
    p[0] = ('rel_op', p[2], p[1], p[3])

def p_expression_plus(p):
    '''expression : expression PLUS term'''
    p[0] = ('arith_op', '+', p[1], p[3])

def p_expression_minus(p):
    '''expression : expression MINUS term'''
    p[0] = ('arith_op', '-', p[1], p[3])

def p_expression_term(p):
    '''expression : term'''
    p[0] = p[1]

def p_term_mult(p):
    '''term : term MULT factor'''
    p[0] = ('arith_op', '*', p[1], p[3])

def p_term_div(p):
    '''term : term DIV factor'''
    p[0] = ('arith_op', '/', p[1], p[3])

def p_term_mod(p):
    '''term : term MOD factor'''
    p[0] = ('arith_op', '%', p[1], p[3])

def p_term_factor(p):
    '''term : factor'''
    p[0] = p[1]

def p_factor_id(p):
    '''factor : ID'''
    p[0] = ('variable', p[1])

def p_factor_num(p):
    '''factor : NUMBER_LITERAL'''
    p[0] = ('literal', p[1])

def p_factor_float(p):
    '''factor : FLOAT_LITERAL'''
    p[0] = ('literal', p[1])

def p_factor_word(p):
    '''factor : WORD_LITERAL'''
    p[0] = ('literal', p[1])

def p_factor_ask(p):
    '''factor : statement_ask'''
    p[0] = p[1]

def p_factor_expr(p):
    '''factor : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_empty(p):
    'empty :'
    pass

parser_errors = []
def p_error(p):
    if p:
        parser_errors.append(f"Error de cortesía sintáctica cerca de '{p.value}' (Línea {p.lineno})")
    else:
        parser_errors.append("Error de sintaxis: Fin de archivo inesperado. ¿Olvidaste cerrar el bloque de forma educada?")

# ----------------------------------------------------------------------
# 2. MOTOR DE EJECUCIÓN (INTÉRPRETE)
# ----------------------------------------------------------------------

class PoliteInterpreter:
    def __init__(self):
        self.output_buffer = []
        self.variables = {}

    def execute(self, source_code, user_inputs=None):
        if user_inputs is None: user_inputs = {}
        global parser_errors
        parser_errors = []
        
        lexer = get_lexer()
        parser = yacc.yacc(debug=False, write_tables=False)
        ast = parser.parse(source_code, lexer=lexer)
        
        from .lexer import lexer_errors
        all_errors = lexer_errors + parser_errors
        if all_errors:
            return {'status': 'completed', 'output': "\n".join(all_errors)}
            
        if not ast:
            return {'status': 'completed', 'output': "Error: Estructura de código irreconocible."}

        _, class_list, main_block = ast
        _, statements = main_block
        
        result = self.run_statements(statements, user_inputs)
        return result

    def evaluate_expression(self, expr):
        if expr[0] == 'literal':
            val = expr[1]
            if isinstance(val, str) and val.startswith('"'): return val[1:-1]
            return val
        elif expr[0] == 'variable':
            return self.variables.get(expr[1], 0)
        elif expr[0] == 'arith_op':
            op = expr[1]
            left = self.evaluate_expression(expr[2])
            right = self.evaluate_expression(expr[3])
            try:
                if op == '+': return left + right
                elif op == '-': return left - right
                elif op == '*': return left * right
                elif op == '/': return left / right
                elif op == '%': return left % right
            except:
                return 0
        return 0

    def evaluate_condition(self, cond):
        if cond[0] == 'rel_op':
            op = cond[1]
            left = self.evaluate_expression(cond[2])
            right = self.evaluate_expression(cond[3])
            if op == '==': return left == right
            elif op == '!=': return left != right
            elif op == '<': return left < right
            elif op == '>': return left > right
            elif op == '<=': return left <= right
            elif op == '>=': return left >= right
        return bool(self.evaluate_expression(cond))

    def run_statements(self, statements, user_inputs):
        for stmt in statements:
            stmt_type = stmt[0]
            
            if stmt_type == 'define_var':
                _, var_name, var_type = stmt
                if var_name not in self.variables:
                    if var_type == 'number': self.variables[var_name] = 0
                    elif var_type == 'floatnumber': self.variables[var_name] = 0.0
                    else: self.variables[var_name] = ""
                    
            elif stmt_type == 'say':
                # PROCESAMIENTO MULTI-PARÁMETRO: Evalúa y concatena la lista de expresiones
                expr_list = stmt[1]
                val_strs = [str(self.evaluate_expression(e)) for e in expr_list]
                self.output_buffer.append("".join(val_strs))
                    
            elif stmt_type == 'read':
                var_name = stmt[1]
                if var_name in user_inputs:
                    self.variables[var_name] = user_inputs[var_name]
                else:
                    return {
                        'status': 'awaiting_input',
                        'variable': var_name,
                        'output': "\n".join(self.output_buffer)
                    }
                    
            elif stmt_type == 'assign':
                var_name = stmt[1]
                self.variables[var_name] = self.evaluate_expression(stmt[2])
                    
            elif stmt_type == 'if_block':
                _, cond, if_statements, else_statements = stmt
                if self.evaluate_condition(cond):
                    res = self.run_statements(if_statements, user_inputs)
                    if res and res['status'] == 'awaiting_input': return res
                else:
                    res = self.run_statements(else_statements, user_inputs)
                    if res and res['status'] == 'awaiting_input': return res

        return {
            'status': 'completed',
            'output': "\n".join(self.output_buffer)
        }