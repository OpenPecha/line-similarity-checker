from config import DATA_DIR
from pandas import DataFrame

from line_similarity_checker.data_sets_reader import DatasetsReader


def test_report_generator():
    datasets_reader = DatasetsReader(DATA_DIR)
    report = datasets_reader.generate_similarity_report()

    assert isinstance(report, DataFrame)
    assert set(report.columns.tolist()) == {
        "Text_File_2",
        "Similarity_Score",
        "Dataset_Name",
        "Dataset_Name_2",
        "Text_File_1",
    }
