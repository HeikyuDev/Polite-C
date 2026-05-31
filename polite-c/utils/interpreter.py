import ply.yacc as yacc
from .lexer import tokens, get_lexer

# ----------------------------------------------------------------------
# 1. DEFINICIÓN DE LA GRAMÁTICA Y CONSTRUCCIÓN DEL AST
# ----------------------------------------------------------------------

def p_program(p):
    '''program : HELLO MAIN EXCLAMATION PLEASE DO THIS COLON NEWLINE INDENT statement_list DEDENT THANKS EXCLAMATION NEWLINE'''
    p[0] = ('main_program', p[10])

# Esta regla alternativa permite asimilar si el usuario no dejó un salto de línea tras el 'thanks!'
def p_program_no_final_newline(p):
    '''program : HELLO MAIN EXCLAMATION PLEASE DO THIS COLON NEWLINE INDENT statement_list DEDENT THANKS EXCLAMATION'''
    p[0] = ('main_program', p[10])

def p_statement_list(p):
    '''statement_list : statement statement_list'''
    p[0] = [p[1]] + p[2]

def p_statement_list_empty(p):
    '''statement_list : empty'''
    p[0] = []

def p_statement_define(p):
    '''statement : PLEASE DEFINE COLON ID AS type NEWLINE'''
    p[0] = ('define_var', p[4], p[6])

def p_type(p):
    '''type : TYPE_NUMBER
            | TYPE_FLOAT
            | TYPE_WORD'''
    p[0] = p[1]

def p_statement_say(p):
    '''statement : PLEASE SAY COLON expression NEWLINE'''
    p[0] = ('say', p[4])

def p_statement_read(p):
    '''statement : PLEASE READ COLON ID NEWLINE'''
    p[0] = ('read', p[4])

def p_statement_assign(p):
    '''statement : PLEASE MAKE ID EQUALS TO expression NEWLINE'''
    p[0] = ('assign', p[3], p[6])

def p_statement_if(p):
    '''statement : IF THIS HAPPENS condition PLEASE DO THIS COLON NEWLINE INDENT statement_list DEDENT'''
    p[0] = ('if_block', p[4], p[10])

def p_statement_if_not(p):
    '''statement : IF NOT COLON NEWLINE INDENT statement_list DEDENT'''
    p[0] = ('else_block', p[6])

def p_condition(p):
    '''condition : ID'''
    p[0] = p[1]

def p_expression_literal(p):
    '''expression : WORD_LITERAL
                  | NUMBER_LITERAL'''
    p[0] = ('literal', p[1])

def p_expression_var(p):
    '''expression : ID'''
    p[0] = ('variable', p[1])

def p_empty(p):
    'empty :'
    pass

parser_errors = []
def p_error(p):
    if p:
        parser_errors.append(f"Error de cortesía sintáctica cerca de '{p.value}' (Línea {p.lineno})")
    else:
        parser_errors.append("Error de sintaxis: Fin de archivo inesperado. ¿Olvidaste cerrar el main de forma educada?")

# ----------------------------------------------------------------------
# 2. MOTOR DEL INTÉRPRETE (EJECUTA EL AST)
# ----------------------------------------------------------------------

class PoliteInterpreter:
    def __init__(self):
        self.output_buffer = []
        self.variables = {}

    def execute(self, source_code, user_inputs=None):
        if user_inputs is None: user_inputs = {}
        
        global parser_errors
        parser_errors = []
        
        if not source_code.endswith('\n'):
            source_code += '\n'
            
        lexer = get_lexer()
        lexer.input(source_code)
        
        parser = yacc.yacc(debug=False, write_tables=False)
        ast = parser.parse(lexer=lexer)
        
        from .lexer import lexer_errors
        all_errors = lexer_errors + parser_errors
        if all_errors:
            return {'status': 'completed', 'output': "\n".join(all_errors)}
            
        if not ast:
            return {'status': 'completed', 'output': "Error: Estructura de código irreconocible."}

        _, statements = ast
        result = self.run_statements(statements, user_inputs)
        return result

    def run_statements(self, statements, user_inputs):
        for stmt in statements:
            stmt_type = stmt[0]
            
            if stmt_type == 'define_var':
                _, var_name, var_type = stmt
                if var_name not in self.variables:
                    if var_type == 'number': self.variables[var_name] = 0
                    else: self.variables[var_name] = ""
                    
            elif stmt_type == 'say':
                expr = stmt[1]
                if expr[0] == 'literal':
                    val = expr[1]
                    if val.startswith('"'): val = val[1:-1]
                    self.output_buffer.append(str(val))
                elif expr[0] == 'variable':
                    var_name = expr[1]
                    self.output_buffer.append(str(self.variables.get(var_name, "Error: Variable no definida")))
                    
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
                expr = stmt[2]
                if expr[0] == 'literal':
                    val = expr[1]
                    if val.startswith('"'): val = val[1:-1]
                    self.variables[var_name] = val
                elif expr[0] == 'variable':
                    var_name_src = expr[1]
                    self.variables[var_name] = self.variables.get(var_name_src, 0)
                    
            elif stmt_type == 'if_block':
                _, var_condition, if_statements = stmt
                val = self.variables.get(var_condition, 0)
                if val and val != "0":
                    res = self.run_statements(if_statements, user_inputs)
                    if res and res['status'] == 'awaiting_input': return res

        return {
            'status': 'completed',
            'output': "\n".join(self.output_buffer)
        }