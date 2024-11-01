import os
import tempfile
from pathlib import Path
from shutil import rmtree

import pytest

from diffpy.nmf_mapping.main import main

dir = Path(__file__).parent.resolve()

data_dir = os.path.join(dir, "data/synthetic_r_vs_gr")

test_map = [
    ([data_dir, "--xrange", "5,10"], "output_1", "Number of components: 3\n"),
    ([data_dir], "output_2", "Number of components: 3\n"),
    ([data_dir, "--xrange", "5,10", "12,15"], "output_3", "Number of components: 3\n"),
]


@pytest.fixture(scope="session")
def temp_dir():
    """A test fixture that creates and destroys tes outputs in a temporary
    directory.
    This will yield the path to the directory.
    """
    cwd = os.getcwd()
    name = "outputs"
    temp_dir = Path(tempfile.gettempdir())
    repo = os.path.join(temp_dir, name)
    if os.path.exists(repo):
        rmtree(repo)
    os.chdir(temp_dir)
    os.mkdir(name)
    os.chdir(cwd)
    yield repo
    os.chdir(cwd)
    rmtree(repo)


@pytest.mark.parametrize("tm", test_map)
def test_nmf_mapping_code(tm, temp_dir, capsys):
    data_dir = tm[0]
    working_dir = Path(temp_dir)
    os.chdir(working_dir)
    main(args=data_dir)
    out, err = capsys.readouterr()
    assert out == tm[2]
    results_dir = os.path.join(working_dir, "nmf_result")
    os.chdir(results_dir)
    expected_base = os.path.join(os.path.dirname(__file__), "output")
    test_specific_dir = os.path.join(expected_base, tm[1])
    for root, dirs, files in os.walk("."):
        for file in files:
            if file in os.listdir(test_specific_dir):
                fn1 = os.path.join(results_dir, file)
                with open(fn1, "r") as f:
                    actual = f.read()
                fn2 = os.path.join(test_specific_dir, file)
                with open(fn2, "r") as f:
                    expected = f.read()
                assert expected == actual
