import ply.lex as lex

# Diccionario de palabras reservadas simples, con soporte para POO
reserved = {
    'as': 'AS',
    'number': 'TYPE_NUMBER',
    'floatnumber': 'TYPE_FLOAT',
    'word': 'TYPE_WORD',
    'Class': 'CLASS',
    'class': 'CLASS',
    'finish': 'FINISH',
    'receives': 'RECEIVES',
    'recieves': 'RECEIVES',
    'with': 'WITH',
    'to': 'TO',
    'make': 'MAKE',
    'equals': 'EQUALS',
    'please': 'PLEASE',
    'create': 'CREATE',
    'object': 'OBJECT',
    'ask': 'ASK'
}

# Catálogo general de tokens sintácticos
tokens = [
    'ID', 'WORD_LITERAL', 'NUMBER_LITERAL', 'FLOAT_LITERAL',
    'LPAREN', 'RPAREN', 'COMMA', 'ASSIGN', 'COLON',
    'PLUS', 'MINUS', 'MULT', 'DIV', 'MOD',
    'EQ', 'NE', 'LT', 'GT', 'LE', 'GE',
    'HELLO_MAIN', 'THANKS', 'PLEASE_DO_THIS', 'PLEASE_DEFINE',
    'PLEASE_SAY', 'PLEASE_READ', 'IF_HAPPENS', 'IF_NOT',
    'PLEASE_GIVE_BACK', 'PLEASE_CREATE', 'PLEASE_ASK', 'TO_GIVE'
] + list(set(reserved.values()))

# Expresiones regulares para los tokens compuestos prioritarios
def t_HELLO_MAIN(t):
    r'hello\s+main\s*!'
    return t

def t_THANKS(t):
    r'thanks\s*!'
    return t

def t_PLEASE_DO_THIS(t):
    r'please\s+do\s+this'
    return t

def t_PLEASE_DEFINE(t):
    r'please\s+define'
    return t

def t_PLEASE_SAY(t):
    r'please\s+say'
    return t

def t_PLEASE_READ(t):
    r'please\s+read'
    return t

def t_IF_HAPPENS(t):
    r'if\s+this\s+happens'
    return t

def t_IF_NOT(t):
    r'if\s+not'
    return t

def t_PLEASE_GIVE_BACK(t):
    r'please\s+give\s+back'
    return t

def t_PLEASE_CREATE(t):
    r'please\s+create'
    return t

def t_PLEASE_ASK(t):
    r'please\s+ask'
    return t

def t_TO_GIVE(t):
    r'to\s+give'
    return t

# Símbolos estándar
t_LPAREN      = r'\('
t_RPAREN      = r'\)'
t_COMMA       = r','
t_ASSIGN      = r'='
t_COLON       = r':'  # <-- Agregado componente físico para el separador de bloques
t_PLUS        = r'\+'
t_MINUS       = r'-'
t_MULT        = r'\*'
t_DIV         = r'/'
t_MOD         = r'%'
t_EQ          = r'=='
t_NE          = r'!='
t_LE          = r'<='
t_GE          = r'>='
t_LT          = r'<'
t_GT          = r'>'

t_WORD_LITERAL = r'\"([^\\\"]|\\.)*\"'

def t_FLOAT_LITERAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_NUMBER_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_COMMENT(t):
    r'!comment:?\s*\"([^\\\"]|\\.)*\"'
    pass

# Control centralizado de saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Estricto: Solo se ignoran espacios en blanco horizontales y retornos de carro
t_ignore = ' \t\r'

lexer_errors = []
def t_error(t):
    lexer_errors.append(f"Mala educación léxica: Carácter inválido '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)

def get_lexer():
    global lexer_errors
    lexer_errors = []
    return lex.lex(optimize=False, debug=False)