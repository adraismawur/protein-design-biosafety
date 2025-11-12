from datetime import datetime
import os
from sqlite3 import connect
from time import sleep
from subprocess import run
from pathlib import Path

STATE_QUEUED = 0
STATE_RUNNING = 1
STATE_FAILED = 2
STATE_DONE = 3


class Config:
    DB_PATH = os.environ.get("DB_PATH", "./pdbs.db")
    PROTEINDJ_PATH = os.environ.get("PROTEINDJ_PATH", "/proteindj")
    PROTEINDJ_IMAGE_PATH = os.environ.get(
        "PROTEINDJ_IMAGE_PATH", "/proteindj/apptainer"
    )
    PROTEINDJ_CPUS = os.environ.get("PROTEINDJ_CPUS", str(os.cpu_count()))
    OUTPUT_BASE_PATH = os.environ.get("OUTPUT_BASE_PATH", "./pdj_output")


def main():
    db_path = Path(Config.DB_PATH).expanduser()
    print(f"Using db file: {db_path.absolute()}")
    db = connect(db_path)

    proteindj_path = Path(Config.PROTEINDJ_PATH).expanduser()
    print(f"proteindj source: {proteindj_path.absolute()}")
    proteindj_image_path = Path(Config.PROTEINDJ_IMAGE_PATH).expanduser()
    print(f"proteindj image path: {proteindj_image_path.absolute()}")

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
        job_params = r.fetchone()[1:]

        if job_params is None:
            r = db.execute(
                "UPDATE jobs SET state = ?, started_at = ?, completed_at = ? WHERE id = ?",
                (
                    STATE_FAILED,
                    datetime.now(),
                    datetime.now(),
                    job_id,
                ),
            )
            db.commit()
            continue

        db.execute(
            "UPDATE jobs SET state = ?, started_at = ? WHERE id = ?",
            (
                STATE_RUNNING,
                datetime.now(),
                job_id,
            ),
        )
        db.commit()

        print(job)
        print(job_params)

        proteindj_params = {}
        proteindj_param_names = [
            "--rfd_mode",
            "--rfd_num_designs",
            "--seqs_per_design",
            "--rfd_min_helices",
            "--rfd_max_helices",
            "--rfd_min_strands",
            "--rfd_max_strands",
            "--rfd_min_ss",
            "--rfd_max_ss",
            "--rfd_min_rog",
            "--rfd_max_rog",
        ]

        for i, pdj_param_name in enumerate(proteindj_param_names):
            proteindj_params[pdj_param_name] = job_params[i]

        nextflow_file_path = proteindj_path / "main.nf"

        # basics
        process_params = [
            "nextflow",
            "run",
            str(nextflow_file_path),
            "-with-apptainer",
            "rfdiffusion",
            "--nv",
            "--container_dir",
            str(proteindj_image_path),
            "--rfd_contigs",
            "[50-50]",
            "--cpus",
            Config.PROTEINDJ_CPUS,
        ]

        # actual process args
        for k, v in proteindj_params.items():
            process_params.append(k)
            process_params.append(str(v))

        # output
        output_path = Path(Config.OUTPUT_BASE_PATH) / job_id
        process_params.append("--out_dir")
        process_params.append(str(output_path))

        print(f"CMD: {' '.join(process_params)}")

        proc = run(process_params)

        if proc.returncode == 0:
            r = db.execute(
                "UPDATE jobs SET state = ?, completed_at = ? WHERE id = ?",
                (
                    STATE_DONE,
                    datetime.now(),
                    job_id,
                ),
            )
        else:
            r = db.execute(
                "UPDATE jobs SET state = ?, completed_at = ? WHERE id = ?",
                (
                    STATE_FAILED,
                    datetime.now(),
                    job_id,
                ),
            )
        db.commit()


if __name__ == "__main__":
    main()
