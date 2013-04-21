from django.db import models
from .validators import iban_validator, swift_bic_validator


# From: https://en.wikipedia.org/wiki/International_Bank_Account_Number
# The IBAN consists of up to 34 alphanumeric characters.
class IbanAccountField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 34)
        super(IbanAccountField, self).__init__(*args, **kwargs)
        self.validators.append(iban_validator)


# From: https://en.wikipedia.org/wiki/ISO_9362
# A SWIFT-BIC consists of up to 11 alphanumeric characters.
class SWIFTBICField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 11)
        super(SWIFTBICField, self).__init__(*args, **kwargs)
        self.validators.append(swift_bic_validator)


# If south is installed, ensure that IbanAccountField will be introspected just
# like a normal CharField
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^django_iban\.fields\.IbanAccountField"])
    add_introspection_rules([], ["^django_iban\.fields\.SWIFTBICField"])
except ImportError:
    pass
