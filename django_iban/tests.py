# coding=utf-8
import datetime
from django.core.exceptions import ValidationError
from django.test import TestCase
from .fields import IBANField, SWIFTBICField
from .forms import IBANFormField, SWIFTBICFormField
from .validators import iban_validator, swift_bic_validator


class IBANTests(TestCase):
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
        self.assertRaisesMessage(ValidationError, u'Wrong IBAN length for country code GB.', iban_validator, iban_short)

        iban_unknown_country = 'CA34CIBC123425345'
        self.assertRaisesMessage(ValidationError, u'CA is not a valid Country Code for IBAN.', iban_validator,
                                 iban_unknown_country)

        iban_invalid_character = u'GB29ÉWBK60161331926819'
        self.assertRaisesMessage(ValidationError, 'is not a valid character for IBAN.', iban_validator,
                                 iban_invalid_character)
        self.assertRaises(ValidationError, iban_validator, iban_invalid_character)

        iban_invalid_check = 'SA0380000000608019167519'
        self.assertRaisesMessage(ValidationError, u'Not a valid IBAN.', iban_validator, iban_invalid_check)

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
            self.assertRaisesMessage(ValidationError, u'Not a valid IBAN.', iban_validator, iban)

    def test_date_conditional_iban(self):
        # Test validation for Guatemala after activation date.
        future_date = datetime.date(2020, 01, 01)
        iban_validator('GT82TRAJ01020000001210029690', future_date)

    def test_iban_fields(self):
        valid = {
            'NL02ABNA0123456789': 'NL02ABNA0123456789',
            'NL91ABNA0417164300': 'NL91ABNA0417164300',
            'MU17BOMM0101101030300200000MUR': 'MU17BOMM0101101030300200000MUR',
            'BE68539007547034': 'BE68539007547034',
        }

        invalid = {
            'NL02ABNA012345678999': ['Wrong IBAN length for country code NL.'],
            'NL91ABNB0417164300': ['Not a valid IBAN.'],
            'MU17BOMM0101101030300200000MUR12345': [
                'Wrong IBAN length for country code MU.',
                'Ensure this value has at most 34 characters (it has 35).']
        }

        self.assertFieldOutput(IBANFormField, valid=valid, invalid=invalid)

        iban_model_field = IBANField()

        # Test valid inputs for model field.
        for input, output in valid.items():
            self.assertEqual(iban_model_field.clean(input, None), output)

        # Invalid inputs for model field.
        for input, errors in invalid.items():
            with self.assertRaises(ValidationError) as context_manager:
                iban_model_field.clean(input, None)
            # The error messages for models are in a different order.
            errors.reverse()
            self.assertEqual(context_manager.exception.messages, errors)


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
