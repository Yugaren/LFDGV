# CertiBase

The Python script-based software was developed to perform comparisons between cultivars from the database (references) and specific pecan trees (queries). The algorithm pairwise compares each query with the references and estimates the genetic similarity as<img src="https://github.com/Yugaren/LFDGV/assets/137843836/635d1a41-9fda-4fa2-be18-75281b2cdc4c" alt="image" style="width: 18%; height: auto;">
based on the mean absolute percent error of alleles at each locus, where q and r are the allele sizes in base pairs for the query and reference, respectively. The 'max' function is used to constrain the estimates of S between 0.0 and 1.0, preventing negative estimates of S when the query is compared with genetically distant cultivars that exhibit relatively large differences in allele sizes. For example, if the query is a sample from the Barton cultivar, comparison with the Barton reference will return S values close to 1.0, as small differences in allele sizes are tolerated.

## How to Use

**1 - Download the folder containing all files within this repository:**

- CertiBase.py
- .editorconfig
- Banco de Dados.xlsx
- README.md
- requirements.txt


**2 - Check if Python is installed on your system:**

```sh
python3 --version
```

**2.1 - If it is not installed:**

```sh
sudo apt update
```
```sh
sudo apt install python3
```

Or download here: 
- [Python 3](https://www.python.org/downloads/)


**2.2 - If you are using a virtual environment, activate the environment before running the file:**                                                                 

```sh
source /path/to/the/venv/bin/activate
```

**3 - To configure, type:**

```sh
pip3 install -r requirements.txt
```

**4 - In your terminal, navigate to the directory of the .py file, for example:**

```sh
cd /path/to/the/directory/where/you/saved/the/repository/folder
```

You can use **"ls"** in your terminal to display the files available in your directory as you use **"cd"** to enter the directory.

```sh
ls
```

**5 - Execute the Python file in the terminal:**
```sh
python3 CertiBase.py
```
