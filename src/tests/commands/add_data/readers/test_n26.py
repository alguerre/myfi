from src.commands.add_data.readers import N26


def test_n26(sample_bank_history, sample_files):
    assert (
        N26().read(sample_files["n26"]).drop(["origin", "total"], axis=1).to_dict()
        == sample_bank_history.drop(["total"], axis=1).to_dict()
    )
