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
    data_sets_path: Path

    def __init__(self, data_set_dir: Path):
        if not data_set_dir.exists():
            raise FileNotFoundError(f"DataSet directory not found: {data_set_dir}")
        self.data_sets_path = data_set_dir
        self.load_datasets()

    def load_datasets(self):
        self.Datasets = {}
        for dataset_dir in self.data_sets_path.iterdir():
            if dataset_dir.is_dir():
                self.Datasets[dataset_dir.stem] = DataSet(dataset_dir)

    def get_dataset_names(self):
        return list(self.Datasets.keys())

    def get_dataset(self, dataset_name: str) -> DataSet:
        return self.Datasets[dataset_name]

    def generate_similarity_report(self):
        report_data = []
        distinct_files = []
        for dataset_name, dataset in self.Datasets.items():
            for file_name, text in dataset.text_files.items():
                distinct_files.append(
                    {"dataset_name": dataset_name, "file_name": file_name, "text": text}
                )

        for i in range(len(distinct_files)):
            for j in range(i + 1, len(distinct_files)):
                file = distinct_files[i]
                other_file = distinct_files[j]

                score = check_line_similarity(
                    file["text"], other_file["text"], normalized=True
                )
                report_data.append(
                    {
                        "Dataset_Name": file["dataset_name"],
                        "Text_File_1": file["file_name"],
                        "Dataset_Name_2": other_file["dataset_name"],
                        "Text_File_2": other_file["file_name"],
                        "Similarity_Score": score,
                    }
                )

        return pd.DataFrame(report_data)

    def filter_by_similarity_threshold(
        self, threshold: float, keep_the_files: bool = True
    ):
        report_data = self.generate_similarity_report()
        filtered_data = report_data[report_data["Similarity_Score"] >= threshold]

        if not keep_the_files:
            deleted_files = set()
            for entry in filtered_data.itertuples():
                dataset_path_1 = Path(self.data_sets_path, entry.Dataset_Name)
                dataset_path_2 = Path(self.data_sets_path, entry.Dataset_Name_2)

                files_1 = list(dataset_path_1.rglob(f"{entry.Text_File_1}.txt"))
                files_2 = list(dataset_path_2.rglob(f"{entry.Text_File_2}.txt"))

                file_path_1 = files_1[0] if files_1 else None
                file_path_2 = files_2[0] if files_2 else None

                # Check if either of the files has already been deleted or if they do not exist
                if (not file_path_1 or file_path_1 in deleted_files) or (
                    not file_path_2 or file_path_2 in deleted_files
                ):
                    continue

                # Choose one file to delete, for example, file_path_1
                if file_path_1 and file_path_1.exists():
                    file_path_1.unlink()  # Delete the file
                    deleted_files.add(file_path_1)
                    print(f"Deleted file: {entry.Dataset_Name}/{entry.Text_File_1}.txt")
                    continue
                elif file_path_2 and file_path_2.exists():
                    file_path_2.unlink()  # Delete the file
                    deleted_files.add(file_path_2)
                    print(
                        f"Deleted file: {entry.Dataset_Name_2}/{entry.Text_File_2}.txt"
                    )

        return filtered_data


if __name__ == "__main__":
    data_sets = DatasetsReader(Path(DOWNLOADS_DIR))
    report = data_sets.generate_similarity_report()
    report.to_csv("report.csv", index=False)
