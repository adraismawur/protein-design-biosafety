import json
import os
from pathlib import Path
import subprocess

from config import Config
from Bio import SeqIO, Blast
from datetime import datetime

Blast.email = "arjan.draisma@wur.nl"


class BlastService:
    class Constants:
        METHOD = "blastp"

    last_contact = datetime.now()
    last_RID_request = datetime.now()

    blacklisted_organisms = set()

    with open(Path(Config.ORGANISM_BLACKLIST_FILE)) as f:
        blacklisted_organisms.update(map(int, f.readlines()))

    def filter_input(job_id) -> tuple[bool, str]:
        job_folder = Path(os.path.join(Config.UPLOAD_FOLDER, job_id))
        file_path = Path(os.path.join(job_folder, job_id + ".pdb"))

        if not file_path.exists():
            return False, "Input PDB does not exist"

        records = SeqIO.parse(file_path, "pdb-atom")

        fasta = []

        unique_seqs = set()

        for record in records:
            if str(record.seq) in unique_seqs:
                continue
            unique_seqs.add(str(record.seq))
            fasta.append(f"> {record.id}\n")
            fasta.append(str(record.seq) + "\n")

        fasta_file = job_folder / (job_id + ".fa")

        with open(fasta_file, "w") as f:
            f.writelines(fasta)

        blast_db = Config.BLAST_DB_NAME
        blast_output_file = job_folder / (job_id + ".json")

        command = [
            "blastp",
            "-db",
            blast_db,
            "-query",
            str(fasta_file),
            "-out",
            str(blast_output_file),
            "-outfmt",
            "15",  # json
        ]

        output = subprocess.run(command)

        if output.returncode != 0:
            return False, "Could not run blast"

        with open(blast_output_file, "r") as output_json:
            data = json.loads(output_json.read())

            if "BlastOutput2" not in data:
                return False, "Could not parse blast output"

            for blast_output in data["BlastOutput2"]:
                if "report" not in blast_output:
                    continue

                report = blast_output["report"]

                if "results" not in report:
                    continue

                results = blast_output["report"]["results"]

                if "search" not in results:
                    continue

                search = blast_output["report"]["results"]["search"]

                # I'm having fun. Are you having fun?

                if "hits" not in search:
                    continue

                hits = blast_output["report"]["results"]["search"]["hits"]

                for hit in hits:
                    if "description" not in hit:
                        continue

                    for description in hit["description"]:
                        if "taxid" not in description:
                            continue

                        if description["taxid"] in BlastService.blacklisted_organisms:
                            organism = (
                                description["sciname"]
                                if "sciname" in description
                                else "Unknown"
                            )

                            return (
                                False,
                                f"Blast search detected blacklisted organism peptide in input: {organism}",
                            )

        return True, None
