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

    first_row = report.iloc[0]
    assert first_row["Dataset Name"] == "batch 1"
    assert first_row["Text File 1"] == "1-1-4a_line_9874_2"
    assert first_row["Dataset Name 2"] == "batch 1"
    assert first_row["Text File 2"] == "1-1-4a_line_9874_3"
    assert first_row["Similarity Score"] == 0.26373626373626374


test_report_generator()
