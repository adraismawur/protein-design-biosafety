import json
import os
from pathlib import Path
from flask import render_template, request, redirect, url_for
from pdbs_web import app, get_db
from pdbs_web.forms.submission import (
    MandatoryBinderDenovoForm,
    MandatoryMonomerDenovoForm,
    RunParameterForm,
)
from uuid import uuid4
from datetime import datetime


design_modes = {
    "monomer_denovo": MandatoryMonomerDenovoForm,
    "binder_denovo": MandatoryBinderDenovoForm,
}


@app.route("/", methods=["GET"])
def index_redirect():
    return redirect(url_for("index", design_mode="monomer_denovo"))


@app.route("/<design_mode>", methods=["GET", "POST"])
def index(design_mode: str):
    if not design_mode:
        redirect(url_for("index", design_mode=design_modes[0]))

    form = RunParameterForm(request.form)

    mandatory_form = design_modes[design_mode](request.form)

    if request.method == "POST":
        guid = uuid4()

        data = {}
        data["design_mode"] = design_mode
        data.update(mandatory_form.data)
        data.update(form.filtering_parameters.data)

        if mandatory_form.pdb_input:
            file_name = str(guid) + ".pdb"
            file_path = os.path.join(app.config.get("UPLOAD_FOLDER"), file_name)
            request.files[mandatory_form.pdb_input.user_file.name].save(file_path)

        db = get_db()
        db.execute("INSERT INTO jobs (id) VALUES (?)", (str(guid),))
        db.execute(
            "INSERT INTO job_params VALUES (?, ?)",
            (str(guid), json.dumps(data)),
        )
        db.commit()

        return redirect(url_for("get_job", job_id=str(guid)))

    return render_template(
        "/index.html",
        design_modes=design_modes,
        form=form,
        mandatory_form=mandatory_form,
        current_design_mode=design_mode,
        has_file=False,
    )


state_map = {
    0: "submitted",
    1: "running",
    2: "failed",
    3: "completed",
}


@app.route("/results/<job_id>", methods=["GET"])
def get_job(job_id: str):
    db = get_db()

    r = db.execute(
        "SELECT state, queued_at, started_at, info FROM jobs WHERE id = ?", (job_id,)
    )

    job = r.fetchone()

    if job is None:
        return render_template("error.html", message="Job does not exist")

    job_state = job[0]
    job_queued_at = job[1]
    job_started_at = job[2]
    job_info = job[3]
    job_time_elapsed = None

    if job_started_at:
        job_time_elapsed = datetime.now() - datetime.fromisoformat(job_started_at)

    r = db.execute("SELECT COUNT(*) FROM jobs WHERE state = 0")

    jobs_queued = r.fetchone()[0]

    if job_state == 3:
        return redirect(url_for("get_job_result", job_id=job_id))

    return render_template(
        "/job.html",
        job_state=job_state,
        job_state_text=state_map[job_state],
        job_queued_at=job_queued_at,
        job_started_at=job_started_at,
        job_time_elapsed=job_time_elapsed,
        job_info=job_info,
        jobs_queued=jobs_queued,
    )


@app.route("/results/<job_id>", methods=["GET"])
def get_job_result(job_id: str):
    output_path = Path(app.config.get("OUTPUT_BASE_PATH")) / job_id

    csv = output_path / "results" / "all_designs.csv"

    output_data = []
    with open(csv, "r") as csv_file:
        for line in csv_file:
            output_data.append(line.split(","))

    db = get_db()
    r = db.execute("SELECT started_at, completed_at FROM jobs WHERE id = ?", (job_id,))

    job = r.fetchone()
    if job is None:
        return render_template("error.html", message="Job does not exist")

    job_started = datetime.fromisoformat(job[0])
    job_completed = datetime.fromisoformat(job[1])
    job_duration = job_completed - job_started

    return render_template(
        "/results.html",
        job_id=job_id,
        job_started=job_started,
        job_completed=job_completed,
        job_duration=job_duration,
        summary=output_data,
    )
