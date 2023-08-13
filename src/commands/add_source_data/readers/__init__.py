from os.path import basename

from .base import Reader
from .bbva import Bbva
from .dummy import Dummy
from .n26 import N26
from .sabadell import Sabadell
from .utils import identify_bank

_readers = {
    "bbva": Bbva(),
    "dummy": Dummy(),
    "n26": N26(),
    "sabadell": Sabadell(),
}


def get_reader(file: str) -> Reader:
    bank = identify_bank(filename=basename(file))
    try:
        return _readers[bank.lower()]
    except KeyError:
        raise NotImplementedError(f"Not available reader for [{bank}]")
