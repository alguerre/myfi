from src.commands.add_data.readers import Bbva


def test_bbva(sample_bank_history, sample_files):
    assert (
        Bbva().read(sample_files["bbva"]).drop(["origin"], axis=1).to_dict()
        == sample_bank_history.to_dict()
    )
