from typing import Callable

from import_export.widgets import ForeignKeyWidget


class ForeignKeyWidgetWithCreation(ForeignKeyWidget):
    def __init__(self, model, field='pk', use_natural_foreign_keys=False, get_or_create: Callable = None,
                 other_cols_map=None, **kwargs):
        super().__init__(model, field, use_natural_foreign_keys, **kwargs)
        self.other_cols = other_cols_map if other_cols_map is not None else {}
        self.get_or_create = get_or_create

    def clean(self, value, row=None, **kwargs):
        try:
            return super().clean(value, row, **kwargs)
        except self.model.DoesNotExist:
            params = {self.field: value}
            if row is not None:
                params = {**params, **{self.other_cols[p]: row[p] for p in self.other_cols if row[p] != ''}}
            return self.get_or_create(**params)
