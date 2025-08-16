# Descripción del proyecto
- Consiste en resolver las peticiones de la interface "dislexiayconducta.com" para que el Servidor  regrese el resultado de uno y hasta tres tipos de diagnósticos formulados por el usuario desde la aplicación web antes mencionada.
La respuesta al usuario se hará mediante un correo electrónico que será remitido de manera inmediata. 

# Installation
1. Make a folder that has sense for the project: `mkdir diagnostics`
2. Change to the new dictory and clone the Git repository: `git clone git@github.com:dislexiayconducta/Diagnosticos.git`
3. Create virtual environment: `python -m venv env --prompt=dyc`
4. Once the virtual environment was created run the following command: `pip install -r requirements.txt`
5. At the end of the step 4, Create the database throught the mysql shell. 
6. Execute migrations: `python manage.py makemigrations`after that run: `python manage.py migrate`. If you prefer use the Makefile and run: `make mig`the latter command runs both makemigrations and migrate.
