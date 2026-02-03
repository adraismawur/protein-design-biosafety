import os
from sqlite3 import connect
from flask import Flask, g
from pathlib import Path


class Config:
    DB_PATH = os.environ.get("DB_PATH", "./pdbs.db")
    OUTPUT_BASE_PATH = os.environ.get("OUTPUT_BASE_PATH", "./pdj_output")
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "./upload")


app = Flask(__name__)


app.config.from_object(Config)


def get_db():
    if "db" not in g:
        db = connect(Config.DB_PATH)

        p = Path(__file__).parent

        print(p)

        with open(p / "db_schema.sql", "r") as schema:
            schema = schema.read()
            print(schema)
            db.cursor().executescript(schema)
            db.commit()

        g.db = db

    return g.db


from pdbs_web import routes
