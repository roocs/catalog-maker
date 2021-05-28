catalog-maker
=============

.. image:: https://github.com/roocs/catalog-maker/workflows/build/badge.svg
    :target: https://github.com/roocs/catalog-maker/actions
    :alt: Build Status

.. image:: https://readthedocs.org/projects/catalog-maker/badge/?version=latest
    :target: https://catalog-maker.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation

A package to build intake catalogs for cmip5, cmip6 and cordex data holdings

* Free software: BSD - see LICENSE file in top-level package directory

Creating an Intake Catalog
==========================

Catalog maker provides tools for writing data catalogs of the known data holdings in a csv format, described by a YAML file.

For each project in ``catalog_maker/etc/roocs.ini`` there are options to set the file paths for the inputs and outputs of this catalog maker.
A list of datasets to include needs to be provided. The path to this list for each project can be set in ``catalog_maker/etc/roocs.ini``. The datasets in this list must be what you want in the ``ds_id`` column of the csv file.

The data catalog is created using a database backend to store the results of the scans, from which the csv and YAML files will be created.
For this, a postgresql database is required. Once you have a database, you need to export an environment variable called ``$ABCUNIT_DB_SETTINGS``:

.. code-block::

    $ export ABCUNIT_DB_SETTINGS="dbname=<name> user=<user> host=<host> password=<pwd>"

The table created will be named after the project you are creating a catalog for in the format ``<project_name>_catalog_results`` e.g. c3s_cmip6_catalog_results

Creating batches
================

Once the list of datasets is collated a number of batches must be created:

.. code-block::

    $ python catalog_maker/cli.py create-batches -p c3s-cmip6

The option ``-p`` is required to specify the project.

Creating catalog entries
========================

Once the batches are created, the catalog maker can be run - either locally or on lotus. The settings for how many datasets to be included in a batch and the maximum duration of each job on lotus can also be changed in ``catalog_maker/etc/roocs.ini``.

Each batch can be run idependently, e.g. running batch 1 locally:

.. code-block::

    $ python catalog_maker/cli.py run -p c3s-cmip6 -b 1 -r local

or running all batches on lotus:

.. code-block::

    $ python catalog_maker/cli.py run -p c3s-cmip6 -r lotus

This creates a table in the database containing an ordered dictionary of the entry for each file in each dataset if successful, or the error traceback if there is an Exception raised.

Use the flag ``-f`` to force rescans for files that have previously been successfully scanned.

Viewing entries and errors
==========================

To view the records:

.. code-block::

    $ python catalog_maker/cli.py list -p c3s-cmip6

With many entries, this may take a while.


To just get a count of how many files have been scanned:

.. code-block::

    $ python catalog_maker/cli.py list -p c3s-cmip6 -c


To see any errors:

.. code-block::

    $ python catalog_maker/cli.py show-errors -p c3s-cmip6


To see just a count of errors:

.. code-block::

    $ python catalog_maker/cli.py show-errors -p c3s-cmip6 -c


Each count will show how many files and how many datasets have been successful/failed.

The list count will also show the total numbers of datasets/files in the database - including errors.
The error count will show whether there are any datasets that have files which have succeeded and failed i.e. that are partially scanned.
You can then use the delete command explained below to delete the entries for these partially scanned datasets if required.

Deleting entries
================
It is possible to delete entries by dataset id:

.. code-block::

    $ python catalog_maker/cli.py delete -p c3s-cmip6 -d <ds_id>

You can also provide a list of dataset ids to the -d option.
This command only deletes successful entries and will leave errors for the datasets specified in the database.

To delete all entries, including errors for specific dataset ids, use the command:

.. code-block::

    $ python catalog_maker/cli.py delete -p c3s-cmip6 -d <ds_id> -e

Writing to CSV
==============

The final command is to write the entries to a csv file.

.. code-block::

    $ python catalog_maker/cli.py write -p c3s-cmip6

The csv file will be generated in the ``csv_dir`` specified in ``catalog_maker/etc/roocs.ini`` and will have the name "{project}_{version_stamp}.csv.gz".
e.g. ``c3s-cmip6_v20210414.csv.gz``

A yaml file will be created the ``catalog_dir`` specified in ``catalog_maker/etc/roocs.ini``.
It will have the name ``c3s.yml`` and will contain the below for each project scanned and which is using the same ``catalog_dir``:

.. code-block::

    sources:
      c3s-cmip6:
        args:
          urlpath:
        cache:
        - argkey: urlpath
          type: file
        description: c3s-cmip6 datasets
        driver: intake.source.csv.CSVSource
        metadata:
          last_updated:

``urlpath`` and ``last_updated`` for a project will be updated very time the csv file is written for the project.

Deleting the table of results
=============================

In order to delete all entries in the table of results:

.. code-block::

    $ python catalog_maker/cli.py clean -p c3s-cmip6

Credits
=======

This package was created with ``Cookiecutter`` and the ``audreyr/cookiecutter-pypackage`` project template.


* Cookiecutter: https://github.com/audreyr/cookiecutter
* cookiecutter-pypackage: https://github.com/audreyr/cookiecutter-pypackage
