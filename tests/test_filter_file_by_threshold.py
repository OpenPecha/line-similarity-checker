from config import DATA_DIR

from line_similarity_checker.data_sets_reader import DatasetsReader


def test_filter_by_threshold():
    data_sets = DatasetsReader(DATA_DIR)
    threshold = 0.4
    filtered_report = data_sets.filter_by_similarity_threshold(
        threshold, keep_the_files=True
    )
    # Assert that all similarity scores are greater than the threshold
    assert all(filtered_report["Similarity_Score"] >= threshold)
