import ply.yacc as yacc
from .lexer import tokens, get_lexer

# ----------------------------------------------------------------------
# 1. GRAMÁTICA CON SOPORTE MULTI-PARÁMETRO EN IMPRESIÓN (ELEGANTES BNF)
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
    # Modificación a la regla para que acepte explícitamente el token OBJECT
    '''statement_create : PLEASE_CREATE OBJECT ID'''
    # Para permitir creación de objetos dentro del bloque main
    p[0] = ('create_obj_single', p[3])

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

polite_parser = yacc.yacc(debug=False, write_tables=False)

# ----------------------------------------------------------------------
# 2. MOTOR DE EJECUCIÓN DEL INTERPRETE (ACTUALIZADO PARA COMPATIBILIDAD POO)
# ----------------------------------------------------------------------

class PoliteInstance:
    """Clase auxiliar para emular la memoria interna (atributos) de cada objeto."""
    def __init__(self, class_name):
        self.class_name = class_name
        self.fields = {}

class PoliteInterpreter:
    def __init__(self):
        self.output_buffer = []
        self.global_variables = {}
        self.classes_blueprints = {}  # Guarda los moldes de las clases: { nombre_clase: [sentencias/metodos] }

    def execute(self, source_code, user_inputs=None):
        if user_inputs is None: user_inputs = {}
        global parser_errors
        parser_errors = []
        
        lexer = get_lexer()
        ast = polite_parser.parse(source_code, lexer=lexer)
        
        from .lexer import lexer_errors
        all_errors = lexer_errors + parser_errors
        if all_errors:
            return {'status': 'completed', 'output': "\n".join(all_errors)}
            
        if not ast:
            return {'status': 'completed', 'output': "Error: Estructura de código irreconocible."}

        # PROCESAMIENTO COMPATIBLE DE LA RAÍZ DEL ÁRBOL
        _, class_list, main_block = ast
        
        # 1. Almacenar los "planos" estructurales de las clases
        for clazz in class_list:
            _, class_name, class_statements = clazz
            self.classes_blueprints[class_name] = class_statements
            
        # 2. Ejecutar el bloque principal con memoria global limpia
        _, statements = main_block
        result = self.run_statements(statements, user_inputs, current_context=self.global_variables)
        return result

    def evaluate_expression(self, expr, current_context):
        if expr[0] == 'literal':
            val = expr[1]
            if isinstance(val, str) and val.startswith('"'):
                return val[1:-1]
            return int(val) if str(val).isdigit() else float(val)
            
        elif expr[0] == 'variable':
            var_name = expr[1]
            # Búsqueda con prioridad: contextual (local/objeto) -> global
            if var_name in current_context: return current_context[var_name]
            return self.global_variables.get(var_name, 0)
            
        elif expr[0] == 'arith_op':
            op = expr[1]
            left = self.evaluate_expression(expr[2], current_context)
            right = self.evaluate_expression(expr[3], current_context)
            try:
                if op == '+': return left + right
                elif op == '-': return left - right
                elif op == '*': return left * right
                elif op == '/': return left / right if right != 0 else "Error: División por cero"
                elif op == '%': return left % right
            except:
                return 0
                
        elif expr[0] == 'ask_method':
            # Soporte para asignación directa desde métodos con retorno: miVar = please ask obj to met
            res = self.execute_method_call(expr, {}, current_context)
            if isinstance(res, dict) and 'return_value' in res:
                return res['return_value']
            return 0
        return 0

    def evaluate_condition(self, cond, current_context):
        if cond[0] == 'rel_op':
            op = cond[1]
            left = self.evaluate_expression(cond[2], current_context)
            right = self.evaluate_expression(cond[3], current_context)
            if op == '==': return left == right
            elif op == '!=': return left != right
            elif op == '<': return left < right
            elif op == '>': return left > right
            elif op == '<=': return left <= right
            elif op == '>=': return left >= right
        return bool(self.evaluate_expression(cond, current_context))

    def execute_method_call(self, stmt, user_inputs, current_context):
        _, obj_name, method_name, args = stmt
        
        obj = current_context.get(obj_name, self.global_variables.get(obj_name))
        if not isinstance(obj, PoliteInstance):
            self.output_buffer.append(f"Error: '{obj_name}' no es un objeto instanciado.")
            return None
            
        class_statements = self.classes_blueprints.get(obj.class_name, [])
        target_method = None
        for s in class_statements:
            if s[0] in ('method_def_no_return', 'method_def_with_return') and s[1] == method_name:
                target_method = s
                break
                
        if not target_method:
            self.output_buffer.append(f"Error: El método '{method_name}' no existe en la clase '{obj.class_name}'.")
            return None
            
        # El contexto del método se ejecuta SOBRE la memoria del objeto (para que pueda leer sus atributos como 'numero')
        local_memory = obj.fields 
        
        # Procesar e inyectar parámetros pasados con 'with'
        params = target_method[2]  # Estructura: [('param', 'valor', 'number')]
        evaluated_args = [self.evaluate_expression(a, current_context) for a in args]
        
        for idx, param_node in enumerate(params):
            if idx < len(evaluated_args):
                local_memory[param_node[1]] = evaluated_args[idx] # Asigna el argumento al parámetro local
                
        method_statements = target_method[3] if target_method[0] == 'method_def_no_return' else target_method[4]
        res = self.run_statements(method_statements, user_inputs, current_context=local_memory)
        
        if res and isinstance(res, dict) and res.get('status') == 'awaiting_input':
            return res
            
        if target_method[0] == 'method_def_with_return':
            return_expr = target_method[5]
            return {'return_value': self.evaluate_expression(return_expr, local_memory)}
            
        return None

    def run_statements(self, statements, user_inputs, current_context):
        for stmt in statements:
            stmt_type = stmt[0]
            
            if stmt_type == 'define_var':
                _, var_name, var_type = stmt
                if var_name not in current_context:
                    if var_type == 'number': current_context[var_name] = 0
                    elif var_type == 'floatnumber': current_context[var_name] = 0.0
                    elif var_type == 'word': current_context[var_name] = ""
                    else: current_context[var_name] = ('blueprint_ref', var_type) # Declaración tipo Objeto
                    
            elif stmt_type == 'create_obj_single':
                var_name = stmt[1]
                
                # Buscamos en la memoria qué tipo de clase se le asignó a esta variable en su definición
                class_name = current_context.get(var_name)
                
                # Si es una tupla de referencia previa ('blueprint_ref', tipo_clase) o texto directo
                if isinstance(class_name, tuple) and class_name[0] == 'blueprint_ref':
                    class_name = class_name[1]
                
                if class_name in self.classes_blueprints:
                    # Instanciación real con memoria encapsulada
                    new_instance = PoliteInstance(class_name)
                    
                    # Precargar las propiedades definidas dentro de la clase como atributos limpios
                    for class_stmt in self.classes_blueprints[class_name]:
                        if class_stmt[0] == 'define_var':
                            _, p_name, p_type = class_stmt
                            new_instance.fields[p_name] = 0 if p_type == 'number' else ""
                            
                    current_context[var_name] = new_instance
                else:
                    self.output_buffer.append(f"Error: No se puede instanciar '{var_name}' porque su tipo no corresponde a una clase definida.")
                    
            elif stmt_type == 'ask_method':
                self.execute_method_call(stmt, user_inputs, current_context)
                    
            elif stmt_type == 'say':
                expr_list = stmt[1]
                val_strs = [str(self.evaluate_expression(e, current_context)) for e in expr_list]
                self.output_buffer.append("".join(val_strs))
                    
            elif stmt_type == 'read':
                var_name = stmt[1]
                if var_name in user_inputs:
                    val = user_inputs[var_name]
                    if isinstance(val, str):
                        val_clean = val.strip()
                        if val_clean.isdigit(): val = int(val_clean)
                        else:
                            try: val = float(val_clean)
                            except ValueError: pass
                    current_context[var_name] = val
                else:
                    return {
                        'status': 'awaiting_input',
                        'variable': var_name,
                        'output': "\n".join(self.output_buffer)
                    }
                    
            elif stmt_type == 'assign':
                var_name = stmt[1]
                current_context[var_name] = self.evaluate_expression(stmt[2], current_context)
                    
            elif stmt_type == 'if_block':
                _, cond, if_statements, else_statements = stmt
                # Evaluamos la condición relacional (ej: numero == 0)
                if self.evaluate_condition(cond, current_context):
                    res = self.run_statements(if_statements, user_inputs, current_context)
                    if res and res.get('status') == 'awaiting_input': return res
                else:
                    # Si hay un bloque else, lo ejecutamos
                    if else_statements:
                        res = self.run_statements(else_statements, user_inputs, current_context)
                        if res and res.get('status') == 'awaiting_input': return res

            elif stmt_type == 'else_block':
                _, else_statements = stmt
                # Si el IF inmediato anterior fue falso, se ejecuta este bloque
                if hasattr(self, 'last_if_condition') and not self.last_if_condition:
                    res = self.run_statements(else_statements, user_inputs, current_context)
                    if res and res.get('status') == 'awaiting_input': return res
        return {
            'status': 'completed',
            'output': "\n".join(self.output_buffer)
        }