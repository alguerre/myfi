from src.commands.add_source_data.readers import Dummy


def test_dummy(sample_bank_history, sample_files):
    assert (
        Dummy().read(sample_files["dummy"]).drop(["origin"], axis=1).to_dict()
        == sample_bank_history.to_dict()
    )
