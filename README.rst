django-iban
===========

.. image:: https://secure.travis-ci.org/benkonrath/django-iban.png?branch=master
   :target: http://travis-ci.org/benkonrath/django-iban?branch=master
.. image:: https://coveralls.io/repos/benkonrath/django-iban/badge.png?branch=master
   :target: https://coveralls.io/r/benkonrath/django-iban?branch=master
.. image:: https://pypip.in/v/django-iban/badge.png
   :target: https://crate.io/packages/django-iban/
.. image:: https://pypip.in/d/django-iban/badge.png
   :target: https://crate.io/packages/django-iban/

Validated Django model fields for `International Bank Account Numbers`_ (IBAN - ISO 13616-1:2007) and
`SWIFT-BIC`_ (ISO 9362:2009).

**Author:** Ben Konrath

**License:** 3-clause BSD

**Features:**

* Validates IBAN using the official validation algorithm.
* Support for all currently active and planned to be active IBAN countries / numbers.
* Optional validation for IBANs included the Nordea IBAN extensions.
* Optionally limit validation to a list specific of countries.
* Basic validation for SWIFT-BIC.
* Supports Django 1.4, 1.5 and 1.6.
* Python 3.2 and 3.3 support for Django >= 1.5.

**Usage:**

Use the model fields ``IBANField`` and/or ``SWIFTBICField`` in your models::

    from django.db import models
    from django_iban.fields import IBANField, SWIFTBICField

    class CustomerModel(models.Model):
        iban = IBANField()
        swift_bic = SWIFTBICField()

Use the form fields ``IBANFormField`` and/or ``SWIFTBICFormField`` in your forms::

    from django import forms
    from django_iban.forms import IBANFormField, SWIFTBICFormField

    class CustomerForm(forms.Form):
        iban = IBANFormField()
        swift_bic = SWIFTBICFormField()

To limit IBAN validation to specific countries, set the 'include_countries' argument with a tuple or list of ISO 3166-1
alpha-2 codes. For example, `include_countries=('NL', 'BE, 'LU')`.

A list of countries that use IBANs as part of SEPA is included for convenience. To use this feature, set
`include_countries=IBAN_SEPA_COUNTRIES` as an argument to the field.

    Example::

    from django.db import models
    from django_iban.fields import IBANField,
    from django_iban.sepa_countries import IBAN_SEPA_COUNTRIES

    class MyModel(models.Model):
        iban = IBANField(include_countries=IBAN_SEPA_COUNTRIES)

In addition to validating official IBANs, this field can optionally validate unofficial IBANs that have been
catalogued by Nordea by setting the `use_nordea_extensions` argument to True.


**Development:**

Coding style: PEP8 with 120 character lines.

.. _International Bank Account Numbers: https://en.wikipedia.org/wiki/International_Bank_Account_Number
.. _SWIFT-BIC: https://en.wikipedia.org/wiki/ISO_9362
