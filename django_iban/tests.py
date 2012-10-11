# coding=utf-8
from django.core.exceptions import ValidationError
from django.test import TestCase
from .fields import iban_validator


class IbanTests(TestCase):
    def test_valid_iban(self):
        wikipedia_examples = [ 'GB82WEST12345698765432',
                               'GR1601101250000000012300695',
                               'GB29NWBK60161331926819',
                               'SA0380000000608010167519',
                               'CH9300762011623852957',
                               'IL620108000000099999999' ]

        for iban in wikipedia_examples:
            iban_validator(iban)

    def test_invalid_iban(self):
        iban_short = 'GB82WEST1234569876543'
        self.assertRaisesMessage(ValidationError, u'Wrong IBAN length for country code GB.',
                                 iban_validator, iban_short)

        iban_unknown_country = 'CA34CIBC123425345'
        self.assertRaisesMessage(ValidationError, u'CA is not a valid Country Code for IBAN.',
                                 iban_validator, iban_unknown_country)

        iban_invalid_character = u'GB29ÉWBK60161331926819'
        # TODO: assertRaisesMessage() is throwing a UnicodeEncodeError when
        #       message has a unicode character.
        # self.assertRaisesMessage(ValidationError, u'É is not a valid character for IBAN.',
        #                         iban_validator, iban_invalid_character)
        self.assertRaises(ValidationError, iban_validator, iban_invalid_character)

        iban_invalid_check = 'SA0380000000608019167519'
        self.assertRaisesMessage(ValidationError, u'Not a valid IBAN.',
                                 iban_validator, iban_invalid_check)