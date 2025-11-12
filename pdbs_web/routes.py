from pathlib import Path
from flask import g, render_template, request, redirect, url_for
from pdbs_web import app, get_db
from pdbs_web.forms.submission import RunParameterForm
from uuid import uuid4
from datetime import datetime, timedelta


@app.route("/", methods=["GET", "POST"])
def index():
    form = RunParameterForm(request.form)

    if request.method == "POST":
        guid = uuid4()

        db = get_db()
        db.execute("INSERT INTO jobs (id) VALUES (?)", (str(guid),))
        db.execute(
            "INSERT INTO job_params VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                str(guid),
                request.values["mandatory_parameters-rfd_mode"],
                request.values["mandatory_parameters-rfd_num_designs"],
                request.values["mandatory_parameters-seqs_per_design"],
                request.values["filtering_parameters-rfd_min_helices"],
                request.values["filtering_parameters-rfd_max_helices"],
                request.values["filtering_parameters-rfd_min_strands"],
                request.values["filtering_parameters-rfd_max_strands"],
                request.values["filtering_parameters-rfd_min_ss"],
                request.values["filtering_parameters-rfd_max_ss"],
                request.values["filtering_parameters-rfd_min_rog"],
                request.values["filtering_parameters-rfd_max_rog"],
            ),
        )
        db.commit()

        return redirect(url_for("get_job", job_id=str(guid)))

    return render_template("/index.html", form=form)


state_map = {
    0: "submitted",
    1: "running",
    2: "failed",
    3: "completed",
}


@app.route("/<job_id>", methods=["GET"])
def get_job(job_id: str):
    db = get_db()

    r = db.execute(
        "SELECT state, queued_at, started_at FROM jobs WHERE id = ?", (job_id,)
    )

    job = r.fetchone()

    if job is None:
        return render_template("error.html", message="Job does not exist")

    job_state = job[0]
    job_queued_at = job[1]
    job_started_at = job[2]
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
    if job == None:
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
