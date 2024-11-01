import os
import pathlib

import numpy as np

import diffpy.nmf_mapping.nmf_mapping_code as nmf

dir = pathlib.Path(__file__).parent.resolve()


def test_load_data():
    # make sure extracting correct filenames
    bfto_dir = os.path.join(dir, "data/synthetic_r_vs_gr")
    bfto_expected_filenames = np.array([f"synthetic{i}" for i in range(50)])
    loaded_filenames = nmf.load_data(bfto_dir)[1]
    assert np.testing.assert_array_equal(loaded_filenames, bfto_expected_filenames) is None

    # make sure interpolation to same r-grid is working
    diff_r_grid_dir = os.path.join(dir, "data", "different_r_grid")
    diff_r_grid_arr = nmf.load_data(diff_r_grid_dir)[0]
    assert np.testing.assert_array_equal(diff_r_grid_arr[0][:, 0], diff_r_grid_arr[1][:, 0]) is None
