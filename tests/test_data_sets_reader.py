from config import DATA_DIR

from line_similarity_checker.data_sets_reader import DatasetsReader


def test_datasets_reader():
    data_sets_reader = DatasetsReader(DATA_DIR)
    datasets = data_sets_reader.get_dataset_names()
    assert set(datasets) == {"batch 1", "batch 2", "batch 3"}

    batch_1 = data_sets_reader.get_dataset("batch 1")
    assert len(batch_1.text_files) == 3

    text_file_names = batch_1.get_text_file_names()
    assert set(text_file_names) == {
        "1-1-4a_line_9874_2",
        "1-1-4a_line_9874_3",
        "1-1-4a_line_9874_1",
    }

    text = batch_1.get_text("1-1-4a_line_9874_1")
    assert (
        text
        == "བདག་གི་ཁར་སྦྲེངས་ནས་འདུག་གོ །ཨང་གའི་རྒྱལ་པོས་རྒྱལ་པོ་པདྨ་ཆེན་པོ་ལ་ཕོ་ཉ་བཏང་སྟེ། གལ་ཏེ་ཕྱིར་འབྱུང་ན་དེ་ལྟ་ན་ལེགས། གལ་ཏེ་ཕྱིར་མི་འབྱུང་ན། ཇི་སྟེ་སྟེང་གི་ནམ་མཁའ་ལ་འགྲོ་ན་ནི།"  # noqa
    )

    text = batch_1.get_text("1-1-4a_line_9874_2")
    assert (
        text
        == "མདའ་བརྒྱུད་པས་ཁྱོད་ལྟུང་བར་བྱའོ། །ཇི་སྟེ་སའི་འོག་ཏུ་འགྲོ་ན་ནི། མཆིལ་པ་དང་འདྲ་བའི་ཚུལ་གྱིས་དྲང་བར་བྱའོ། །ཇི་སྟེ་རིའི་རྩེ་མོར་འཛེག་ན་ནི་དེར་ཡང་ཁྱོད་ཐར་པ་མེད་དོ། །ཞེས་སྤྲིང་ངོ༌། །རྒྱལ་"  # noqa
    )

    text = batch_1.get_text("1-1-4a_line_9874_3")
    assert (
        text
        == "པོ་པདྨ་ཆེན་པོས་འཕྲིན་ཡིག་བླངས་ནས། དེ་མི་བདེ་བར་གྱུར་ཏེ། ལག་པ་འགྲམ་པ་ལ་བསྟད་ནས། སེམས་ཁོང་དུ་ཆུད་ཅིང་འདུག་འདུག་ནས། དེས་བློན་པོ་རྣམས་ལ་སྨྲས་པ། ཤེས་ལྡན་དག་ཨང་"  # noqa
    )


test_datasets_reader()
