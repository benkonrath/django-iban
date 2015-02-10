django-iban
===========

.. WARNING::
   **Obsolete package** You should not use this package any longer. The IBAN and BIC fields are now
   available in version 1.1 and later of the https://pypi.python.org/pypi/django-localflavor package.
   Bug reports and feature requests should be filed against https://github.com/django/django-localflavor.

   The IBAN and BIC fields in django-localflavor have bugs fixes that are not included in this package.
   Please migrate existing code to the IBAN and BIC fields in the `django-localflavor generic package`_.

**Migrating Model Fields to django-localflavor**

Add `localflavor` to your `INSTALLED_APPS` and then change the model fields ``IBANField``
and``SWIFTBICField`` to the versions from django-localflavor.

For example, the django-iban model fields should be changed from this::

    from django_iban.fields import IBANField, SWIFTBICField

    class CustomerModel(models.Model):
        iban = IBANField()
        bic = SWIFTBICField()

to the django-localflavor model field versions::

    from localflavor.generic.models import IBANField, BICField

    class CustomerModel(models.Model):
        iban = IBANField()
        bic = BICField()

For Django < 1.7, you will need to use South to migrate your database. Use `schemamigration`
to create a migration and then run `migrate` alter your database. For example::

    % ./manage.py schemamigration myapp --auto convert_django_iban_to_django_localflavor
     ~ Changed field iban on myapp.CustomerModel
     ~ Changed field bic on myapp.CustomerModel
    Created 0002_convert_django_iban_to_django_localflavor.py. You can now apply this migration with: ./manage.py migrate myapp

    % ./manage.py migrate myapp
    Running migrations for myapp:
     - Migrating forwards to 0002_convert_django_iban_to_django_localflavor.
     > myapp:0002_convert_django_iban_to_django_localflavor
     - Loading initial data for myapp.
    Installed 0 object(s) from 0 fixture(s)

For Django >= 1.7, run `makemigrations` to create a migration and then run `migrate` alter
your database. For example::

    % ./manage.py makemigrations myapp
    Migrations for 'myapp':
      0002_auto_20150210_1004.py:
        - Alter field bic on customermodel
        - Alter field iban on customermodel

    % ./manage.py migrate myapp
    Operations to perform:
      Apply all migrations: myapp
    Running migrations:
      Applying myapp.0002_auto_20150210_1004... OK

**Migrating Form Fields to django-localflavor**

Change the form fields ``IBANFormField`` and ``SWIFTBICFormField`` to the versions from django-localflavor.

For example, the django-iban form fields should be changed from this::

    from django_iban.forms import IBANFormField, SWIFTBICFormField

    class CustomerForm(forms.Form):
        iban = IBANFormField()
        swift_bic = SWIFTBICFormField()

to the django-localflavor form field versions::

    from localflavor.generic.forms import IBANFormField, BICFormField

    class CustomerForm(forms.Form):
        iban = IBANFormField()
        bic = BICFormField()

.. _django-localflavor generic package: https://django-localflavor.readthedocs.org/en/latest/generic/
