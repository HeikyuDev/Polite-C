from ast import pattern
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
        Detecta declaraciones de variables.

        Ejemplos válidos:
            please define numero as number
            please define palabra as word

        Devuelve:
            ('numero', 'number')
            ('palabra', 'word')
            o None si no coincide.
        """
        VALID_TYPES = ["number", "floatnumber", "word"]

        pattern = rf'^please\s+define\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+as\s+({"|".join(VALID_TYPES)})$'

        match = re.match(pattern, line.strip())

        if match:
            return match.group(1), match.group(2)
        return None
    
    @staticmethod
    def parse_assignment(line):
            """
        Detecta asignaciones.
        Ejemplos:
            make num equals to 5
            make palabra equals to "hola"
        Devuelve:
            ('num', '5')
            ('palabra', '"hola"')
            o None
            """

            pattern = r'^make\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+equals\s+to\s+(.+)$'
            match = re.match(pattern, line.strip())

            if match:
                return match.group(1), match.group(2)

            return None
    