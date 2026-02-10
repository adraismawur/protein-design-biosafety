class PARAMETERS:
    class ESSENTIAL:
        DESIGN_MODE = "design_mode"
        NUM_DESIGNS = "num_designs"
        SEQS_PER_DESIGN = "seqs_per_design"
        OUT_DIR = "out_dir"

    class SPECIFIC:
        DESIGN_LENGTH = "design_length"
        INPUT_PDB = "input_pdb"
        HOTSPOT_RESIDUES = "hotspot_residues"
        RFD_CONTIGS = "rfd_contigs"
        RFD_SCAFFOLD_DIR = "rfd_scaffold_dir"
        RFD_MASK_LOOPS = "rfd_mask_loops"
        RFD_INPAINT_SEQ = "rfd_inpaint_seq"
        RFD_LENGTH = "rfd_length"
        RFD_PARTIAL_DIFFUSION_TIMESTEPS = "rfd_partial_diffusion_timesteps"


# parameter limits for integer parameters
PARAMETER_LIMITS = {
    "rfd_num_designs": (1, 10),
    "seqs_per_design": (1, 10),
}

# mandatory parameters per mode
MANDATORY_PARAMETERS = {
    "monomer_denovo": [
        PARAMETERS.SPECIFIC.DESIGN_LENGTH,
    ],
    "monomer_foldcond": [
        PARAMETERS.SPECIFIC.RFD_SCAFFOLD_DIR,
    ],
    "monomer_motifscaff": [
        PARAMETERS.SPECIFIC.INPUT_PDB,
        PARAMETERS.SPECIFIC.RFD_CONTIGS,
    ],
    "monomer_partialdiff": [
        PARAMETERS.SPECIFIC.INPUT_PDB,
        PARAMETERS.SPECIFIC.RFD_PARTIAL_DIFFUSION_TIMESTEPS,
    ],
    "binder_denovo": [
        PARAMETERS.SPECIFIC.DESIGN_LENGTH,
        PARAMETERS.SPECIFIC.INPUT_PDB,
    ],
    "binder_foldcond": [
        PARAMETERS.SPECIFIC.INPUT_PDB,
    ],
    "binder_motifscaff": [
        PARAMETERS.SPECIFIC.INPUT_PDB,
        PARAMETERS.SPECIFIC.RFD_CONTIGS,
    ],
    "binder_partialdiff": [
        PARAMETERS.SPECIFIC.INPUT_PDB,
        PARAMETERS.SPECIFIC.RFD_PARTIAL_DIFFUSION_TIMESTEPS,
    ],
    "bindcraft_denovo": [
        PARAMETERS.SPECIFIC.DESIGN_LENGTH,
        PARAMETERS.SPECIFIC.INPUT_PDB,
    ],
}

REQUIRE_FILES = {"binder_denovo"}


def validate_integer_param_limits(params: dict[str, int]) -> tuple[bool, str]:
    for key, limits in PARAMETER_LIMITS.items():
        if key not in params:
            continue

        param = params[key]

        if param < limits[0] or param > limits[1]:
            return (
                False,
                f"Parameter {key} exceeded limits ({limits[0]}, {limits[1]})",
            )

    return (True, None)


def validate_parameters(params: dict[str, object]) -> tuple[bool, str]:
    if "design_mode" not in params:
        return (False, "Design mode not in parameters")

    if "mandatory_parameters" not in params:
        print(params)
        return (False, "Mandatory parameters not provided")

    if "filtering_parameters" not in params:
        return (False, "Filtering parameters not provided")

    int_limit_validation = validate_integer_param_limits(params)

    if not int_limit_validation[0]:
        return int_limit_validation

    return (True, None)


def generate_cmd_params(params: dict[str, object]) -> list[str]:
    param_list = []

    for key, value in params.items():
        if value is None:
            continue

        param_list.append(f"--{key}")
        param_list.append(str(value))

    return param_list
