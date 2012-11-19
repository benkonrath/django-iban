from django.db import models

from .validators import iban_validator

# From: https://en.wikipedia.org/wiki/International_Bank_Account_Number
# The IBAN consists of up to 34 alphanumeric characters.
class IbanAccountField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 34)
        super(IbanAccountField, self).__init__(*args, **kwargs)
        self.validators.append(iban_validator)


# If south is installed, ensure that IbanAccountField will be introspected just
# like a normal CharField
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^django_iban\.fields\.IbanAccountField"])
except ImportError:
    pass
