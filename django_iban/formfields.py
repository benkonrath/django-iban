from django import forms

from django_iban.validators import iban_validator, swift_bic_validator


# From: https://en.wikipedia.org/wiki/International_Bank_Account_Number
# An IBAN consists of up to 34 alphanumeric characters.
class IBANField(forms.CharField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 34)
        super(IBANField, self).__init__(*args, **kwargs)
        self.validators.append(iban_validator)


# From: https://en.wikipedia.org/wiki/ISO_9362
# A SWIFT-BIC consists of up to 11 alphanumeric characters.
class SWIFTBICField(forms.CharField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 11)
        super(SWIFTBICField, self).__init__(*args, **kwargs)
        self.validators.append(swift_bic_validator)
