import re

class PoliteLexer:
    @staticmethod
    def clean_line(raw_line):
        """Elimina espacios extra y comentarios de la línea."""
        line = raw_line.strip()
        # Remueve comentarios !comment: "..."
        line = re.sub(r'!comment:\s*".*?"', '', line).strip()
        return line

    @staticmethod
    def parse_declaration(line):
        """
        Detecta si una línea es una declaración de variable dentro de please define:(
        Ejemplo: numero -> as number
        Devuelve: ('numero', 'number') o None
        """
        match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*->\s*as\s*(number|floatnumber|word)$', line)
        if match:
            return match.group(1), match.group(2)
        return None