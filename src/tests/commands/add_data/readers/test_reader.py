from contextlib import nullcontext as does_not_raise

from pytest import mark, raises

from src.commands.add_data.error import InvalidFilenameError
from src.commands.add_data.readers import Reader, get_reader, identify_bank


@mark.parametrize(
    "filename,result,expectation",
    [
        ("source_santander_05062019_to_23072023.csv", "santander", does_not_raise()),
        ("source_bbva_05062019_to_23072023.csv", "bbva", does_not_raise()),
        ("source_bbva_02019_to_23073.csv", None, raises(InvalidFilenameError)),
    ],
)
def test_identify_bank(filename: str, result: str, expectation):
    with expectation:
        assert identify_bank(filename) == result


@mark.parametrize(
    "file,expectation",
    [
        ("source_santander_05062019_to_23072023.csv", raises(NotImplementedError)),
        ("source_sabadell_05062019_to_23072023.csv", does_not_raise()),
        ("source_n26_01012018_to_03012018.csv", does_not_raise()),
    ],
)
def test_get_reader(file: str, expectation):
    with expectation:
        reader = get_reader(file)
        assert isinstance(reader, Reader)
