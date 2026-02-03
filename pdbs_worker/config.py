import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_PATH = os.environ.get("DB_PATH", "./pdbs.db")
    PROTEINDJ_PATH = os.environ.get("PROTEINDJ_PATH", "./proteindj")
    PROTEINDJ_IMAGE_PATH = os.environ.get(
        "PROTEINDJ_IMAGE_PATH", "./proteindj/apptainer"
    )
    PROTEINDJ_CPUS = os.environ.get("PROTEINDJ_CPUS", str(os.cpu_count()))
    OUTPUT_BASE_PATH = os.environ.get("OUTPUT_BASE_PATH", "./pdj_output")
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "./upload")
