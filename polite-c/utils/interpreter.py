from .lexer import PoliteLexer

class PoliteInterpreter:
    def __init__(self):
        self.output_buffer = []
        self.variables = {}  # Memoria del programa: { 'numero': 0, 'palabra': '' }

    def execute(self, source_code, user_inputs=None):
        """
        user_inputs: Un diccionario enviado por el frontend con las respuestas del usuario.
                     Ejemplo: { 'numero': '15' }
        """
        if user_inputs is None:
            user_inputs = {}
            
        lines = source_code.split('\n')
        in_main_block = False
        in_define_block = False
        
        for line_num, raw_line in enumerate(lines, 1):
            line = PoliteLexer.clean_line(raw_line)
            
            if not line:
                continue
            
            # Control de bloques principales
            if line == "hello main! please do this:":
                in_main_block = True
                continue
                
            if line == "thanks!":
                in_main_block = False
                break
                
            if in_main_block:

                # --- DECLARACIÓN DE VARIABLES ---
                # Valores por defecto para cada tipo
                DEFAULT_VALUES = {
                    "number": 0,
                    "floatnumber": 0.0,
                    "word": ""
                }
                decl = PoliteLexer.parse_declaration(line)

                if decl:
                    var_name, var_type = decl

                    # Evitar redeclaraciones
                    if var_name in self.variables:
                        self.output_buffer.append(
                            f"Error (Línea {line_num}): La variable '{var_name}' ya existe."
                        )
                        continue

                    # Inicialización según tipo
                    if var_type == 'number':
                        self.variables[var_name] = DEFAULT_VALUES[var_type]

                    elif var_type == 'floatnumber':
                        self.variables[var_name] = DEFAULT_VALUES[var_type]

                    elif var_type == 'word':
                        self.variables[var_name] = DEFAULT_VALUES[var_type]

                    continue

                # --- COMANDO DE ENTRADA (please read:) ---
                if line.startswith("please read:"):
                    var_name = line.replace("please read:", "").strip()
                    if var_name not in self.variables:
                        self.output_buffer.append(f"Error (Línea {line_num}): La variable '{var_name}' no ha sido definida.")
                        continue
                    
                    # Verificamos si ya tenemos el dato provisto por el usuario desde el frontend
                    if var_name in user_inputs:
                        # Asignamos el valor convirtiéndolo al tipo correcto
                        raw_val = user_inputs[var_name]
                        try:
                            # Aquí podríamos verificar el tipo real, simulamos una asignación básica
                            self.variables[var_name] = raw_val
                        except ValueError:
                            self.output_buffer.append(f"Error de Tipo (Línea {line_num}): El valor no coincide con el tipo de '{var_name}'.")
                    else:
                        # ¡PAUSA! No tenemos el dato. Le avisamos al frontend que requerimos input.
                        return {
                            'status': 'awaiting_input',
                            'variable': var_name,
                            'output': "\n".join(self.output_buffer)
                        }
                # --- ASIGNACIONES ---
                assign = PoliteLexer.parse_assignment(line)

                if assign:
                    var_name, raw_value = assign

                    # Verificar que exista la variable
                    if var_name not in self.variables:
                        self.output_buffer.append(
                            f"Error (Línea {line_num}): Variable '{var_name}' no definida."
                        )
                        continue

                    current_value = self.variables[var_name]

                    try:

                        # NUMBER
                        if isinstance(current_value, int):
                            self.variables[var_name] = int(raw_value)

                        # FLOAT
                        elif isinstance(current_value, float):
                            self.variables[var_name] = float(raw_value)

                        # WORD
                        elif isinstance(current_value, str):

                            # Validar comillas
                            if raw_value.startswith('"') and raw_value.endswith('"'):
                                self.variables[var_name] = raw_value[1:-1]
                            else:
                                self.output_buffer.append(
                                    f'Error (Línea {line_num}): Los textos deben ir entre comillas.'
                                )

                    except ValueError:
                        self.output_buffer.append(
                            f"Error (Línea {line_num}): Valor inválido para '{var_name}'."
                        )

                    continue

                # --- COMANDO DE SALIDA (please say:) CON SOPORTE PARA VARIABLES ---
                elif line.startswith("please say:"):
                    content = line.replace("please say:", "").strip()
                    
                    # Caso 1: Texto plano entre comillas
                    if content.startswith('"') and content.endswith('"'):
                        self.output_buffer.append(content[1:-1])
                    # Caso 2: Es una variable conocida en memoria
                    elif content in self.variables:
                        self.output_buffer.append(str(self.variables[content]))
                    else:
                        self.output_buffer.append(f"Error (Línea {line_num}): No puedo decir '{content}' porque no está entre comillas ni es una variable definida.")
                        
        return {
            'status': 'completed',
            'output': "\n".join(self.output_buffer)
        }