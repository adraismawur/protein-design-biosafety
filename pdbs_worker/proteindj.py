from datetime import datetime
from subprocess import PIPE, run
from pathlib import Path

from config import Config
from params import generate_cmd_params
from constants import STATE_FAILED, STATE_DONE


def run_proteindj(
    db,
    params,
    job_id,
):
    proteindj_path = Path(Config.PROTEINDJ_PATH).expanduser()
    print(f"proteindj source: {proteindj_path.absolute()}")
    proteindj_image_path = Path(Config.PROTEINDJ_IMAGE_PATH).expanduser()
    print(f"proteindj image path: {proteindj_image_path.absolute()}")

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
    process_params.extend(generate_cmd_params(params))

    # output
    output_path = Path(Config.OUTPUT_BASE_PATH) / job_id
    process_params.append("--out_dir")
    process_params.append(str(output_path))

    print(f"CMD: {' '.join(process_params)}")

    proc = run(process_params, text=True, stdout=PIPE, stderr=PIPE)

    if proc.returncode == 0:
        db.execute(
            "UPDATE jobs SET state = ?, completed_at = ?, info = ? WHERE id = ?",
            (
                STATE_DONE,
                datetime.now(),
                "Job completed",
                job_id,
            ),
        )
    else:
        # try and figure out a reason. Nextflow is kind of weird so we have to dig through stdout/stderr
        # for specific errors.
        reason = ""

        for line in proc.stdout.split("\n"):
            if "Process requirement exceeds available memory" in line:
                reason = "Worker machine has insufficient memory."
                break

        db.execute(
            "UPDATE jobs SET state = ?, completed_at = ?, info = ? WHERE id = ?",
            (
                STATE_FAILED,
                datetime.now(),
                f"ProteinDJ run failed: {reason}",
                job_id,
            ),
        )
    db.commit()
