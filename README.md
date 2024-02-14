
<h1 align="center">
  <br>
  <a href="https://openpecha.org"><img src="https://avatars.githubusercontent.com/u/82142807?s=400&u=19e108a15566f3a1449bafb03b8dd706a72aebcd&v=4" alt="OpenPecha" width="150"></a>
  <br>
</h1>

<!-- Replace with 1-sentence description about what this tool is or does.-->


<h3 align="center">line-similarity-checker</h3>

## Description

Package for checking text similarity between txt files.This project is actually built to filter out identical or very similar lines in OCR Training data.


## Project owner(s)


- [@tenzin3](https://github.com/tenzin3)

## Integrations


None
## Docs

Edit distance is a measure of similarity between two strings, quantified as the minimum number of operations required to transform one string into the other. The operations typically include insertions, deletions, or substitutions of a single character.

In this project, [damerauLevenshtein](https://pypi.org/project/fastDamerauLevenshtein/
) is used for measuring edit distance.




## Installation


```bash
  pip install git+https://github.com/OpenPecha/line-similarity-checker.git
```
  
A python package known as line_similarity_checker would be installed in your environment.
## Usage/Examples

#### 1.Checking similarity b/w two lines
```python

from line_similarity_checker.similarity_checker import check_line_similarity

line1 = "ང་བོད་པ་ཡིན།"
line2 = "ང་བོད་པ་ཡིན།"

similarity_score = check_line_similarity(line1, line2,normalized=False)
normalized_similarity_score = check_line_similarity(line1, line2, normalized=True)


print(similarity_score)                     #1.0
print(normalized_similarity_score)          #0.9166666
```

Above is a way to check simlarity between two lines, similarity score shows how many operations need to be done to achieve a same line. This score is then normalized in range of 0-1. Normalized similarity score is useful in filtering with threshold, which we would see later on.

#### 2.Checking similarity in data sets
```python

from line_similarity_checker.data_sets_reader import DatasetsReader

data_sets = DatasetsReader(Path("data_dir"))
data_sets.generate_similarity_report(Path("output_dir"), 0.7)
```
Above code, first, read the datasets given "data_dir", then it generates the similarity report. "0.7" is given as a threshold such that it would only store result equal or greater than that.

In most cases, there are batches of folder, and each folder has multiples text files as well.The package perform within datasets first, and then it compares similarity across dataset.

Naming convention:

i)Within dataset: "data_set_folder_name".csv      Eg: batch1.csv, batch2.csv

ii)Across dataset: "data_set_folder_name"_"text_file_name"_vs_others.csv      Eg: batch 1_1-1-4a_line_9874_1_vs_others.csv

#### Input 
![image](https://github.com/OpenPecha/line-similarity-checker/assets/52460417/f4c6384b-a3f8-48b7-935f-729115c917de)

#### Output
![image](https://github.com/OpenPecha/line-similarity-checker/assets/52460417/f5587687-8caa-457d-9c5a-92e5d58c7a6c)


