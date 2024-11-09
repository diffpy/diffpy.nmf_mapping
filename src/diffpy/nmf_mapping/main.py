import os
import sys
import time
from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
from datetime import datetime

import numpy as np

import diffpy.nmf_mapping.nmf_mapping_code as nmf


def boolean_string(s):
    try:
        if s.lower() not in {"false", "true"}:
            raise ValueError("Not a valid boolean string")
    except AttributeError:
        raise ValueError("Not a valid boolean string")
    return s.lower() == "true"


def main(args=None):
    """
    Parses directory argument supplied by user and conducts NMF decomposition
    analysis (computes NMF decomposition and shows the weights over time).
    """

    _BANNER = """
    This is a package which takes a directory of 1D diffraction files
    (xrd or pdf) and returns json files containing the decomposed components,
    the phase fraction of these components from file to file,
    as well as the reconstruction error as a fxn of component
    """

    parser = ArgumentParser(prog="nmf_mapping", description=_BANNER, formatter_class=RawTextHelpFormatter)

    def tup(s):
        if not isinstance(s, str):
            raise TypeError("Input must be a string of two integers separated by a comma.")

        try:
            l, h = map(int, s.split(","))
            return l, h
        except ValueError:
            raise ValueError("Input must be two integers separated by a comma (e.g., '1,5')")

    # args
    parser.add_argument(
        "directory", default=None, type=str, help="a directory of PDFs to calculate NMF decomposition"
    )
    group = parser.add_mutually_exclusive_group()
    parser.add_argument(
        "--save-files",
        default=True,
        type=boolean_string,
        help="whether to save the component, graph, and json files in the execution directory\n"
        "default: True\n"
        "e.g. --save-files False",
    )
    group.add_argument(
        "--threshold",
        default=None,
        type=int,
        help="a threshold for the number of structural phases graphed (NMF components returned)\n"
        "e.g. --threshold 3",
    )
    group.add_argument(
        "--improve-thresh",
        default=None,
        type=float,
        help="a threshold (between 0 and 1) for the relative improvement ratio necessary to add an"
        " additional component. Default is 0.001. 0.1 Recommended for real data.\n"
        "e.g. --improve-thresh 0.1",
    )
    group.add_argument(
        "--pca-thresh",
        default=None,
        type=float,
        help="a threshold (between 0 and 1) for the explained variance of PCA to determine the \n"
        "number of components for NMF. e.g. --pca-thresh 0.95",
    )
    parser.add_argument(
        "--n-iter",
        default=None,
        type=int,
        help="total number of iterations to run NMF algo. Defaults to 1000. 10000 typical to publish.",
    )
    parser.add_argument(
        "--xrd",
        default=False,
        type=boolean_string,
        help="whether to look for .xy files rather than .gr files\n" "default: False\n" "e.g. --xrd True",
    )
    parser.add_argument(
        "--x_units",
        default=None,
        type=str,
        choices=["twotheta", "q"],
        required="--xrd" in sys.argv,
        help="x axis units for XRD data\n" "default: None\n" "e.g. --x_units twotheta",
    )
    parser.add_argument(
        "--xrange",
        default=None,
        type=tup,
        nargs="*",
        help="the x-range over which to calculate NMF, can be multiple ranges (e.g. --xrange 5,10 12,15)",
    )
    parser.add_argument("--show", default=True, type=boolean_string, help="whether to show the plot")
    args0 = Namespace()
    args1, _ = parser.parse_known_args(args, namespace=args0)

    input_list, data_list = nmf.load_data(args1.directory, args1.xrd)
    if args1.pca_thresh:
        df_components, df_component_weight_timeseries, df_reconstruction_error, df_explained_var_ratio = (
            nmf.NMF_decomposition(
                input_list,
                args1.xrange,
                args1.threshold,
                additional_comp=False,
                improve_thresh=args1.improve_thresh,
                n_iter=args1.n_iter,
                pca_thresh=args1.pca_thresh,
            )
        )
    else:
        df_components, df_component_weight_timeseries, df_reconstruction_error = nmf.NMF_decomposition(
            input_list,
            args1.xrange,
            args1.threshold,
            additional_comp=False,
            improve_thresh=args1.improve_thresh,
            n_iter=args1.n_iter,
        )

    fig1 = nmf.component_plot(df_components, args1.xrd, args1.x_units, args1.show)
    fig2 = nmf.component_ratio_plot(df_component_weight_timeseries, args1.show)
    fig3 = nmf.reconstruction_error_plot(df_reconstruction_error, args1.show)
    if args1.pca_thresh:
        fig4 = nmf.explained_variance_plot(df_explained_var_ratio, args1.show)

    if args1.save_files:
        if not os.path.exists(os.path.join(os.getcwd(), "nmf_result")):
            os.mkdir(os.path.join(os.getcwd(), "nmf_result"))
        output_fn = datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H%M%S%f")
        df_components.to_json(os.path.join(os.getcwd(), "nmf_result", "x_index_vs_y_col_components.json"))
        df_component_weight_timeseries.to_json(
            os.path.join(os.getcwd(), "nmf_result", "component_index_vs_pratio_col.json")
        )
        df_component_weight_timeseries.to_csv(
            os.path.join(os.getcwd(), "nmf_result", output_fn + "component_row_pratio_col.txt"),
            header=None,
            index=False,
            sep=" ",
            mode="a",
        )
        df_reconstruction_error.to_json(
            os.path.join(os.getcwd(), "nmf_result", "component_index_vs_RE_value.json")
        )
        plot_file1 = os.path.join(os.getcwd(), "nmf_result", output_fn + "comp_plot.png")
        plot_file2 = os.path.join(os.getcwd(), "nmf_result", output_fn + "ratio_plot.png")
        plot_file3 = os.path.join(os.getcwd(), "nmf_result", output_fn + "loss_plot.png")
        if args1.pca_thresh:
            plot_file7 = os.path.join(os.getcwd(), "nmf_result", output_fn + "pca_var_plot.png")
        plot_file4 = os.path.splitext(plot_file1)[0] + ".pdf"
        plot_file5 = os.path.splitext(plot_file2)[0] + ".pdf"
        plot_file6 = os.path.splitext(plot_file3)[0] + ".pdf"
        if args1.pca_thresh:
            plot_file8 = os.path.splitext(plot_file7)[0] + ".pdf"
        txt_file = os.path.join(os.getcwd(), "nmf_result", output_fn + "_meta" + ".txt")
        with open(txt_file, "w+") as fi:
            fi.write("NMF Analysis\n\n")
            fi.write(f"{len(df_component_weight_timeseries.columns)} files uploaded for analysis.\n\n")
            fi.write(f"The selected active r ranges are:  {args1.xrange} \n\n")
            fi.write("Thesholding:\n")
            fi.write(f"\tThe input component threshold was: {args1.threshold}\n")
            fi.write(f"\tThe input improvement threshold was: {args1.improve_thresh}\n")
            fi.write(f"\tThe input # of iterations to run was: {args1.n_iter}\n")
            fi.write(f"\tWas PCA thresholding used?: {args1.pca_thresh}\n")
            fi.write(f"{len(df_components.columns)} components were extracted")

        fig1.savefig(plot_file1)
        fig2.savefig(plot_file2)
        fig3.savefig(plot_file3)
        if args1.pca_thresh:
            fig4.savefig(plot_file7)
        fig1.savefig(plot_file4)
        fig2.savefig(plot_file5)
        fig3.savefig(plot_file6)
        if args1.pca_thresh:
            fig4.savefig(plot_file8)
        columns = df_components.columns
        for i, col in enumerate(columns):
            data = np.column_stack([df_components.index.to_list(), df_components[col].to_list()])

            if args1.xrd:
                np.savetxt(
                    os.path.join(os.getcwd(), "nmf_result", output_fn + f"_comp{i}" + ".xy"),
                    data,
                    header=f"NMF Generated XRD\nSource = nmfMapping\n"
                    f"Date = {output_fn}\n{args1.x_units} Intensity\n",
                    fmt="%s",
                    comments="' ",
                )
            else:
                np.savetxt(
                    os.path.join(os.getcwd(), "nmf_result", output_fn + f"_comp{i}" + ".cgr"),
                    data,
                    header=f"NMF Generated PDF\nSource: nmfMapping\n" f"Date: {output_fn}\nr g",
                    fmt="%s",
                )


if __name__ == "__main__":
    main()
