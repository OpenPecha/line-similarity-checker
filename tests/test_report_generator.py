from config import DATA_DIR
from pandas import DataFrame

from line_similarity_checker.data_sets_reader import DatasetsReader


def test_report_generator():
    datasets_reader = DatasetsReader(DATA_DIR)
    report = datasets_reader.generate_similarity_report()

    assert isinstance(report, DataFrame)
    assert set(report.columns.tolist()) == {
        "Text File 2",
        "Similarity Score",
        "Dataset Name",
        "Dataset Name 2",
        "Text File 1",
    }


test_report_generator()
