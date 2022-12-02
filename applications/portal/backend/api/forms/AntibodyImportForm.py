from django import forms
from import_export.forms import ImportForm

from areg_portal.settings import IGNORE, INSERT, DUPLICATE, UPDATE, FILL, OVERRIDE

FOR_NEW_CHOICES = (
    (IGNORE, "Don't Insert New Antibodies"),
    (INSERT, "Insert New Antibodies"),
)

FOR_EXTANT_CHOICES = (
    (IGNORE, "Do Nothing with Duplicates"),
    (UPDATE, "Update"),
    (DUPLICATE, "Make duplicate"),
)

METHOD_CHOICES = (
    (FILL, "Update filled columns in CSV"),
    (OVERRIDE, "Overwrite"),
)


class AntibodyImportForm(ImportForm):
    for_new = forms.ChoiceField(choices=FOR_NEW_CHOICES)
    for_extant = forms.ChoiceField(choices=FOR_EXTANT_CHOICES)
    method = forms.ChoiceField(choices=METHOD_CHOICES)
