import datetime
import string
try:
  from django_countries.data import COUNTRIES
except ImportError:
  from django_countries.countries import OFFICIAL_COUNTRIES as COUNTRIES
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

# Dictionary of ISO country code to IBAN length.
# Data from:
# https://en.wikipedia.org/wiki/International_Bank_Account_Number#IBAN_formats_by_country
#
# Notes
# =====
#
# French Guyana (GF), French Polynesia (PF), French Southern Territories (TF), Guadeloupe (GP), Martinique (MQ),
# Mayotte (YT), New Caledonia (NC), Reunion, Saint Pierre et Miquelon (PM), and Wallis and Futuna Islands (WF) have
# their own ISO country code but are included for the IBAN (ISO 13616:2007) under the code "FR".
#
# References:
# https://en.wikipedia.org/wiki/International_Bank_Account_Number#cite_note-36
# http://www.ecbs.org/iban/france-bank-account-number.html
# https://www.nordea.com/V%C3%A5ra+tj%C3%A4nster/Internationella+produkter+och+tj%C3%A4nster/Cash+Management/IBAN+countries/908472.html

iban_length = {'AL': 28,
               'AD': 24,
               'AT': 20,
               'AZ': 28,
               'BE': 16,
               'BH': 22,
               'BA': 20,
               'BG': 22,
               'BR': 29,
               'CR': 21,
               'HR': 21,
               'CY': 28,
               'CZ': 24,
               'DK': 18,
               'DO': 28,
               'EE': 20,
               'FO': 18,
               'FI': 18,
               'FR': 27,
               'GE': 22,
               'DE': 22,
               'GI': 23,
               'GR': 27,
               'GL': 18,
               'HU': 28,
               'IS': 26,
               'IE': 22,
               'IL': 23,
               'IT': 27,
               'KZ': 20,
               'KW': 30,
               'LV': 21,
               'LB': 28,
               'LI': 21,
               'LT': 20,
               'LU': 20,
               'MK': 19,
               'MT': 31,
               'MR': 27,
               'MU': 30,
               'MC': 27,
               'MD': 24,
               'ME': 22,
               'NL': 18,
               'NO': 15,
               'PS': 29,
               'PL': 28,
               'PK': 24,
               'PT': 25,
               'RO': 24,
               'SM': 27,
               'SA': 24,
               'RS': 22,
               'SK': 24,
               'SI': 19,
               'ES': 24,
               'SE': 24,
               'CH': 21,
               'TN': 24,
               'TR': 26,
               'AE': 23,
               'GB': 22,
               'VG': 24}


def iban_validator(value, future_date=None):
    """ A validator for International Bank Account Numbers (IBAN - ISO 13616-1:2007). """

    # TODO: Remove and add countries to main iban_length after activation date.
    if future_date:
        current_date = future_date
    else:
        current_date = timezone.now().date()

    # Qatar becomes part of the IBAN system on 1 January 2014.
    if current_date >= datetime.date(2014, 01, 01):
        iban_length['QA'] = 29

    # Guatemala becomes part of the IBAN system on 1 July 2014.
    if current_date >= datetime.date(2014, 07, 01):
        iban_length['GT'] = 28

    # Official validation algorithm:
    # https://en.wikipedia.org/wiki/International_Bank_Account_Number#Validating_the_IBAN
    # 1. Check that the total IBAN length is correct as per the country. If not, the IBAN is invalid.
    country_code = value[:2]
    if country_code in iban_length:
        if iban_length[country_code] != len(value):
            raise ValidationError(_(u"Wrong IBAN length for country code %s.") % country_code)
    else:
        raise ValidationError(_(u"%s is not a valid Country Code for IBAN.") % country_code)

    # 2. Move the four initial characters to the end of the string.
    value = value[4:] + value[:4]

    # 3. Replace each letter in the string with two digits, thereby expanding the string, where
    #    A = 10, B = 11, ..., Z = 35.
    value_digits = ""
    for x in value:
        # Check if we can use ord() before doing the official check. This protects against bad character encoding.
        if len(x) > 1:
            raise ValidationError(_(u"%s is not a valid character for IBAN.") % x)

        # The official check.
        ord_value = ord(x)
        if 48 <= ord_value <= 57:  # 0 - 9
            value_digits += x
        elif 65 <= ord_value <= 90:  # A - Z
            value_digits += str(ord_value - 55)
        else:
            raise ValidationError(_(u"%s is not a valid character for IBAN.") % x)

    # 4. Interpret the string as a decimal integer and compute the remainder of that number on division by 97.
    if int(value_digits) % 97 != 1:
        raise ValidationError(_(u"Not a valid IBAN."))


def swift_bic_validator(value):
    """ Validation for ISO 9362:2009 (SWIFT-BIC). """

    # Length is 8 or 11.
    swift_bic_length = len(value)
    if swift_bic_length != 8 and swift_bic_length != 11:
        raise ValidationError(_(u"A SWIFT-BIC is either 8 or 11 characters long."))

    # First 4 letters are A - Z.
    institution_code = value[:4]
    for x in institution_code:
        if x not in string.uppercase:
            raise ValidationError(_(u"%s is not a valid SWIFT-BIC Institution Code.") % institution_code)

    # Letters 5 and 6 consist of an ISO 3166-1 alpha-2 country code.
    country_code = value[4:6]
    if country_code not in COUNTRIES:
        raise ValidationError(_(u"%s is not a valid SWIFT-BIC Country Code.") % country_code)
