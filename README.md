# Django-cheems

## Preparar el proyecto en Visual Studio Code (Windows)

Abre en VS Code la carpeta raíz del repositorio, donde están `manage.py` y
`requirements.txt`. En una terminal PowerShell integrada, crea y activa el
entorno virtual:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Si PowerShell bloquea la activación, permite scripts solo en la terminal actual
y vuelve a activarlo:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

En VS Code, selecciona el intérprete `.\venv\Scripts\python.exe` con
**Python: Select Interpreter**. Después crea tu configuración local a partir de
la plantilla:

```powershell
Copy-Item .env.example .env
```

Edita `.env` en la raíz del repositorio. Cambia `SECRET_KEY` por una clave
aleatoria (puedes generarla con
`python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
y configura estos valores con los datos de tu servidor MySQL:

| Variable | Valor |
| --- | --- |
| `DB_NAME` | Nombre de la base de datos que ya existe en MySQL |
| `DB_USER` | Usuario MySQL con permisos sobre esa base |
| `DB_PASSWORD` | Contraseña de ese usuario |
| `DB_HOST` | `127.0.0.1` si MySQL está en tu equipo; de lo contrario, el host del servidor |
| `DB_PORT` | Puerto MySQL, normalmente `3306` |
| `DB_SSL_CA` | Ruta al certificado CA si el proveedor MySQL remoto exige TLS; déjala vacía para MySQL local |

No guardes ni compartas el archivo `.env`: está excluido de Git. `.env.example`
es solo una plantilla y no debe contener credenciales reales.

Inicia Django desde la misma terminal con el entorno activo:

```powershell
python manage.py check
python manage.py runserver
```

Abre `http://127.0.0.1:8000/` en el navegador.

## Adaptar el esquema MySQL a la aplicación

La conexión se configura en **`.env`**; normalmente no hace falta cambiar
carpetas. `django_cheems/settings.py` lee esas variables y selecciona el
backend MySQL. Si cambian los datos de conexión, modifica `.env`, no las
credenciales directamente en el código.

La vista de inicio (`hello/views.py`) llama a `User.get_all()` en
`hello/entities/user.py`, que consulta la tabla `user`. La aplicación espera
que esa tabla tenga `id`, `name`, `account`, `password` y `profile`; los valores
de `profile` deben ser compatibles con `1` (administrador) o `2` (operador),
definidos en `hello/enums/profile.py`. Si tu tabla o columnas tienen otros
nombres, adapta las consultas y el mapeo en `hello/entities/user.py`.

Para una base remota que requiere TLS, coloca el certificado CA en el proyecto
o configura `DB_SSL_CA` con su ruta en `.env`. La plantilla deja esta variable
vacía para usar MySQL local sin certificado.

`hello/models.py` está vacío y las órdenes de trabajo aún no se guardan: la
aplicación no define modelos Django para crear automáticamente sus tablas de
negocio. Si quieres que Django administre tu esquema, define los modelos en
`hello/models.py`, crea migraciones y verifica que correspondan al esquema
existente antes de aplicarlas. `python manage.py migrate` crea las tablas
internas de Django, pero no crea la tabla `user` que consulta esta aplicación.
No ejecutes migraciones contra una base con datos importantes sin revisar antes
el plan y hacer un respaldo.
