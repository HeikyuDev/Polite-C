# polite-c/compiler/views.py

from django.shortcuts import render
from django.http import JsonResponse
from utils.lexer import PoliteInterpreter

def ide_home(request):
    # Carga la página principal del IDE
    return render(request, 'compiler/index.html')

def run_code(request):
    if request.method == 'POST':
        source_code = request.POST.get('code', '')
        
        # Instanciamos nuestro mini motor de Polite C
        interpreter = PoliteInterpreter()
        console_result = interpreter.execute(source_code)
        
        # Devolvemos el resultado en formato JSON para que la página no tenga que recargarse
        return JsonResponse({
            'success': True,
            'output': "\n".join(console_result)
        })
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=400)