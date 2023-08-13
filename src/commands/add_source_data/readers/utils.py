import re

from src.commands.add_source_data.error import InvalidFilenameError


def identify_bank(filename: str) -> str:
    regex = r"source_(?P<bank>\w+)_\d{8}_to_\d{8}.(csv|xls)$"
    match = re.search(regex, filename)

    if match:
        return match.group("bank")
    raise InvalidFilenameError(
        f"The provided file [{filename}] do not follow the required format [{regex}]"
    )
