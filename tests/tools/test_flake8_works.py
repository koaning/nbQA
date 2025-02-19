"""Check :code:`flake8` works as intended."""

import os
from textwrap import dedent
from typing import TYPE_CHECKING

import pytest

from nbqa.__main__ import main

if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture


@pytest.mark.parametrize(
    "path_0, path_1, path_2",
    (
        (
            os.path.abspath(
                os.path.join("tests", "data", "notebook_for_testing.ipynb")
            ),
            os.path.abspath(
                os.path.join("tests", "data", "notebook_for_testing_copy.ipynb")
            ),
            os.path.abspath(
                os.path.join("tests", "data", "notebook_starting_with_md.ipynb")
            ),
        ),
        (
            os.path.join("tests", "data", "notebook_for_testing.ipynb"),
            os.path.join("tests", "data", "notebook_for_testing_copy.ipynb"),
            os.path.join("tests", "data", "notebook_starting_with_md.ipynb"),
        ),
    ),
)
def test_flake8_works(
    path_0: str, path_1: str, path_2: str, capsys: "CaptureFixture"
) -> None:
    """
    Check flake8 works. Shouldn't alter the notebook content.

    Parameters
    ----------
    capsys
        Pytest fixture to capture stdout and stderr.
    """
    # check passing both absolute and relative paths

    main(["flake8", path_0, path_1, path_2])

    expected_path_0 = os.path.join("tests", "data", "notebook_for_testing.ipynb")
    expected_path_1 = os.path.join("tests", "data", "notebook_for_testing_copy.ipynb")
    expected_path_2 = os.path.join("tests", "data", "notebook_starting_with_md.ipynb")

    out, err = capsys.readouterr()
    expected_out = dedent(
        f"""\
        {expected_path_0}:cell_1:1:1: F401 'os' imported but unused
        {expected_path_0}:cell_1:3:1: F401 'glob' imported but unused
        {expected_path_0}:cell_1:5:1: F401 'nbqa' imported but unused
        {expected_path_0}:cell_2:19:9: W291 trailing whitespace
        {expected_path_0}:cell_4:1:1: E402 module level import not at top of file
        {expected_path_0}:cell_4:1:1: F401 'random.randint' imported but unused
        {expected_path_0}:cell_5:1:1: E402 module level import not at top of file
        {expected_path_0}:cell_5:2:1: E402 module level import not at top of file
        {expected_path_1}:cell_1:1:1: F401 'os' imported but unused
        {expected_path_1}:cell_1:3:1: F401 'glob' imported but unused
        {expected_path_1}:cell_1:5:1: F401 'nbqa' imported but unused
        {expected_path_2}:cell_1:1:1: F401 'os' imported but unused
        {expected_path_2}:cell_1:3:1: F401 'glob' imported but unused
        {expected_path_2}:cell_1:5:1: F401 'nbqa' imported but unused
        {expected_path_2}:cell_3:2:1: E302 expected 2 blank lines, found 0
        """
    )
    expected_err = ""
    assert sorted(out.splitlines()) == sorted(expected_out.splitlines())
    assert sorted(err.splitlines()) == sorted(expected_err.splitlines())
