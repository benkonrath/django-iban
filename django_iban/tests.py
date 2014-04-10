# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

from .fields import IBANField, SWIFTBICField
from .forms import IBANFormField, SWIFTBICFormField
from .validators import IBANValidator, swift_bic_validator


class IBANTests(TestCase):
    def test_valid_iban(self):
        """ Test the IBANValidator with the valid examples in Wikipedia. """
        wikipedia_examples = [
            'GB82WEST12345698765432',
            'GR1601101250000000012300695',
            'GB29NWBK60161331926819',
            'SA0380000000608010167519',
            'CH9300762011623852957',
            'IL620108000000099999999'
        ]

        for iban in wikipedia_examples:
            IBANValidator(iban)

    def test_invalid_iban(self):
        """ Test the IBANValidator with various invalid IBANs. """
        iban_short = 'GB82WEST1234569876543'
        self.assertRaisesMessage(ValidationError, 'Wrong IBAN length for country code GB.', IBANValidator(),
                                 iban_short)

        iban_unknown_country = 'CA34CIBC123425345'
        self.assertRaisesMessage(ValidationError, 'CA is not a valid Country Code for IBAN.', IBANValidator(),
                                 iban_unknown_country)

        iban_invalid_character = 'GB29ÉWBK60161331926819'
        self.assertRaisesMessage(ValidationError, 'is not a valid character for IBAN.', IBANValidator(),
                                 iban_invalid_character)

        iban_invalid_check = 'SA0380000000608019167519'
        self.assertRaisesMessage(ValidationError, 'Not a valid IBAN.', IBANValidator(), iban_invalid_check)

    def test_iban_fields(self):
        """ Test the IBAN model and form field. """
        valid = {
            'NL02ABNA0123456789': 'NL02ABNA0123456789',
            'NL02ABNA0123456789': 'NL02ABNA0123456789',
            'NL02 ABNA 0123 4567 89': 'NL02ABNA0123456789',

            'NL91ABNA0417164300': 'NL91ABNA0417164300',
            'NL91 ABNA 0417 1643 00': 'NL91ABNA0417164300',

            'MU17BOMM0101101030300200000MUR': 'MU17BOMM0101101030300200000MUR',
            'MU17 BOMM 0101 1010 3030 0200 000M UR': 'MU17BOMM0101101030300200000MUR',

            'BE68539007547034': 'BE68539007547034',
            'BE68 5390 0754 7034': 'BE68539007547034',
        }

        invalid = {
            'NL02ABNA012345678999': ['Wrong IBAN length for country code NL.'],
            'NL02 ABNA 0123 4567 8999': ['Wrong IBAN length for country code NL.'],

            'NL91ABNB0417164300': ['Not a valid IBAN.'],
            'NL91 ABNB 0417 1643 00': ['Not a valid IBAN.'],

            'MU17BOMM0101101030300200000MUR12345': [
                'Wrong IBAN length for country code MU.',
                'Ensure this value has at most 34 characters (it has 35).'],
            'MU17 BOMM 0101 1010 3030 0200 000M UR12 345': [
                'Wrong IBAN length for country code MU.',
                'Ensure this value has at most 34 characters (it has 35).'],

            # This IBAN should only be valid only if the Nordea extensions are turned on.
            'EG1100006001880800100014553': ['EG is not a valid Country Code for IBAN.'],
            'EG11 0000 6001 8808 0010 0014 553': ['EG is not a valid Country Code for IBAN.']
        }

        self.assertFieldOutput(IBANFormField, valid=valid, invalid=invalid)

        # Test valid inputs for model field.
        iban_model_field = IBANField()
        for input, output in valid.items():
            self.assertEqual(iban_model_field.clean(input, None), output)

        # Invalid inputs for model field.
        for input, errors in invalid.items():
            with self.assertRaises(ValidationError) as context_manager:
                iban_model_field.clean(input, None)
            # The error messages for models are in a different order.
            errors.reverse()
            self.assertEqual(context_manager.exception.messages, errors)

    def test_nordea_extensions(self):
        """ Test a valid IBAN in the Nordea extensions. """
        iban_validator = IBANValidator(use_nordea_extensions=True)
        # Run the validator to ensure there are no ValidationErrors raised.
        iban_validator('EG1100006001880800100014553')


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

        swift_bic_invalid_character = 'DÉUTDEFF'
        self.assertRaises(ValidationError, swift_bic_validator, swift_bic_invalid_character)

    def test_swift_bic_fields(self):
        valid = {
            'DEUTDEFF': 'DEUTDEFF',
            'NEDSZAJJXXX': 'NEDSZAJJXXX',
            'DABADKKK': 'DABADKKK',
            'UNCRIT2B912': 'UNCRIT2B912',
            'DSBACNBXSHA': 'DSBACNBXSHA'
        }

        invalid = {
            'NEDSZAJJXX': ['A SWIFT-BIC is either 8 or 11 characters long.'],
            'CIBCJJH2': ['JJ is not a valid SWIFT-BIC Country Code.'],
            'D3UTDEFF': ['D3UT is not a valid SWIFT-BIC Institution Code.']
        }

        self.assertFieldOutput(SWIFTBICFormField, valid=valid, invalid=invalid)

        swift_bic_model_field = SWIFTBICField()

        # Test valid inputs for model field.
        for input, output in valid.items():
            self.assertEqual(swift_bic_model_field.clean(input, None), output)

        # Invalid inputs for model field.
        for input, errors in invalid.items():
            with self.assertRaises(ValidationError) as context_manager:
                swift_bic_model_field.clean(input, None)
            self.assertEqual(errors, context_manager.exception.messages)
