# CertiBase

O software baseado em script Python foi desenvolvido com o objetivo de realizar comparações entre as cultivares do banco de dados (referências) e árvores de pecã específicas (consulta). O algoritmo realiza a comparação par a par da consulta com as referências e estima a similaridade genética (S) com base no erro percentual absoluto médio dos alelos em cada locus, onde q e r são os tamanhos dos alelos, em pares de bases, da consulta e da referência, respectivamente. A função ‘max’ é usada para limitar as estimativas de S entre 0,0 e 1,0, evitando estimativas negativas de S quando a consulta é comparada com cultivares geneticamente distantes, apresentando diferenças relativamente grandes em pares de bases entre os alelos. Por exemplo, se a consulta for uma amostra da cultivar Barton, a comparação com a referência Barton retornará valores de S próximos a 1,0, já que pequenas diferenças nos tamanhos dos alelos são aceitas.

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

**1.1 - Em seu terminal, navegue até o diretório do arquivo .py, exemplo:**
cd /caminho/para/o/diretorio

**1.2 - Execute o arquivo pyton:**
python3 CertiBase.py

**2.1 -Verifique se o Python está instalado no seu sistema**:
python3 --version

**2.2 - Caso não esteja instalado:**
sudo apt update
sudo apt install python3

**3.1 - Se você estiver usando um ambiente virtual (virtual environment), ative o ambiente antes de executar o arquivo:**                                                                          source /caminho/para/o/venv/bin/activate

**3.2 -** E então execute o passo **1.2** novamente.
