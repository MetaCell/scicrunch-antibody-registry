from typing import Callable

from import_export.widgets import ManyToManyWidget


class ManyToManyWidgetWithCreation(ManyToManyWidget):
    def __init__(self, model, separator=None, field=None, get_or_create: Callable = None, **kwargs):
        super().__init__(model, separator, field, **kwargs)
        self.get_or_create = get_or_create

    def clean(self, value, row=None, **kwargs):
        if not value:
            return self.model.objects.none()
        else:
            ids = value.split(self.separator)
            return [self.get_or_create(**{self.field: i.strip()}) for i in ids]