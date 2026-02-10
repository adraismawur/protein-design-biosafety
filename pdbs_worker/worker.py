from datetime import datetime
import json
from sqlite3 import connect
from time import sleep
from pathlib import Path

from params import REQUIRE_FILES
from config import Config
from constants import STATE_QUEUED, STATE_RUNNING, STATE_FAILED
from blast import BlastService
from proteindj import run_proteindj


def fail_job(db, job_id, reason):
    db.execute(
        "UPDATE jobs SET state = ?, started_at = ?, completed_at = ?, info = ? WHERE id = ?",
        (
            STATE_FAILED,
            datetime.now(),
            datetime.now(),
            reason,
            job_id,
        ),
    )
    db.commit()


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

        params = json.loads(job_params)

        # validation = validate_parameters(params)

        # if not validation[0]:
        #     db.execute(
        #         "UPDATE jobs SET state = ?, completed_at = ?, info = ? WHERE id = ?",
        #         (
        #             STATE_FAILED,
        #             datetime.now(),
        #             f"Validation failed: {validation[1]}",
        #             job_id,
        #         ),
        #     )
        #     db.commit()
        #     continue

        # file pre-processing and filtering
        if params["design_mode"] in REQUIRE_FILES:
            filter_result = BlastService.filter_input(job_id)

            if not filter_result[0]:
                fail_job(
                    db,
                    job_id,
                    filter_result[1],
                )
                continue

        run_proteindj(db, params, job_id)


if __name__ == "__main__":
    main()
