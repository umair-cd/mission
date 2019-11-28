from django.db.models import CharField
from django.forms import Textarea


class CharFieldWithTextarea(CharField):
    def formfield(self, **kwargs):
        kwargs.update({
            "widget": Textarea
        })
        return super(CharFieldWithTextarea, self).formfield(**kwargs)
