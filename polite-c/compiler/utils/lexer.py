import ply.lex as lex

# Diccionario unificado de palabras reservadas estrictas de la Parte 1
reserved = {
    'hello': 'HELLO',
    'main': 'MAIN',
    'please': 'PLEASE',
    'do': 'DO',
    'this': 'THIS',
    'define': 'DEFINE',
    'as': 'AS',
    'number': 'TYPE_NUMBER',
    'floatnumber': 'TYPE_FLOAT',
    'word': 'TYPE_WORD',
    'say': 'SAY',
    'read': 'READ',
    'if': 'IF',
    'happens': 'HAPPENS',
    'not': 'NOT',
    'thanks': 'THANKS',
    'make': 'MAKE',
    'equals': 'EQUALS',
    'to': 'TO',
    'Class': 'CLASS',
    'class': 'CLASS',
    'finish': 'FINISH',
    'receives': 'RECEIVES',
    'recieves': 'RECEIVES',  # Soporte preventivo ante errores de tipeo
    'give': 'GIVE',
    'back': 'BACK',
    'create': 'CREATE',
    'ask': 'ASK',
    'with': 'WITH',
}

# Definición del catálogo general de tokens sintácticos
tokens = [
    'ID', 'WORD_LITERAL', 'NUMBER_LITERAL', 'FLOAT_LITERAL',
    'EXCLAMATION', 'LPAREN', 'RPAREN', 'COMMA', 'ASSIGN',
    'PLUS', 'MINUS', 'MULT', 'DIV', 'MOD',
    'EQ', 'NE', 'LT', 'GT', 'LE', 'GE'
] + list(set(reserved.values()))

# Expresiones regulares para símbolos y operadores permitidos
t_EXCLAMATION = r'!'
t_LPAREN      = r'\('
t_RPAREN      = r'\)'
t_COMMA       = r','
t_ASSIGN      = r'='
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

# Captura de cadenas de texto literales (entre comillas)
t_WORD_LITERAL = r'\"([^\\\"]|\\.)*\"'

# Reconocimiento y casteo dinámico de constantes numéricas
def t_FLOAT_LITERAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_NUMBER_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Reconocimiento de identificadores y mapeo de palabras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Ignorar comentarios estructurados !comment: "..."
def t_COMMENT(t):
    r'!comment:\s*\"([^\\\"]|\\.)*\"'
    pass

# Caracteres en blanco ignorados de manera continua por la RAM
t_ignore = ' \t\r'

# Contador nativo de líneas del sistema
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Gestión formal de errores léxicos de cortesía
lexer_errors = []
def t_error(t):
    lexer_errors.append(f"Mala educación léxica: Carácter inválido '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)

def get_lexer():
    global lexer_errors
    lexer_errors = []
    return lex.lex(optimize=False, debug=False)