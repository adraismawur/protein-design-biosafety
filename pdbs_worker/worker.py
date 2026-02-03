from datetime import datetime
import json
from sqlite3 import connect
from time import sleep
from pathlib import Path

from params import validate_parameters
from config import Config
from constants import STATE_QUEUED, STATE_RUNNING, STATE_FAILED
from proteindj import run_proteindj


def main():
    db_path = Path(Config.DB_PATH).expanduser()
    print(f"Using db file: {db_path.absolute()}")
    db = connect(db_path)

    while True:
        sleep(1)

        r = db.execute(
            "SELECT * FROM jobs WHERE state = ? LIMIT 1",
            (STATE_QUEUED,),
        )

        job = r.fetchone()

        if job is None:
            continue

        job_id = job[0]

        r = db.execute("SELECT * FROM job_params WHERE id = ?", (job_id,))

        # skip id. TODO: replace with more generic solution
        job_params = r.fetchone()[1]

        if job_params is None:
            r = db.execute(
                "UPDATE jobs SET state = ?, started_at = ?, completed_at = ?, info = ? WHERE id = ?",
                (
                    STATE_FAILED,
                    datetime.now(),
                    datetime.now(),
                    "No parameters provided",
                    job_id,
                ),
            )
            db.commit()
            continue

        db.execute(
            "UPDATE jobs SET state = ?, started_at = ?, info = ? WHERE id = ?",
            (
                STATE_RUNNING,
                datetime.now(),
                "Job accepted",
                job_id,
            ),
        )
        db.commit()

        print(job)
        print(job_params)

        params = json.loads(job_params)

        validation = validate_parameters(params)

        if not validation[0]:
            db.execute(
                "UPDATE jobs SET state = ?, completed_at = ?, info = ? WHERE id = ?",
                (
                    STATE_FAILED,
                    datetime.now(),
                    f"Validation failed: {validation[1]}",
                    job_id,
                ),
            )

        # handle file input
        if False:
            pass

        run_proteindj(db, params, job_id)


if __name__ == "__main__":
    main()
