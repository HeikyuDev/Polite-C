# polite-c/utils/lexer.py

class PoliteInterpreter:
    def __init__(self):
        self.output_buffer = []  # Aquí guardamos lo que el compilador debe "decir"
        self.variables = {}      # Memoria del programa para guardar variables a futuro

    def execute(self, source_code):
        self.output_buffer = [] # Limpiar consola anterior
        lines = source_code.split('\n')
        
        in_main_block = False
        
        for line_num, raw_line in enumerate(lines, 1):
            line = raw_line.strip()
            
            # 1. Ignorar líneas vacías o comentarios
            if not line or line.startswith('!comment:'):
                continue
            
            # 2. Detectar inicio del programa
            if line == "hello main! please do this:":
                in_main_block = True
                continue
                
            # 3. Detectar fin del programa
            if line == "thanks!":
                if not in_main_block:
                    self.output_buffer.append(f"Error (Línea {line_num}): Se agradeció con 'thanks!' pero nunca se saludó al main.")
                in_main_block = False
                break
                
            # 4. Procesar instrucciones dentro del bloque ejecutable
            if in_main_block:
                # Procesar comando 'please say:'
                if line.startswith("please say:"):
                    # Extraer el contenido quitando la palabra clave
                    content = line.replace("please say:", "").strip()
                    # Quitar comillas si es un texto plano
                    if content.startswith('"') and content.endswith('"'):
                        content = content[1:-1]
                    
                    self.output_buffer.append(content)
                else:
                    self.output_buffer.append(f"Error de Sintaxis (Línea {line_num}): No entendí la petición '{line}'. ¿Fuiste lo suficientemente educado?")
        
        # Validación de cierre de seguridad
        if in_main_block:
            self.output_buffer.append("Error de mala educación: El programa principal comenzó pero olvidaste despedirte con 'thanks!' al final.")
            
        return self.output_buffer