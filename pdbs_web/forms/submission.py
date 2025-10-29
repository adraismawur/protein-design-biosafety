from flask_wtf import FlaskForm
from wtforms import (
    FileField,
    IntegerField,
    SelectField,
    FormField,
    SubmitField,
)


rfd_modes = [
    "monomer_denovo",
    "monomer_foldcond",
    "monomer_motifscaff",
    "monomer_partialdiff" "binder_denovo",
    "binder_foldcond",
    "binder_motifscaff",
    "binder_partialdiff",
]


class MandatoryParameterForm(FlaskForm):
    rfd_mode = SelectField(choices=rfd_modes, render_kw={"class": "browser-default"})
    rfd_num_designs = IntegerField(default=8)
    seqs_per_design = IntegerField(default=8)


class FilteringParameterForm(FlaskForm):
    rfd_min_helices = IntegerField(default=1)
    rfd_max_helices = IntegerField(default=10)
    rfd_min_strands = IntegerField(default=1)
    rfd_max_strands = IntegerField(default=10)
    rfd_min_ss = IntegerField(default=1)
    rfd_max_ss = IntegerField(default=10)
    rfd_min_rog = IntegerField(default=1)
    rfd_max_rog = IntegerField(default=10)


class RunParameterForm(FlaskForm):
    file = FileField("Input PDB")

    mandatory_parameters = FormField(MandatoryParameterForm)
    filtering_parameters = FormField(FilteringParameterForm)

    submit = SubmitField("Submit", render_kw={"class": "btn"})
