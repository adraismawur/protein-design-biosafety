from flask import render_template
from pdbs_web import app
from pdbs_web.forms.submission import RunParameterForm


@app.route("/")
def index():
    form = RunParameterForm()

    return render_template("/index.html", form=form)
