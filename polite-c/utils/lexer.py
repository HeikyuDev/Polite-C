import ply.lex as lex

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
}

tokens = [
    'ID', 'COLON', 'WORD_LITERAL', 'NUMBER_LITERAL', 'EXCLAMATION',
    'INDENT', 'DEDENT', 'NEWLINE'
] + list(reserved.values())

t_COLON = r':'
t_EXCLAMATION = r'!'
t_WORD_LITERAL = r'\"([^\\\"]|\\.)*\"'
t_NUMBER_LITERAL = r'\d+'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_COMMENT(t):
    r'!comment:\s*\"([^\\\"]|\\.)*\"'
    pass

# Consumimos los saltos de línea de forma segura en el lexer base incrementando el contador
def t_BASE_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t\r' # Agregamos \r por si ejecutan desde Windows

class IndentLexer(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.token_queue = []
        self.indents = [0]

    def input(self, data):
        self.token_queue = []
        self.indents = [0]
        
        # Procesamos todo el bloque de datos de forma nativa y continua
        self.lexer.input(data)
        self.lexer.lineno = 1
        
        tokens_list = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            tokens_list.append(tok)
            
        lines = data.split('\n')
        token_idx = 0
        
        # Mapeo y reconstrucción controlada de bloques lógicos
        for idx, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith('!comment:'):
                continue
                
            indent_pos = len(line) - len(line.lstrip())
            
            # Agrupamos los tokens pertenecientes de forma estricta a esta línea
            line_tokens = []
            while token_idx < len(tokens_list) and tokens_list[token_idx].lineno == idx:
                line_tokens.append(tokens_list[token_idx])
                token_idx += 1
                
            if not line_tokens:
                continue
                
            # Gestión limpia de la pila de indentación sin romper el buffer
            if indent_pos > self.indents[-1]:
                self.indents.append(indent_pos)
                indent_tok = lex.LexToken()
                indent_tok.type = 'INDENT'
                indent_tok.value = indent_pos
                indent_tok.lineno = idx
                indent_tok.lexpos = line_tokens[0].lexpos
                self.token_queue.append(indent_tok)
            elif indent_pos < self.indents[-1]:
                while indent_pos < self.indents[-1]:
                    self.indents.pop()
                    dedent_tok = lex.LexToken()
                    dedent_tok.type = 'DEDENT'
                    dedent_tok.value = indent_pos
                    dedent_tok.lineno = idx
                    dedent_tok.lexpos = line_tokens[0].lexpos
                    self.token_queue.append(dedent_tok)
                    
            self.token_queue.extend(line_tokens)
            
            # Inyección explícita y segura del NEWLINE sintáctico que Yacc espera
            nl_tok = lex.LexToken()
            nl_tok.type = 'NEWLINE'
            nl_tok.value = '\n'
            nl_tok.lineno = idx
            nl_tok.lexpos = line_tokens[-1].lexpos
            self.token_queue.append(nl_tok)
            
        # Cierre definitivo de bloques huérfanos
        while len(self.indents) > 1:
            self.indents.pop()
            end_dedent = lex.LexToken()
            end_dedent.type = 'DEDENT'
            end_dedent.value = 0
            end_dedent.lineno = len(lines)
            end_dedent.lexpos = 0
            self.token_queue.append(end_dedent)

    def token(self):
        if self.token_queue:
            return self.token_queue.pop(0)
        return None

lexer_errors = []
def t_error(t):
    # Ahora t.value[0] mostrará correctamente caracteres inválidos reales, no los saltos de línea internos
    lexer_errors.append(f"Mala educación léxica: Carácter inválido '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)

def get_lexer():
    global lexer_errors
    lexer_errors = []
    base_lexer = lex.lex(optimize=False, debug=False)
    return IndentLexer(base_lexer)