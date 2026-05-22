````md
# Polite C Compiler

Polite C Compiler es una aplicación web desarrollada con Django para interpretar y analizar código escrito en **Polite C**, un mini-lenguaje de programación orientado a objetos con sintaxis conversacional.

El objetivo del proyecto es simular el funcionamiento básico de un compilador, donde el cliente envía una cadena de caracteres que representa el código fuente escrito por el usuario, y el servidor se encarga de procesarla mediante un analizador léxico y, posteriormente, un analizador sintáctico.

## Descripción del proyecto

Polite C es un mini-lenguaje diseñado con fines educativos. Su sintaxis está inspirada en lenguajes como C y Java, pero reemplaza parte de la simbología tradicional por expresiones más legibles y conversacionales.

Ejemplo de código Polite C:

```txt
Class GeneradorDeMensajes please do this
    please define numero as number

    procesarDato receives () please do this
        please say "Ingrese un número por teclado"
        please read numero

        if this happens (numero == 0) please do this
            please say "Error, el número no puede ser cero"
        if not please do this
            please say "El número ingresado es válido"
        finish
    finish
finish

hello main! please do this
    please create miGenerador as GeneradorDeMensajes
    please ask miGenerador to procesarDato
thanks!
````

## Funcionalidades principales

* Recepción de código fuente Polite C desde el cliente.
* Procesamiento del código en el servidor.
* Identificación de tokens mediante un analizador léxico.
* Preparación para análisis sintáctico mediante una gramática libre de contexto.
* Separación del proyecto en capas para facilitar el mantenimiento.
* Base para construir una interfaz tipo mini IDE.

## Tecnologías utilizadas

* Python
* Django
* HTML
* CSS
* JavaScript

## Estructura sugerida del proyecto

```txt
polite-c/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── compiler/
│   ├── lexer/
│   │   ├── __init__.py
│   │   ├── token.py
│   │   └── lexer.py
│   │
│   ├── parser/
│   │   ├── __init__.py
│   │   └── parser.py
│   │
│   ├── services/
│   │   └── compiler_service.py
│   │
│   ├── views.py
│   ├── urls.py
│   └── tests.py
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/HeikyuDev/Polite-C
cd polite-c
```

### 2. Crear el entorno virtual

En Windows:

```bash
python -m venv venv
```

### 3. Activar el entorno virtual

En PowerShell:

```bash
.\venv\Scripts\Activate.ps1
```

En CMD:

```bash
venv\Scripts\activate
```

En Linux o macOS:

```bash
source venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

Si todavía no existe el archivo `requirements.txt`, se puede generar con:

```bash
pip freeze > requirements.txt
```

### 5. Ejecutar migraciones

```bash
python manage.py migrate
```

### 6. Iniciar el servidor

```bash
python manage.py runserver
```

Luego abrir en el navegador:

```txt
http://127.0.0.1:8000/
```

## Entorno virtual y Git

La carpeta del entorno virtual no debe subirse al repositorio. Por eso debe estar incluida en el archivo `.gitignore`.

Ejemplo:

```gitignore
venv/
.venv/
env/
__pycache__/
*.py[cod]
db.sqlite3
.env
```

## Flujo general de funcionamiento

```txt
Cliente web
    ↓
Envía código fuente como cadena de caracteres
    ↓
Servidor Django
    ↓
Analizador léxico
    ↓
Lista de tokens
    ↓
Analizador sintáctico
    ↓
Resultado del análisis o mensajes de error
```

## Objetivo académico

Este proyecto forma parte del desarrollo de un mini-lenguaje orientado a objetos para aplicar conceptos de Teoría de la Computación, principalmente:

* definición de tokens;
* expresiones regulares;
* análisis léxico;
* autómatas finitos;
* gramáticas libres de contexto;
* análisis sintáctico.

## Estado del proyecto

Proyecto en desarrollo.

Actualmente se está preparando la base del servidor Django y la estructura necesaria para implementar el analizador léxico y el analizador sintáctico de Polite C.

## Autores

Grupo 04 - Teoría de la Computación
Universidad Nacional de Misiones

```

Hay una sola cosa que tenés que cambiar: donde dice `https://github.com/usuario/polite-c.git`, poné la URL real de tu repositorio.
```
