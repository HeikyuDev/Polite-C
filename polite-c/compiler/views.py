# polite-c/compiler/views.py

import json
from django.shortcuts import render
from django.http import JsonResponse
# Corregido: Agregamos el punto (.) porque utils está adentro de compiler
from .utils.interpreter import PoliteInterpreter 

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
<<<<<<< Updated upstream
        source_code = request.POST.get('code', '')
        raw_inputs = request.POST.get('inputs', '{}')
        
        try:
            user_inputs = json.loads(raw_inputs)
        except json.JSONDecodeError:
            user_inputs = {}
        
        interpreter = PoliteInterpreter()
        execution_result = interpreter.execute(source_code, user_inputs)
        
        return JsonResponse(execution_result)
=======
        try:
            source_code = request.POST.get('code', '')
            raw_inputs = request.POST.get('inputs', '{}')
            
            try:
                user_inputs = json.loads(raw_inputs)
            except json.JSONDecodeError:
                user_inputs = {}
            
            interpreter = PoliteInterpreter()
            execution_result = interpreter.execute(source_code, user_inputs)
            
            return JsonResponse(execution_result)
        except Exception as e:
            import traceback
            error_msg = f"Error en ejecución: {str(e)}\n{traceback.format_exc()}"
            return JsonResponse({
                'status': 'completed',
                'output': error_msg
            })
>>>>>>> Stashed changes
        
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=400)