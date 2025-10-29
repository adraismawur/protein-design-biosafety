import os
from flask import Flask, render_template


app = Flask(__name__)


class Config:
    SECRET_KEY = os.environ.get("PDBS_SECRET", "CHANGEME")


app.config.from_object(Config)


from pdbs_web import routes
