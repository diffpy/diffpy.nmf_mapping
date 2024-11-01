"""
Author: Zachary Thatcher
Local NMF Analysis of PDFs for PDFitc.
"""

import re
import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bg_mpl_stylesheets.styles import all_styles
from scipy import interpolate
from sklearn.decomposition import NMF, PCA
from sklearn.exceptions import ConvergenceWarning

from diffpy.utils.parsers.loaddata import loadData

plt.style.use(all_styles["bg-style"])
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=ConvergenceWarning)


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys_file_name(text):
    """
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    """
    return [atoi(c) for c in re.split(r"(\d+)", text.stem)]


def load_data(dir, xrd=False):
    """
    Takes a directory and selects out the .gr or .xy or .xye files. Loads these files
    into a 3D numpy array.

    Parameters
    ----------
    dir: string
        directory containing the .gr or .xy or .xye files on which NMF analysis
        will be conducted
    xrd: boolean
        whether or not to look for .xy (or .xye) files (if True) or .gr files (if False)
    Returns
    -------
    3D numpy array
        array containing the contents of the files for each file
    numpy array
        numpy array containing filenames
    """
    dir = Path(dir)
    if xrd:
        data_list = list(dir.glob("*.xy"))
        if len(data_list) == 0:
            data_list = list(dir.glob("*.xye"))
        if len(data_list) == 0:
            data_list = list(dir.glob("*.dat"))
        if len(data_list) == 0:
            raise FileNotFoundError("No xy, xye, or dat files found")
    else:
        data_list = list(dir.glob("*.gr"))
        if len(data_list) == 0:
            data_list = list(dir.glob("*.dat"))
        if len(data_list) == 0:
            raise FileNotFoundError("No gr or dat files found")
    n = len(data_list)
    data_list.sort(key=natural_keys_file_name)
    data_length = loadData(data_list[0]).shape[0]
    data_arr = np.zeros((n, data_length, 2))

    # if not on the same x grid, interpolate, use first data set as standard
    x_set = loadData(data_list[0])[:, 0]
    for i in range(n):
        new_dat = loadData(data_list[i])
        x = new_dat[:, 0]
        y = new_dat[:, 1]
        if len(x) != len(x_set) or not all(x == x_set):
            f = interpolate.interp1d(x, y, bounds_error=False, fill_value="extrapolate")
            data_arr[i][:, 1] = f(x_set)
            data_arr[i][:, 0] = x_set
        else:
            data_arr[i] = new_dat[:, :2]

    # extract list of filenames
    for j in range(n):
        data_list[j] = data_list[j].stem

    data_list = np.array(data_list)

    return data_arr, data_list


