# sistema_pln
Sistema de Análisis de Lenguaje Natural (PLN)

Este proyecto es una aplicación web construida con el framework Django de Python, diseñada para realizar tareas básicas de Procesamiento de Lenguaje Natural (PLN) sobre archivos de texto.

Características Principales

Subida de Archivos: Permite a los usuarios cargar archivos de texto (.txt).

Análisis de Texto:

Generación de histogramas de palabras.

Conversión de texto a mayúsculas y minúsculas.

Normalización del texto: limpieza de caracteres especiales y eliminación de "stopwords" (palabras comunes como "el", "la", "de", etc.).

N-gramas: Cálculo y visualización de la frecuencia de n-gramas (secuencias de palabras) de tamaño configurable.

Requisitos del Sistema

Asegúrate de tener instalado Python 3.8 o superior en tu sistema.

Verificar la versión de Python:

python --version


o

python3 --version


Configuración e Instalación

Sigue estos pasos para poner en marcha el proyecto en un entorno local, independientemente del sistema operativo.

Paso 1: Clonar el Repositorio

Abre tu terminal o línea de comandos, navega hasta el directorio donde deseas guardar el proyecto y clona el repositorio desde GitHub:

git clone [https://github.com/luis7-9/sistema-pln.git](https://github.com/luis7-9/sistema-pln.git)


Paso 2: Navegar al Directorio del Proyecto

Ingresa al directorio del proyecto que acabas de clonar:

cd sistema-pln


Paso 3: Crear un Entorno Virtual

Es una buena práctica trabajar en un entorno virtual para aislar las dependencias del proyecto y evitar conflictos con otros proyectos de Python.

Crear el entorno virtual:

python -m venv venv


Esto creará un directorio llamado venv que contiene la instalación de Python y las herramientas necesarias.

Paso 4: Activar el Entorno Virtual

En sistemas basados en Linux/macOS:

source venv/bin/activate


En sistemas basados en Windows:

venv\Scripts\activate


Una vez activado, verás (venv) al inicio de tu línea de comandos, lo que indica que estás trabajando dentro del entorno virtual.

Paso 5: Instalar las Dependencias

El proyecto utiliza Django. Debes instalarlo usando pip, el gestor de paquetes de Python.

pip install Django


Paso 6: Ejecutar las Migraciones de la Base de Datos

Django usa migraciones para gestionar la estructura de la base de datos. Debes aplicarlas para crear las tablas necesarias (por ejemplo, la tabla para los archivos subidos).

python manage.py makemigrations analisis
python manage.py migrate


Paso 7: Iniciar el Servidor de Desarrollo

Finalmente, puedes iniciar el servidor de desarrollo local de Django.

python manage.py runserver


Verás un mensaje en la terminal que indica que el servidor se está ejecutando. Abre tu navegador y navega a http://127.0.0.1:8000/ para ver la aplicación en funcionamiento.

Paso 8: Crear un Usuario Administrador (Opcional)

Si deseas acceder al panel de administración de Django, puedes crear un superusuario:

python manage.py createsuperuser


Sigue las instrucciones en pantalla para crear el usuario. Luego, accede al panel de administración en http://127.0.0.1:8000/admin/ con las credenciales que creaste.