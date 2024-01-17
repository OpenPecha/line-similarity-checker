from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import pandas as pd

from line_similarity_checker.config import DOWNLOADS_DIR
from line_similarity_checker.similarity_checker import check_line_similarity


@dataclass
class DataSet:
    text_files: Dict[str, str]

    def __init__(self, data_set_dir: Path):
        if not data_set_dir.exists():
            raise FileNotFoundError(f"DataSet directory not found: {data_set_dir}")
        self.load_text_files(data_set_dir)

    def load_text_files(self, data_set_dir: Path):
        self.text_files = {}
        for text_file in data_set_dir.rglob("*.txt"):
            if text_file.is_file():
                with open(text_file, encoding="utf-8") as f:
                    self.text_files[text_file.stem] = f.read()

    def get_text_file_names(self):
        return list(self.text_files.keys())

    def get_text(self, text_file_name: str) -> str:
        return self.text_files[text_file_name]


@dataclass
class DatasetsReader:
    Datasets: Dict[str, DataSet]

    def __init__(self, data_set_dir: Path):
        if not data_set_dir.exists():
            raise FileNotFoundError(f"DataSet directory not found: {data_set_dir}")
        self.load_datasets(data_set_dir)

    def load_datasets(self, data_set_dir: Path):
        self.Datasets = {}
        for dataset_dir in data_set_dir.iterdir():
            if dataset_dir.is_dir():
                self.Datasets[dataset_dir.stem] = DataSet(dataset_dir)

    def get_dataset_names(self):
        return list(self.Datasets.keys())

    def get_dataset(self, dataset_name: str) -> DataSet:
        return self.Datasets[dataset_name]

    def generate_similarity_report(self):
        report_data = []

        for dataset_name, dataset in self.Datasets.items():
            for file_name, text in dataset.text_files.items():
                for other_dataset_name, other_dataset in self.Datasets.items():
                    for other_file_name, other_text in other_dataset.text_files.items():
                        if (
                            dataset_name == other_dataset_name
                            and file_name == other_file_name
                        ):
                            continue  # Skip comparing the file with itself
                        score = check_line_similarity(text, other_text, normalized=True)
                        report_data.append(
                            {
                                "Dataset_Name": dataset_name,
                                "Text_File_1": file_name,
                                "Dataset_Name_2": other_dataset_name,
                                "Text_File_2": other_file_name,
                                "Similarity_Score": score,
                            }
                        )

        return pd.DataFrame(report_data)

    def filter_by_similarity_threshold(self, threshold: float):
        report_data = self.generate_similarity_report()

        # List to store pairs of files exceeding the threshold
        files_pairs_exceeding_threshold = []

        # Iterate through the report data
        for entry in report_data.itertuples():
            if entry.Similarity_Score > threshold:
                file_pair = {
                    "Dataset_Name": entry.Dataset_Name,
                    "Text_File_1": entry.Text_File_1,
                    "Dataset_Name_2": entry.Dataset_Name_2,
                    "Text_File_2": entry.Text_File_2,
                    "Similarity_Score": entry.Similarity_Score,
                }
                files_pairs_exceeding_threshold.append(file_pair)

        return pd.DataFrame(files_pairs_exceeding_threshold)


if __name__ == "__main__":
    data_sets = DatasetsReader(Path(DOWNLOADS_DIR))
    threshold = 0.4  # Example threshold
    filtered_report = data_sets.filter_by_similarity_threshold(threshold)
    print(filtered_report)