# TODO Add regularization on the frobenius norm in order to prevent creation of an excessive number of components
def NMF_decomposition(
    data_arr, x_range=None, thresh=None, additional_comp=False, improve_thresh=None, n_iter=None, pca_thresh=None
):
    """
    Takes a 3D array of PDFs and returns the structurally significant
    components present in all of the PDFs (or XRD) provided in r vs gr format,
    as well as the ratio of each in the data list, as well as the
    reconstruction error found in the first 10 components regardless
    of the threshold.

    Parameters
    ----------
    data_arr: 3D numpy array
        array containing the contents of .gr files (PDFs) or .xy or .xye files (XRD)
    x_range: tuple
        tuple containing x-range
    thresh: int
        threshold for number of NMF phase components

    Returns
    -------
    pandas dataframe
        dataframe containing the NMF components either beneath the
        reconstruction error threshold of 0.001 or the most structurally
        significant up to the allowed threshold. Index is r and the
        columns are numbered from most to least structurally significant,
        starting at 0, (loc and iloc interchange-able) to least.
    pandas dataframe
        dataframe containing the weight of the structurally significant
        phases returned in the above dataframe across the .gr files provided
    pandas dataframe
        dataframe containing the reconstruction error of the 10 most
        structurally significant components found in the NMF
    """
    y_matrix = nmf_shift(np.array([i[:, 1] for i in data_arr]))
    x_values = data_arr[0][:, 0]
    x_vs_y_df_preprocess = pd.DataFrame(y_matrix.T, index=x_values)
    df_list = []

    if n_iter is None:
        n_iter = 1000

    if x_range:
        for x_low, x_high in x_range:
            if x_low > x_high:
                raise ValueError("Invalid x-range")
            else:
                df_list.append(
                    x_vs_y_df_preprocess[
                        (x_vs_y_df_preprocess.index >= x_low) & (x_vs_y_df_preprocess.index <= x_high)
                    ]
                )
        x_vs_y_df = pd.concat(df_list)
    else:
        x_vs_y_df = x_vs_y_df_preprocess

    nmf_loss = []
    pca_explained_variance = []
    # Assuming that the algorithm won't be able to decompose a timeseries of less than x scans into
    # x or more components
    if thresh is None:
        if len(x_vs_y_df.columns) < 10:
            max_comp = len(x_vs_y_df.columns)
        else:
            max_comp = 10
    else:
        max_comp = thresh
    if pca_thresh is not None:
        pca = PCA(n_components=pca_thresh)
        pca.fit(x_vs_y_df.to_numpy().T)
        pca_number_components = len(pca.components_)
        pca_explained_variance = pca.explained_variance_ratio_
        df_explained_var_ratio = pd.DataFrame(pd.Series(pca_explained_variance))
        df_explained_var_ratio.index = df_explained_var_ratio.index + 1
    sweeping_grid = range(1, max_comp + 1, 1)
    for i in sweeping_grid:
        # Use a lower iteration number for reasonable cutoff behavior
        m = NMF(n_components=i, random_state=23, max_iter=1000)
        m.fit(x_vs_y_df.to_numpy().T)
        nmf_loss += [m.reconstruction_err_]
    df_reconstruction_error = pd.DataFrame(pd.Series(nmf_loss))
    df_reconstruction_error.index = df_reconstruction_error.index + 1
    if thresh is None:
        if improve_thresh is not None:
            if improve_thresh > 1 or improve_thresh < 0:
                raise ValueError("Invalid improvement threshold ratio. Must be between 0 and 1.")
            thresh = nmf_ncomp_selection(nmf_loss, rtol=improve_thresh)
        elif pca_thresh:
            thresh = pca_number_components
        else:
            thresh = nmf_ncomp_selection(nmf_loss)

        if additional_comp:
            thresh += 1
    # Assuming that the algorithm won't be able to decompose a timeseries of less than x scans into
    # x or more components
    if len(x_vs_y_df.columns) < thresh:
        n_comp = len(x_vs_y_df.columns)
    else:
        n_comp = thresh
    nmf = NMF(n_components=n_comp, random_state=23, max_iter=n_iter)
    nmf.fit(x_vs_y_df.to_numpy().T)
    df_components = pd.DataFrame(nmf.components_.T, index=x_vs_y_df.index)

    nmf_weight = nmf.transform(x_vs_y_df.to_numpy().T)
    nmf_weight /= nmf_weight.sum(1)[:, np.newaxis]
    nmf_weight = nmf_weight.T
    nmf_weight = np.array([nmf_weight[s, :] for s in range(n_comp)])
    df_component_weight_timeseries = pd.DataFrame(nmf_weight, index=range(n_comp))

    if pca_thresh:
        return df_components, df_component_weight_timeseries, df_reconstruction_error, df_explained_var_ratio
    return df_components, df_component_weight_timeseries, df_reconstruction_error


def component_plot(df_components, xrd=False, x_units=None, show=True):
    """
    Takes a dataframe containing the NMF components as columns and x index,
    Returns a matplotlib figure representing the constituent component plot

    Parameters
    ----------
    df_components: pandas dataframe
        dataframe containing the NMF components with r index and gr cols
    xrd: boolean
        whether or not the data is xrd data
    x_units: enum
        "twotheta" or "q". The x axis units if the data is xrd data
    show: boolean
        whether or not to show the plot, default to True

    Returns
    -------
    fig: matplotlib figure
        figure on absolute scale

    """

    df = df_components.copy()
    data_list = df.columns

    fig, ax = plt.subplots(figsize=(6, 8))
    y_w_max_range = (df.max() - df.min()).idxmax()
    max_range = (df.max() - df.min())[y_w_max_range]
    shift = max_range
    # seq to align with input phase
    for i, s in enumerate(data_list):
        ax.plot(df.index.to_numpy(dtype=np.single), df[s].to_numpy() + i * shift, label=s)
    ax.legend(loc="best")
    if xrd:
        if x_units == "twotheta" or x_units == "ttheta":
            ax.set_xlabel(r"2($\mathrm{\Theta}$)")
        else:
            ax.set_xlabel(r"$Q (nm^{-1})$")
        ax.set_ylabel(r"$Intensity$")
    else:
        ax.set_xlabel(r"r ($\mathrm{\AA}$)")
        ax.set_ylabel(r"$G^e$")
    ax.set_title("Structural Phase Components from NMF")
    ax.xaxis.set_major_locator(plt.MaxNLocator(9))

    if show:
        plt.show()

    return fig


