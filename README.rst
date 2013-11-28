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

* Support for all currently active IBAN countries / numbers.
* Validates IBAN using the official validation algorithm.
* Date conditional support for Qatar IBANs (active 1 January, 2014)
* Date conditional support for Guatemalan IBANs (active 1 July, 2014)
* Basic validation for SWIFT-BIC.

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

**Development:**

Coding style: PEP8 with 120 character lines.

Ideas for new features include:

* SWIFT-BIC validation using referenced IBANField (SEPA requires both IBAN and SWIFT-BIC to be correct).
* Translation of validation error messages using Transifex.

Pull requests happily accepted.

.. _International Bank Account Numbers: https://en.wikipedia.org/wiki/International_Bank_Account_Number
.. _SWIFT-BIC: https://en.wikipedia.org/wiki/ISO_9362
