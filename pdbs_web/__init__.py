import os
from sqlite3 import connect
from flask import Flask, g
from pathlib import Path


app = Flask(__name__)


class Config:
    SECRET_KEY = os.environ.get("PDBS_SECRET", "CHANGEME")
    DB_PATH = os.environ.get("DB_PATH", "./pdbs.db")


app.config.from_object(Config)

def get_db():
    if "db" not in g:
        db = connect(Config.DB_PATH)

        p = Path(__file__).parent

        with open(p / "db_schema.sql", "r") as schema:
            db.execute(schema.read())
            db.commit()
        
        g.db = db
    
    return g.db



from pdbs_web import routes
