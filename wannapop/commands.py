import click
from flask.cli import AppGroup
from os import path
from sqlalchemyseed import load_entities_from_json, Seeder
from . import db_manager as db

basedir = path.abspath(path.dirname(__file__))

db_cli = AppGroup('db')

@db_cli.command('seed')
@click.argument('seeder')
# Command example:
# flask db seed category
def seed(seeder):
    seeders = ["category", "status"]
    if seeder in seeders:
        db_seed(seeder)
    else:
        print("Unknown seeder")

def db_seed(seeder):
    filepath = path.join(basedir, "seeders", seeder + ".json")
    # load entities
    entities = load_entities_from_json(filepath)
    # Initializing Seeder
    seeder = Seeder(db.session)
    # Seeding
    seeder.seed(entities)
    # Committing
    seeder.session.commit()