def component_ratio_plot(df_component_weight_timeseries, show=True):
    """
    Takes a pandas df with the index representing the components and the columns
    representing the different experiments, the values being the weight.
    Returns a matplotlib figure of the component ratio across the files provided.

    Parameters
    ----------
    df_component_weight_timeseries: pandas dataframe
        dataframe containing the NMF component ratios throughout time-series
    show: boolean
        whether or not to show the plot, default to True

    Returns
    -------
    fig: matplotlib figure
        figure on absolute scale

    """

    df = df_component_weight_timeseries.copy()
    component_list = df.index
    fig, ax = plt.subplots(figsize=(6, 8))
    # seq to align with input phase
    for component in component_list:
        ax.plot(df.loc[component].to_numpy(), "--s", label=component)
    ax.legend(loc="best")
    ax.set_xlabel("Reaction time (a.u.)")
    ax.set_ylabel("Weight")
    ax.set_title("NMF Weights")

    if show:
        plt.show()

    return fig


def reconstruction_error_plot(df_reconstruction_error, show=True):
    """
    Takes a pandas df with one column representing the reconstruction error and
    an index of the phase component. Returns a matplotlib figure of the
    reconstruction error plot.

    Parameters
    ----------
    df_reconstruction_error: pandas dataframe
        dataframe containing the reconstruction error of NMF
    show: boolean
        whether or not to show the plot, default to True

    Returns
    -------
    fig: matplotlib figure
        figure on absolute scale with removed files

    """

    df = df_reconstruction_error.copy()

    fig, ax = plt.subplots(figsize=(6, 8))
    # assumes that they are in the correct order
    ax.plot(df.index.to_numpy(), df[df.columns[0]].to_numpy())
    ax.set_xlabel("Number of components")
    ax.set_ylabel("Reconstruction error")
    if len(df[df.columns[0]].to_numpy()) == 10:
        ax.set_title("Reconstruction Error\nFirst Ten Components")
    else:
        ax.set_title("Reconstruction Error")
    plt.xticks(df.index.to_numpy())

    if show:
        plt.show()

    return fig


def explained_variance_plot(df_explained_var_ratio, show=True):
    """
    Takes a pandas df with one column representing the reconstruction error and
    an index of the phase component. Returns a matplotlib figure of the
    reconstruction error plot.

    Parameters
    ----------
    df_explained_var_ratio: pandas dataframe
        dataframe containing the explained variance ratio of PCA
    show: boolean
        whether or not to show the plot, default to True

    Returns
    -------
    fig: matplotlib figure
        figure on absolute scale with removed files

    """

    df = df_explained_var_ratio.copy()

    fig, ax = plt.subplots(figsize=(6, 8))
    # assumes that they are in the correct order
    ax.plot(df.index.to_numpy(), df[df.columns[0]].to_numpy())
    ax.set_xlabel("Number of components")
    ax.set_ylabel("Explained variance")
    ax.set_title("PCA Explained Variance")
    plt.xticks(df.index.to_numpy())

    if show:
        plt.show()

    return fig


def nmf_shift(ars):
    return ars - ars.flatten().min()


def nmf_ncomp_selection(loss, rtol=None):
    rtol_unset = False
    if rtol is None:
        rtol_unset = True
        rtol = 1e-3
    starting_len = len(loss)
    loss = np.asarray(loss)  # cast anyway
    assert loss.ndim == 1
    # find improvement ratio after adding subsequent comp
    imp_ratio = np.abs(np.diff(loss) / loss[:-1])
    # comma here to make tuple an ndarray
    (inds,) = np.where(imp_ratio <= rtol)
    if not list(inds) and rtol_unset:
        print("Improvement ratio of 1E-3 not met, attempting 1E-2...")
        rtol = 1e-2
        (inds,) = np.where(imp_ratio <= rtol)
        if not list(inds):
            print("Improvement ratio of 1E-2 not met. Inspect data and impose manual cutoff")
            len(loss)
            return starting_len
    if not list(inds):
        print(f"Improvement ratio of {rtol} not met. Inspect data and impose manual cutoff")
        return starting_len
    return inds[0] + 1
