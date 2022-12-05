from django import forms
from import_export.forms import ImportForm

from areg_portal.settings import IGNORE_KEY, INSERT_KEY, DUPLICATE_KEY, UPDATE_KEY, FILL_KEY, OVERRIDE_KEY

FOR_NEW_CHOICES = (
    (IGNORE_KEY, "Don't Insert New Antibodies"),
    (INSERT_KEY, "Insert New Antibodies"),
)

FOR_EXTANT_CHOICES = (
    (IGNORE_KEY, "Do Nothing with Duplicates"),
    (UPDATE_KEY, "Update"),
    (DUPLICATE_KEY, "Make duplicate"),
)

METHOD_CHOICES = (
    (FILL_KEY, "Update filled columns in CSV"),
    (OVERRIDE_KEY, "Overwrite"),
)


class AntibodyImportForm(ImportForm):
    for_new = forms.ChoiceField(choices=FOR_NEW_CHOICES)
    for_extant = forms.ChoiceField(choices=FOR_EXTANT_CHOICES)
    method = forms.ChoiceField(choices=METHOD_CHOICES)
