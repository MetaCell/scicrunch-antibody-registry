from api.models import Antibody, Specie
from portal.settings import TARGET_SPECIES_RAW


def synchronize_target_species(object_id, request):
    # Make a mutable copy of request.POST
    post_data = request.POST.copy()

    original_formset_species, updated_formset_species, updated_target_species_raw = \
        get_target_species_data_from_form(object_id, post_data)

    if _only_raw_target_species_changed(original_formset_species, updated_formset_species,
                                        updated_target_species_raw):
        _add_new_species(post_data, updated_formset_species, updated_target_species_raw)
        _mark_species_to_delete(post_data, updated_target_species_raw)

    request.POST = post_data
    return request


def get_target_species_data_from_form(object_id, post_data):
    original_formset_species = set()
    # Fetch the original Antibody instance, if it exists
    if object_id:
        original_antibody = Antibody.objects.get(pk=object_id)
        original_formset_species = set([species.name for species in original_antibody.species.all()])
    # Extract the updated target_species_raw data
    updated_target_species_raw = set(name.strip() for name in post_data.get(TARGET_SPECIES_RAW, '').split(','))

    updated_formset_species = set()  # Initialize

    for key in list(post_data.keys()):
        if _is_species_formset_id_field(key):
            species_id = int(post_data[key])
            species_name = Specie.objects.get(id=species_id).name
            updated_formset_species.add(species_name)

    return original_formset_species, updated_formset_species, updated_target_species_raw


def _mark_species_to_delete(post_data, updated_target_species_raw):
    for key in list(post_data.keys()):
        if _is_species_formset_id_field(key):
            species_id = int(post_data[key])
            species_name = Specie.objects.get(id=species_id).name
            if species_name not in updated_target_species_raw:
                # Extract the index from the key and mark this form for deletion
                idx = key.split('-')[1]
                delete_checkbox_name = f'antibodyspecies_set-{idx}-DELETE'
                post_data[delete_checkbox_name] = 'on'


def _add_new_species(post_data, updated_formset_species, updated_target_species_raw):
    new_species_names = updated_target_species_raw - updated_formset_species
    new_species_ids = Specie.objects.filter(name__in=new_species_names).values_list('id', flat=True)

    # Get the current total forms count and update it
    total_forms = int(post_data.get('antibodyspecies_set-TOTAL_FORMS'))
    post_data['antibodyspecies_set-TOTAL_FORMS'] = str(total_forms + len(new_species_ids))

    for idx, species_id in enumerate(new_species_ids, start=total_forms):
        post_data[f'antibodyspecies_set-{idx}-specie'] = str(species_id)


def _only_raw_target_species_changed(original_formset_species, updated_formset_species, updated_target_species_raw):
    return updated_target_species_raw != original_formset_species \
           and updated_formset_species == original_formset_species


def _is_species_formset_id_field(key):
    return key.startswith('antibodyspecies_set') and key.endswith('specie')


def get_target_species_raw(antibody):
    species_names = [specie.name for specie in antibody.species.all()]
    return ", ".join(species_names)
