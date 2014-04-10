from django.db import models
from .validators import IBANValidator, swift_bic_validator


class IBANField(models.CharField):
    """
    An IBAN consists of up to 34 alphanumeric characters.

    https://en.wikipedia.org/wiki/International_Bank_Account_Number
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 34)
        super(IBANField, self).__init__(*args, **kwargs)
        self.validators.append(IBANValidator())

    def to_python(self, value):
        value = super(IBANField, self).to_python(value)
        return value.replace(' ', '')


class SWIFTBICField(models.CharField):
    """
    A SWIFT-BIC consists of up to 11 alphanumeric characters.

    https://en.wikipedia.org/wiki/ISO_9362
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 11)
        super(SWIFTBICField, self).__init__(*args, **kwargs)
        self.validators.append(swift_bic_validator)


# If south is installed, ensure that IBANField will be introspected just
# like a normal CharField
try:
    from south.modelsinspector import add_introspection_rules

    add_introspection_rules([], ["^django_iban\.fields\.IBANField"])
    add_introspection_rules([], ["^django_iban\.fields\.SWIFTBICField"])
except ImportError:
    pass
