from import_export.forms import ImportForm
from django import forms

FOR_NEW_CHOICES = (
    ("ignore", "Don't Insert New Antibodies"),
    ("insert", "Insert New Antibodies"),
)

FOR_EXTANT_CHOICES = (
    ("ignore", "Do Nothing with Duplicates"),
    ("update", "Update"),
    ("duplicate", "Make duplicate"),
)

METHOD_CHOICES = (
    ("fill", "Update filled columns in CSV"),
    ("overwrite", "Overwrite"),
)


class AntibodyImportForm(ImportForm):
    for_new = forms.ChoiceField(choices=FOR_NEW_CHOICES)
    for_extant = forms.ChoiceField(choices=FOR_EXTANT_CHOICES)
    method = forms.ChoiceField(choices=METHOD_CHOICES)
