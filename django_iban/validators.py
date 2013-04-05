import datetime

from django.core.exceptions import ValidationError
from django.utils import timezone

# Dictionary of ISO country code to IBAN length.
# Data from:
# https://en.wikipedia.org/wiki/International_Bank_Account_Number#IBAN_formats_by_country
iban_length = { 'AL': 28,
                'AD': 24,
                'AT': 20,
                'AZ': 28,
                'BE': 16,
                'BH': 22,
                'BA': 20,
                'BG': 22,
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
                'VG': 24,
    # https://en.wikipedia.org/wiki/International_Bank_Account_Number#cite_note-24
    # French Polynesia (PF), French Southern Territories (TF), Mayotte (YT),
    # New Caledonia (NC), Saint Pierre and Miquelon (PM), and
    # Wallis and Futuna Islands (WF) have their own ISO country code but may be
    # identified within the IBAN by either FR or their specific country code.
                'PF': 27,
                'TF': 27,
                'YT': 27,
                'NC': 27,
                'PM': 27,
                'WF': 27 }

def iban_validator(value, future_date=None):
    # TODO: Remove and add countries to main iban_length after activation date.
    if future_date:
        current_date = future_date
    else:
        current_date = timezone.now().date()
    # Brazil becomes part of the IBAN system on 1 July 2013.
    if current_date >= datetime.date(2013, 07, 01):
        iban_length['BR'] = 29
    # Guatemala becomes part of the IBAN system on 1 July 2014.
    if current_date >= datetime.date(2014, 07, 01):
        iban_length['GT'] = 28

    # Official validation algorithm:
    # https://en.wikipedia.org/wiki/International_Bank_Account_Number#Validating_the_IBAN
    # 1. Check that the total IBAN length is correct as per the country. If not,
    #    the IBAN is invalid.
    country_code = value[:2]
    if iban_length.has_key(country_code):
        if iban_length[country_code] != len(value):
            raise ValidationError(u"Wrong IBAN length for country code %s." % country_code)
    else:
        raise ValidationError(u"%s is not a valid Country Code for IBAN." % country_code)

    # 2. Move the four initial characters to the end of the string.
    value = value[4:] + value[:4]

    # 3. Replace each letter in the string with two digits, thereby expanding
    #    the string, where A = 10, B = 11, ..., Z = 35.
    value_digits = ""
    for x in value:
        # Check if we can use ord() before doing the official check. This
        # protects against bad character encoding.
        if len(x) > 1:
            raise ValidationError(u"%s is not a valid character for IBAN." % x)

        # The official check.
        ord_value = ord(x)
        if 48 <= ord_value <= 57:  # 0 - 9
            value_digits += x
        elif 65 <= ord_value <= 90:  # A - Z
            value_digits += str(ord_value - 55)
        else:
            raise ValidationError(u"%s is not a valid character for IBAN." % x)

    # 4. Interpret the string as a decimal integer and compute the remainder of
    # that number on division by 97.
    # If the country code is BG we replace the control number with 00
    # and from 98 subtract the remainder from division by 97 and expect the
    # result to be equal with the original control number
    if country_code == 'BG':
        control_number = int(value_digits[-2:])
        value_digits = value_digits[:-2] + '00'
        if control_number != (98 - int(value_digits) % 97):
            raise ValidationError(u"Not a valid IBAN.")
    else:
        if int(value_digits) % 97 != 1:
            raise ValidationError(u"Not a valid IBAN.")
