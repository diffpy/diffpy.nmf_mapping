import shutil
from os.path import exists, join
from pathlib import Path

import pytest

from diffpy.nmf_mapping.main import main

dir = Path(__file__).parent.resolve()
data_dir = join(dir, "data/synthetic_r_vs_gr")


@pytest.mark.parametrize(
    "args, output_dir",
    [
        (["tests/data/synthetic_r_vs_gr", "--xrange", "5,10", "--show", "false"], "output_1"),
        (["tests/data/synthetic_r_vs_gr", "--show", "false"], "output_2"),
        (["tests/data/synthetic_r_vs_gr", "--xrange", "5,10", "12,15", "--show", "false"], "output_3"),
    ],
)
def test_nmf_mapping_code(args, output_dir, tmpdir):

    # Save the result in ("nmf_result") at the top project level (default behavior)
    main(args=args)

    # Define the copied results directory in tmpdir
    tmp_results_dir = join(tmpdir, "nmf_result")
    expected_output_dir = join("tests/output", output_dir)

    # Copy the output to tmpdir
    shutil.copytree("nmf_result", tmp_results_dir)

    # Remove the nmf_result folder from the top project level
    shutil.rmtree("nmf_result")

    # Define the specific JSON files to check
    json_files_to_check = [
        "component_index_vs_pratio_col.json",
        "component_index_vs_RE_value.json",
        "x_index_vs_y_col_components.json",
    ]

    # Compare each specified .json file
    for json_file in json_files_to_check:
        # Define paths for actual and expected .json files
        actual_file_path = join(tmp_results_dir, json_file)
        expected_file_path = join(expected_output_dir, json_file)

        # Ensure the file exists in both locations
        assert exists(actual_file_path)
        assert exists(expected_file_path)

        # Read and compare file contents
        with open(actual_file_path, "r") as actual_file:
            actual = actual_file.read()

        with open(expected_file_path, "r") as expected_file:
            expected = expected_file.read()

        # Assert that the contents match
        assert actual == expected
