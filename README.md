
## Setup

### Python Virtual Environment

Crear entorno:

    python3 -m venv .venv

Activarlo:

    source .venv/bin/activate

Instalar los requisitos:

    pip install -r requirements.txt

Para generar archivo con requisitos:

    pip freeze > requirements.txt

Para detener entorno:

    deactivate

### Configuración

Debes configurar el archivo .env con los datos solicitados

    cp .env-example .env

## Ejecutar desde terminal

Executa:

    flask --debug run

I obre un navegador a l'adreça: [http://127.0.0.1:5000](http://127.0.0.1:5000).

Aquesta comanda executa el codi de `wsgi.py` 

## Importar datos generados a BD

1. **Generar datos con Mockaroo:**

   - Ve a [Mockaroo](https://mockaroo.com/).
   - Crea un esquema de datos que coincida con la estructura de tu tabla de SQLite.
   - Genera datos de ejemplo y descárgalos en formato CSV.

2. **Abrir DB Browser for SQLite:**

   - Descarga e instala [DB Browser for SQLite](https://sqlitebrowser.org/) si aún no lo tienes.

3. **Importar datos de Mockaroo:**

   - Abre la base de datos existente
   - Selecciona la pestaña "File" en la parte superior izquierda.
   - Elige "Import" en el menú desplegable.
   - Selecciona el archivo CSV que descargaste de Mockaroo.
   - Configura las opciones de importación, como el nombre de la tabla de destino y las opciones de delimitador si es necesario.
   - Haz clic en "OK" para iniciar la importación.

