# from flask_wtf import FlaskForm
from wtforms import FileField, Form, IntegerField, FormField, SubmitField, StringField


design_modes = [
    "monomer_denovo",
    "monomer_foldcond",
    "monomer_motifscaff",
    "monomer_partialdiff" "binder_denovo",
    "binder_foldcond",
    "binder_motifscaff",
    "binder_partialdiff",
]


class MandatoryMonomerDenovoForm(Form):
    design_length = StringField(label="Design length", default="60-100")
    rfd_num_designs = IntegerField(label="Number of designs", default=8)
    seqs_per_design = IntegerField(label="Sequences per design", default=8)


class FilteringParameterForm(Form):
    rfd_min_helices = IntegerField(default=1)
    rfd_max_helices = IntegerField(default=10)
    rfd_min_strands = IntegerField(default=1)
    rfd_max_strands = IntegerField(default=10)
    rfd_min_ss = IntegerField(default=1)
    rfd_max_ss = IntegerField(default=10)
    rfd_min_rog = IntegerField(default=1)
    rfd_max_rog = IntegerField(default=10)


class RunParameterForm(Form):
    file = FileField("Input PDB")

    filtering_parameters = FormField(FilteringParameterForm)

    submit = SubmitField("Submit", render_kw={"class": "btn"})
