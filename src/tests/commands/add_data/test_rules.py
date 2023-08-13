from unittest.mock import patch

import pandas as pd
from pytest import fixture

from src.commands.add_data.rules import Rules


@fixture()
def simple_rules() -> Rules:
    with patch("src.commands.add_data.rules.get_config") as config:
        config.return_value = {
            "EXCLUDE": [{"concept": "Europe"}],
            "SAVINGS": [{"concept": "America"}],
        }
        r = Rules()

    return r


@fixture()
def compose_rules() -> Rules:
    with patch("src.commands.add_data.rules.get_config") as config:
        config.return_value = {
            "EXCLUDE": [{"concept": "Europe", "origin": "bbva"}],
            "SAVINGS": [{"concept": "America", "origin": "santander"}],
        }
        r = Rules()

    return r


def test_rules_exclude(simple_rules):
    data = pd.DataFrame({"concept": ["Europe", "America", "Europe"]})
    assert simple_rules.exclude(data).to_dict("list") == {"concept": ["America"]}


def test_rules_exclude__invalid_rule(simple_rules):
    data = pd.DataFrame({"origin": ["a", "b", "c"]})
    assert all(simple_rules.exclude(data) == data)


def test_rules_savings(simple_rules):
    data = pd.DataFrame(
        {"concept": ["Europe", "America", "Europe"], "amount": [3, 4, 5]}
    )
    assert simple_rules.savings(data).to_dict("list") == {
        "concept": ["Europe", "America", "Europe"],
        "amount": [3, 0, 5],
    }


def test_rules_apply(simple_rules):
    data = pd.DataFrame(
        {"concept": ["Europe", "America", "Europe"], "amount": [3, 4, 6]}
    )
    assert simple_rules.apply(data).to_dict("list") == {
        "concept": ["America"],
        "amount": [0],
    }


def test_rules_exclude__compose_rules(compose_rules):
    data = pd.DataFrame(
        {
            "concept": ["Europe", "America", "Europe"],
            "origin": ["bbva", "bank1", "bank2"],
        }
    )
    assert compose_rules.exclude(data).to_dict("list") == {
        "concept": ["America", "Europe"],
        "origin": ["bank1", "bank2"],
    }


def test_rules_savings__compose_rules(compose_rules):
    data = pd.DataFrame(
        {
            "concept": ["Europe", "America", "Europe"],
            "amount": [3, 4, 5],
            "origin": ["bank", "santander", "bank"],
        }
    )
    assert compose_rules.savings(data).to_dict("list") == {
        "concept": ["Europe", "America", "Europe"],
        "amount": [3, 0, 5],
        "origin": ["bank", "santander", "bank"],
    }
