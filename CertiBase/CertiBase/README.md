# CertiBase

The Python script-based software was developed to perform comparisons between cultivars from the database (references) and specific pecan trees (queries). The algorithm pairwise compares each query with the references and estimates the genetic similarity (S) based on the mean absolute percent error of alleles at each locus, where q and r are the allele sizes in base pairs for the query and reference, respectively. The 'max' function is used to constrain the estimates of S between 0.0 and 1.0, preventing negative estimates of S when the query is compared with genetically distant cultivars that exhibit relatively large differences in allele sizes. For example, if the query is a sample from the Barton cultivar, comparison with the Barton reference will return S values close to 1.0, as small differences in allele sizes are tolerated.

## Requirements

[Python 3](https://www.python.org/downloads/)

- Python3
- python3-tk
- pip3

## Configuring

```sh
pip3 install -r requirements.txt
```

## Running

```sh
python3 CertiBase.py
```

## How to Use

**1 - Download the folder containing all files within this repository:**
CertiBase.py
.editorconfig
Banco de Dados.xlsx
README.md
requirements.txt

**1.1 - In your terminal, navigate to the directory of the .py file, for example:**
cd /path/to/the/directory/where/you/saved/the/repository/folder

You can use "ls" in your terminal to display the files available in your directory as you use "cd" to enter the directory.

**1.2 - Execute the Python file in the terminal:**
python3 CertiBase.py

**2.1 - If there is an error, check if Python is installed on your system:**
python3 --version

**2.2 - If it is not installed:**
sudo apt update
sudo apt install python3

**3.1 - If you are using a virtual environment, activate the environment before running the file:**                                                                          source /path/to/the/venv/bin/activate

**3.2 -** Execute step **1.2** again.
