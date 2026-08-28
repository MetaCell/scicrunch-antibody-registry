from api.services.user_service import get_current_user_pk


def get_url_if_permitted(antibody):
    """
        Get antibody URL only if permitted. RULES:
        1. If user is creator of the antibody, return the URL.
        2. Else return only if the link is shown, i.e. show_link is True or it
           is unset on the antibody and the vendor shows links by default.

        Takes an Antibody model instance: it reads `owner_id` and the
        `is_link_shown` property, neither of which exists on a serialized
        schema object.
    """
    user_pk = get_current_user_pk()
    if user_pk is not None and user_pk == antibody.owner_id:
        return antibody.url if antibody.url else None
    return antibody.url if antibody.is_link_shown else None
