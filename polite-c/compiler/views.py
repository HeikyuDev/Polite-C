# polite-c/compiler/views.py

import json
from django.shortcuts import render
from django.http import JsonResponse
from utils.interpreter import PoliteInterpreter

def ide_home(request):
    """
    Renderiza la interfaz principal del Mini IDE para el estudiante.
    """
    return render(request, 'index.html')

def run_code(request):
    """
    Procesa el código de Polite C de manera asíncrona.
    Soporta la pausa de ejecución cuando se requiere la entrada del usuario.
    """
    if request.method == 'POST':
        source_code = request.POST.get('code', '')
        raw_inputs = request.POST.get('inputs', '{}')
        
        # Convertimos la cadena JSON que envió el Frontend a un diccionario de Python
        try:
            user_inputs = json.loads(raw_inputs)
        except json.JSONDecodeError:
            user_inputs = {}
        
        # Instanciamos el intérprete
        interpreter = PoliteInterpreter()
        
        # Ejecutamos el código pasándole la memoria actual de inputs
        execution_result = interpreter.execute(source_code, user_inputs)
        
        # Retornamos el resultado del intérprete directamente al Frontend.
        # execution_result ya es un diccionario con la estructura:
        # { 'status': '...', 'output': '...', 'variable': '...' (opcional) }
        return JsonResponse(execution_result)
        
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=400)