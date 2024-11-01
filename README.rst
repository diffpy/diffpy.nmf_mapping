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

Input:
- directory: path to the directory containing the diffraction files that are to be analyzed
    - format: string (filepath)
        - eg: '/Users/zthatcher/Desktop/Data/nmf_mapping/time_data/' or . for cwd

- save-files (optional): boolean as to whether or not you would like to save the dataframes, plots, and
components (note: pdf data saves as .cgr and xrd data saves as .xy)
    - format: boolean
        - eg: --save-files False
    - default: True

- threshold (optional and mut-exc to other thresholds): a threshold for the number of structural phases graphed (NMF components returned)
    - format as: integer
        - eg: --threshold 2
    - default: 10

- improve-thresh (optional and mut-exc to other thresholds): a threshold (between 0 and 1) for the relative improvement ratio necessary to
  add an additional component. Default is 0.001. 0.1 Recommended for real data.
    - format: float
        - eg: --improve-thresh 0.1
    - default = 0.001

- pca-thresh (optional and mut-exc to other thresholds): explained variance threshold for PCA component counting cutoff
    - format: float
        - eg: --pca-thresh 0.95
    - default = None

- n-iter (optional): total number of iterations to run NMF algo. Defaults to 1000. 10000 typical to publish.
    - format: int
        - eg: --n-iter 10000
    - default: 1000

- x-range (optional): the active x-range over which to run the NMF analysis (must be between shortest and
longest range in the set of files)
    - format: pair of integers representing the lower r bound and the upper r bound with a comma between
    the lower and upper bound
        -  eg: --xrange 5,10 12,15
    - default: entire range

- xrd (optional): set this option if the directory contains xy or xye files rather than gr.
    - format: boolean
        - eg: --xrd True
    - default: False

- x_units (required if xrd): set this as either twotheta or q if working with xrd data.
    - format: enum[str]
        - eg: --x_units twotheta
    - default: None (since --xrd defaults to False)

- show graphs (optional): whether you or not you would like display the images
    - format: boolean
        - eg: --show False
    - default: True

Returns:
- Figure One: PDF or XRD pattern of structural phase components contributing to the NMF reconstruction
- Figure Two: Weights of the phase components plotted in Figure One
- Figure Three: Reconstruction error as a function of components
- (Optional) Figure Four: Explained Variance plot as a function of components for PCA thresholding

Example:

nmf_mapping . --threshold 3 --xrange 5,10 --show True


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
