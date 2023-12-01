# 2daw-m12-p1-solution

Proposta de solució del projecte 1 dins del mòdul de projecte (M12) de 2n de DAW.

## Setup

### Python Virtual Environment

Crea l'entorn:

    python3 -m venv .venv

Activa'l:

    source .venv/bin/activate

Instal·la el requisits:

    pip install -r requirements.txt

Per a generar el fitxer de requiriments:

    pip freeze > requirements.txt

Per desactivar l'entorn:

    deactivate

### Base de dades

Crea una base de dades SQLite a partir de l'script [0_tables.sql](./sqlite/0_tables.sql). Tens una d'exemple creada amb les dades del fitxer [1_mock_data.sql](./sqlite/1_mock_data.sql). Hi ha tres usuaris de prova (un `admin` i dos `wanner`) i tots tres tenen com a contrasenya `patata`.

### Fitxer de configuració

Crea un fitxer `.env` amb els paràmetres de configuració. Pots fer servir el fitxer [.env.exemple](./.env.exemple).

## Run des de terminal

Executa:

    flask --debug run

I obre un navegador a l'adreça: [http://127.0.0.1:5000](http://127.0.0.1:5000).

Aquesta comanda executa el codi de [wsgi.py](./wsgi.py).

Per autenticarte, consula al fitxer [database.sql](./sqlite/database.sql) els usuaris de prova disponibles.

## Debug amb Visual Code

Des de l'opció de `Run and Debug`, crea un fitxer anomenat `launch.json` amb el contingut següent:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "WANNAPOP",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "wsgi.py",
                "FLASK_DEBUG": "1"
            },
            "args": [
                "run",
                "--no-debugger",
                "--no-reload"
            ],
            "jinja": true,
            "justMyCode": true
        }
    ]
}
```
