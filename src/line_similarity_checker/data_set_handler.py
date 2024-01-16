from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from line_similarity_checker.config import DOWNLOADS_DIR


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


if __name__ == "__main__":
    data_sets = DatasetsReader(Path(DOWNLOADS_DIR))
