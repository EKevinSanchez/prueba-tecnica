
# Generación del entorno virtual y instalación de librerías
# Pasos para crear un entorno virtual y instalar las librerías necesarias
# 1. Crear un entorno virtual
python -m venv .venv
# 2. Activar el entorno virtual
# En Windows:
.\.venv\Scripts\activate
# En Linux o MacOS:
source .venv/bin/activate
# 3. Instalar las librerías necesarias
pip install -r requirements.txt
# 4. Desactivar el entorno virtual cuando hayas terminado de utilizar el proyecto
deactivate
# Ejecución del proyecto
# Para ejecutar el proyecto, asegúrate de que el entorno virtual esté activado y luego ejecuta:
python main.py
