Django IBAN
===========

.. image:: https://secure.travis-ci.org/benkonrath/django-iban.png?branch=master
   :target: http://travis-ci.org/benkonrath/django-iban?branch=master

**Validated Django model fields for** `International Bank Account Numbers`_ **(IBAN - ISO 13616-1:2007) and**
`SWIFT-BIC`_ **(ISO 9362:2009).**

**Author:** Ben Konrath

**License:** 3-clause BSD

**Features:**

* Support for all currently active IBAN countries / numbers.
* Validates IBAN using the official validation algorithm.
* Date conditional support for Brazilian IBANs (active 1 July, 2013) and Guatemalan IBANs (active 1 July, 2014)
* Basic validation for SWIFT-BIC.

**Usage:**

Define a field as ``IBANField`` and/or ``SWIFTBICField`` in your ``models.py``::

    from django_iban.fields import IBANField, SWIFTBICField
    
    class Customer(Model):
        iban = IBANField()
        swift_bic = SWIFTBICField()

**Development:**

Ideas for new features include:

* SWIFT-BIC validation using referenced IBANField (SEPA requires both IBAN and SWIFT-BIC to be correct).
* Translation of validation error messages using Transifex.

Pull requests happily accepted.

.. _International Bank Account Numbers: https://en.wikipedia.org/wiki/International_Bank_Account_Number
.. _SWIFT-BIC: https://en.wikipedia.org/wiki/ISO_9362
