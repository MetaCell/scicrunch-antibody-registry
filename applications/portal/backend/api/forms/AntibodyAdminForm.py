from django import forms

from api.helpers.target_species_sync_helper import get_target_species_raw
from api.models import Antibody
from portal.settings import TARGET_SPECIES_RAW


class AntibodyForm(forms.ModelForm):
    target_species_raw = forms.CharField(required=False,
                                         label="Target species (csv)",
                                         help_text="Comma separated value for target species. Values filled here will "
                                                   "be parsed and assigned to the 'Target species' field.")

    class Meta:
        model = Antibody
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AntibodyForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields[TARGET_SPECIES_RAW].initial = get_target_species_raw(self.instance)

    def save(self, commit=True):
        instance = super(AntibodyForm, self).save(commit=commit)

        if TARGET_SPECIES_RAW in self.cleaned_data:
            instance.target_species_raw = self.cleaned_data[TARGET_SPECIES_RAW]

        return instance
