from pathlib import Path
from Bio import SeqIO

PDB_DOWNLOAD_ENDPOINT = "https://files.rcsb.org/download/"


def download_cif(accession, destination_path):
    pass


def convert_cif_pdb(cif_path: Path):

    output_file = cif_path.parent / (cif_path.name + ".pdb")

    SeqIO.convert(cif_path, "cif-atom", output_file, "cif-pdb")
