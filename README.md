NMF Mapping for PDF or XRD Files
---------
This package takes a directory containing diffraction files in .gr (or .xy/.xye) format and performs an NMF decomposition of
the components with the goal of determining the number of structural phases present, and when these phases are
present if the data provided comes from a time series. Any non .gr ( or .xy/.xye) files or .dat files in
the directory will be ignored and skipped in the calculation.

Use
---------
This package is the backend logic for pdfitc.org/NMF. Please consider utilizing pdfitc.org/NMF prior to this tool, if
possible. If your NMF analysis requires some feature from this CLI that isn't present on the website, please let us know
and we will consider adding the feature to the pdfitc.org interface.

Installation
--------
- Install requirements from run.txt via "conda (or pip) install --file (or -r) 'requirements/run.txt'"
- Install using "pip install -e ." in a python 3 environment

Argparse
--------
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

