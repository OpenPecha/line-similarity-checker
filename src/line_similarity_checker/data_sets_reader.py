import multiprocessing
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import pandas as pd

from line_similarity_checker.config import ROOT_DIR
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

    def worker_similarity_check(self, dataset: Dict, other_dataset: Dict):
        score = check_line_similarity(
            dataset["file_content"], other_dataset["file_content"]
        )
        return {
            "Dataset_Name": dataset["dataset_name"],
            "Text_File_1": dataset["file_name"],
            "Dataset_Name_2": other_dataset["dataset_name"],
            "Text_File_2": other_dataset["file_name"],
            "Similarity_Score": score,
            "File_content_1": dataset["file_content"],
            "File_content_2": other_dataset["file_content"],
        }

    def generate_similarity_in_dataset(
        self, dataset_name: str, destination_dir: Path, threshold: float = 0.7
    ):
        tasks = []
        dataset = self.Datasets[dataset_name]
        text_files = dataset.text_files
        for idx in range(len(text_files)):
            text_file = list(text_files.keys())[idx]
            for j in range(idx + 1, len(text_files)):
                other_text_file = list(text_files.keys())[j]
                data_set = {
                    "dataset_name": dataset_name,
                    "file_name": text_file,
                    "file_content": text_files[text_file],
                }
                other_dataset = {
                    "dataset_name": dataset_name,
                    "file_name": other_text_file,
                    "file_content": text_files[other_text_file],
                }
                tasks.append((data_set, other_dataset))

        num_processes = multiprocessing.cpu_count()
        with multiprocessing.Pool(num_processes) as pool:
            results = pool.starmap(self.worker_similarity_check, tasks)

        # Filter results to include only those with similarity score above the threshold
        filtered_results = [
            result for result in results if result["Similarity_Score"] > threshold
        ]

        """writing results to csv with dataset name"""
        if filtered_results:
            pd.DataFrame(filtered_results).to_csv(
                destination_dir / f"{dataset_name}.csv", index=False
            )

    def generate_similarity_within_datasets(
        self, destination_dir: Path, threshold: float = 0.7
    ):
        dataset_names = list(self.Datasets.keys())
        for dataset_name in dataset_names:
            self.generate_similarity_in_dataset(
                dataset_name, destination_dir, threshold
            )

    def generate_similarity_across_datasets(
        self, destination_dir: Path, threshold: float = 0.7
    ):
        dataset_names = list(self.Datasets.keys())
        for i in range(len(dataset_names)):
            dataset_name = dataset_names[i]
            text_files = self.Datasets[dataset_name].text_files
            for text_file in text_files:
                tasks = []
                results = []
                for j in range(i + 1, len(dataset_names)):
                    other_dataset_name = dataset_names[j]
                    other_text_files = self.Datasets[other_dataset_name].text_files
                    for other_text_file in other_text_files:
                        dataset = {
                            "dataset_name": dataset_name,
                            "file_name": text_file,
                            "file_content": text_files[text_file],
                        }
                        other_dataset = {
                            "dataset_name": other_dataset_name,
                            "file_name": other_text_file,
                            "file_content": other_text_files[other_text_file],
                        }
                        tasks.append((dataset, other_dataset))

                # Processing the tasks with multiprocessing
                num_processes = multiprocessing.cpu_count()
                with multiprocessing.Pool(num_processes) as pool:
                    results.extend(pool.starmap(self.worker_similarity_check, tasks))

                # Filter results to include only those with similarity score above the threshold
                filtered_results = [
                    result
                    for result in results
                    if result["Similarity_Score"] > threshold
                ]

                # Writing results to CSV file
                if filtered_results:
                    output_file_name = f"{dataset_name}_{text_file}_vs_others.csv"
                    pd.DataFrame(filtered_results).to_csv(
                        destination_dir / output_file_name, index=False
                    )

    def generate_similarity_report(self, destination_dir: Path, threshold: float = 0.7):
        """line similarity within dataset"""
        self.generate_similarity_within_datasets(destination_dir, threshold)
        """line similarity between datasets"""
        if len(self.get_dataset_names()) >= 2:
            self.generate_similarity_across_datasets(destination_dir, threshold)

    def filter_by_similarity_threshold(
        self, report_file_path: Path, threshold: float, keep_the_files: bool = True
    ):
        report_data = pd.read_csv(report_file_path)
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

    start_time = time.time()
    data_sets = DatasetsReader(Path(ROOT_DIR / "LARGE_DATA" / "100files_into_2"))
    data_sets.generate_similarity_report(Path(ROOT_DIR), 0.5)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
