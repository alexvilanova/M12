# 2daw-m12-p1-s0-solution

Proposta de solució de l'sprint 0 del projecte 1 dins del mòdul de projecte (M12) de 2n de DAW.

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

La base de dades [SQLite](https://www.sqlite.org) s'ha de dir `database.db`. S'ha creat amb l'script [database.sql](./database.sql).

## Run des de terminal

Executa:

    flask --debug run

I obre un navegador a l'adreça: [http://127.0.0.1:5000](http://127.0.0.1:5000).

Aquesta comanda executa el codi de `wsgi.py` 

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
