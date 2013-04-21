# coding=utf-8
import datetime
from django.core.exceptions import ValidationError
from django.test import TestCase
from django_iban.validators import swift_bic_validator
from .fields import iban_validator


class IbanTests(TestCase):
    def test_valid_iban(self):
        wikipedia_examples = [
            'GB82WEST12345698765432',
            'GR1601101250000000012300695',
            'GB29NWBK60161331926819',
            'SA0380000000608010167519',
            'CH9300762011623852957',
            'IL620108000000099999999'
        ]

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

    def test_bulgarian_algorithm(self):
        valid_examples = [
            'BG81CECB97902406715001',
            'BG33AAAA12311012345678',
        ]
        invalid_examples = [
            'BG36CECB97904006715001',
            'BG36CECB97904006715301',
            'BG81CECB97902406715011',
            'BG81CECB97902412345678',
        ]
        for iban in valid_examples:
            iban_validator(iban)
        for iban in invalid_examples:
            self.assertRaisesMessage(ValidationError, u'Not a valid IBAN.',
                                     iban_validator, iban)

    def test_date_conditional_iban(self):
        # Test validation for Guatemala after activation date.
        future_date = datetime.date(2020, 01, 01)
        iban_validator('GT82TRAJ01020000001210029690', future_date)


class SWIFTBICTests(TestCase):
    def test_valid_swift_bic(self):
        wikipedia_examples = [
            'DEUTDEFF',
            'NEDSZAJJXXX',
            'DABADKKK',
            'UNCRIT2B912',
            'DSBACNBXSHA'
        ]

        for swift_bic in wikipedia_examples:
            swift_bic_validator(swift_bic)

    def test_invalid_swift_bic(self):
        swift_bic_short = 'NEDSZAJJXX'
        self.assertRaises(ValidationError, swift_bic_validator, swift_bic_short)

        swift_bic_country = 'CIBCJJH2'
        self.assertRaises(ValidationError, swift_bic_validator, swift_bic_country)

        swift_bic_invalid_character = u'DÉUTDEFF'
        self.assertRaises(ValidationError, swift_bic_validator, swift_bic_invalid_character)
