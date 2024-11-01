|Icon| |title|_
===============

.. |title| replace:: diffpy.nmf_mapping
.. _title: https://diffpy.github.io/diffpy.nmf_mapping

.. |Icon| image:: https://avatars.githubusercontent.com/diffpy
        :target: https://diffpy.github.io/diffpy.nmf_mapping
        :height: 100px

|PyPi| |Forge| |PythonVersion| |PR|

|CI| |Codecov| |Black| |Tracking|

.. |Black| image:: https://img.shields.io/badge/code_style-black-black
        :target: https://github.com/psf/black

.. |CI| image:: https://github.com/diffpy/diffpy.nmf_mapping/actions/workflows/matrix-and-codecov-on-merge-to-main.yml/badge.svg
        :target: https://github.com/diffpy/diffpy.nmf_mapping/actions/workflows/matrix-and-codecov-on-merge-to-main.yml

.. |Codecov| image:: https://codecov.io/gh/diffpy/diffpy.nmf_mapping/branch/main/graph/badge.svg
        :target: https://codecov.io/gh/diffpy/diffpy.nmf_mapping

.. |Forge| image:: https://img.shields.io/conda/vn/conda-forge/diffpy.nmf_mapping
        :target: https://anaconda.org/conda-forge/diffpy.nmf_mapping

.. |PR| image:: https://img.shields.io/badge/PR-Welcome-29ab47ff

.. |PyPi| image:: https://img.shields.io/pypi/v/diffpy.nmf_mapping
        :target: https://pypi.org/project/diffpy.nmf_mapping/

.. |PythonVersion| image:: https://img.shields.io/pypi/pyversions/diffpy.nmf_mapping
        :target: https://pypi.org/project/diffpy.nmf_mapping/

.. |Tracking| image:: https://img.shields.io/badge/issue_tracking-github-blue
        :target: https://github.com/diffpy/diffpy.nmf_mapping/issues

Python package for running NMF analysis on PDF and XRD data.

This package takes a directory containing diffraction files in .gr (or .xy/.xye) format and performs an NMF decomposition of
the components with the goal of determining the number of structural phases present, and when these phases are
present if the data provided comes from a time series. Any non .gr ( or .xy/.xye) files or .dat files in
the directory will be ignored and skipped in the calculation.

This package is the backend logic for pdfitc.org/NMF. Please consider utilizing pdfitc.org/NMF prior to this tool, if
possible. If your NMF analysis requires some feature from this CLI that isn't present on the website, please let us know
and we will consider adding the feature to the pdfitc.org interface.

For more information about the diffpy.nmf_mapping library, please consult our `online documentation <https://diffpy.github.io/diffpy.nmf_mapping>`_.

Citation
--------

If you use this program for a scientific research that leads
to publication, we ask that you acknowledge use of the program
by citing the following paper in your publication:

   Z. A. Thatcher, C.-H. Liu, L. Yang, B. C. McBride, G. Thinh Tran, A. Wustrow, M. A. Karlsen, J. R. Neilson, D. B. Ravnsbæk, and S. J. L. Billinge,
   `nmfMapping: a cloud-based web application for non-negative matrix factorization of powder diffraction and pair distribution function datasets
   <https://doi.org/10.1107/S2053273322002522>`__,
   *Acta Crystallogr. A* **78**, 242-248 (2022).

and please consider citing

   C.-H. Liu, C. J. Wright, R. Gu, S. Bandi, A. Wustrow, P. K. Todd, D. O'Nolan, M. L. Beauvais, J. R. Neilson, P. J. Chupas, K. W. Chapman, and S. J. L. Billinge,
   `Validation of non-negative matrix factorization for rapid assessment of large sets of atomic pair distribution function data
   <https://doi.org/10.1107/S160057672100265X>`__,
   *J. Appl. Cryst.* **54**, 768-775 (2022).

Installation
------------

The preferred method is to use `Miniconda Python
<https://docs.conda.io/projects/miniconda/en/latest/miniconda-install.html>`_
and install from the "conda-forge" channel of Conda packages.

To add "conda-forge" to the conda channels, run the following in a terminal. ::

        conda config --add channels conda-forge

We want to install our packages in a suitable conda environment.
The following creates and activates a new environment named ``diffpy.nmf_mapping_env`` ::

        conda create -n diffpy.nmf_mapping_env diffpy.nmf_mapping
        conda activate diffpy.nmf_mapping_env

To confirm that the installation was successful, type ::

        python -c "import diffpy.nmf_mapping; print(diffpy.nmf_mapping.__version__)"

The output should print the latest version displayed on the badges above.

If the above does not work, you can use ``pip`` to download and install the latest release from
`Python Package Index <https://pypi.python.org>`_.
To install using ``pip`` into your ``diffpy.nmf_mapping_env`` environment, type ::

        pip install diffpy.nmf_mapping

If you prefer to install from sources, after installing the dependencies, obtain the source archive from
`GitHub <https://github.com/diffpy/diffpy.nmf_mapping/>`_. Once installed, ``cd`` into your ``diffpy.nmf_mapping`` directory
and run the following ::

        pip install .

Getting Started
---------------


You may consult our `online documentation <https://diffpy.github.io/diffpy.nmf_mapping>`_ for tutorials and API references.

Support and Contribute
----------------------

`Diffpy user group <https://groups.google.com/g/diffpy-users>`_ is the discussion forum for general questions and discussions about the use of diffpy.nmf_mapping. Please join the diffpy.nmf_mapping users community by joining the Google group. The diffpy.nmf_mapping project welcomes your expertise and enthusiasm!

If you see a bug or want to request a feature, please `report it as an issue <https://github.com/diffpy/diffpy.nmf_mapping/issues>`_ and/or `submit a fix as a PR <https://github.com/diffpy/diffpy.nmf_mapping/pulls>`_. You can also post it to the `Diffpy user group <https://groups.google.com/g/diffpy-users>`_.

Feel free to fork the project and contribute. To install diffpy.nmf_mapping
in a development mode, with its sources being directly used by Python
rather than copied to a package directory, use the following in the root
directory ::

        pip install -e .

To ensure code quality and to prevent accidental commits into the default branch, please set up the use of our pre-commit
hooks.

1. Install pre-commit in your working environment by running ``conda install pre-commit``.

2. Initialize pre-commit (one time only) ``pre-commit install``.

Thereafter your code will be linted by black and isort and checked against flake8 before you can commit.
If it fails by black or isort, just rerun and it should pass (black and isort will modify the files so should
pass after they are modified). If the flake8 test fails please see the error messages and fix them manually before
trying to commit again.

Improvements and fixes are always appreciated.

Before contributing, please read our `Code of Conduct <https://github.com/diffpy/diffpy.nmf_mapping/blob/main/CODE_OF_CONDUCT.rst>`_.

Contact
-------

For more information on diffpy.nmf_mapping please visit the project `web-page <https://diffpy.github.io/>`_ or email Prof. Simon Billinge at sb2896@columbia.edu.
