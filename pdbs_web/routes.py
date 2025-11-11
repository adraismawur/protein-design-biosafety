from flask import render_template, request, redirect, url_for
from pdbs_web import app, get_db
from pdbs_web.forms.submission import RunParameterForm
from uuid import uuid4
from sqlite3 import Connection

@app.route("/", methods=["GET", "POST"])
def index():
    form = RunParameterForm(request.form)

    if request.method == "POST":
        guid = uuid4()

        data = request.form

        db = get_db()
        db.execute("INSERT INTO jobs (id) VALUES (?)", (str(guid),))
        db.execute(
            "INSERT INTO job_details VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                guid,
                data["rfd_mode"],
                data["rfd_num_designs"],
                data["seqs_per_design"],
                data["rfd_min_helices"],
                data["rfd_max_helices"],
                data["rfd_min_strands"],
                data["rfd_max_strands"],
                data["rfd_min_ss"],
                data["rfd_max_ss"],
                data["rfd_min_rog"],
                data["rfd_max_rog"],),
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

    r = db.execute("SELECT state FROM jobs WHERE id = ?", (job_id,))

    job_state = r.fetchone()[0]

    r = db.execute("SELECT COUNT(*) FROM jobs WHERE state = 0")

    jobs_queued = r.fetchone()[0]

    return render_template("/job.html", job_state=state_map[job_state], jobs_queued=jobs_queued)
