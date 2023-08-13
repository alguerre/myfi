from src.commands.add_data.readers import Sabadell


def test_sabadell(sample_bank_history, sample_files):
    assert (
        Sabadell().read(sample_files["sabadell"]).drop(["origin"], axis=1).to_dict()
        == sample_bank_history.to_dict()
    )
