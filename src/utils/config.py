import yaml


def get_config(file: str) -> dict:
    with open(file) as f:
        return yaml.load(f, Loader=yaml.FullLoader)
