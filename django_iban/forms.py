from django import forms
from .validators import IBANValidator, swift_bic_validator, IBAN_COUNTRY_CODE_LENGTH


iban_min_length = min(IBAN_COUNTRY_CODE_LENGTH.values())


class IBANFormField(forms.CharField):
    """
    An IBAN consists of up to 34 alphanumeric characters.

    https://en.wikipedia.org/wiki/International_Bank_Account_Number
    """
    default_validators = [IBANValidator()]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('min_length', iban_min_length)
        kwargs.setdefault('max_length', 34)
        super(IBANFormField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        value = super(IBANFormField, self).to_python(value)
        return value.replace(' ', '')


class SWIFTBICFormField(forms.CharField):
    """
    A SWIFT-BIC consists of up to 11 alphanumeric characters.

    https://en.wikipedia.org/wiki/ISO_9362
    """
    default_validators = [swift_bic_validator]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 11)
        super(SWIFTBICFormField, self).__init__(*args, **kwargs)
