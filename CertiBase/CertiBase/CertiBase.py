import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np

def isanumber(a):
    try:
        float(a)
        return True
    except (ValueError, TypeError):
        return False

# Função para calcular a similaridade genética entre duas linhas do DataFrame
def calcular_similaridade(query, reference):
    total_similarity = 0
    valid_loci_count = 0

    for q, r in zip(query, reference):
        if isanumber(q) and isanumber(r) and not (np.isnan(float(q)) or np.isnan(float(r))):
            q = float(q)
            r = float(r)
            loco_similarity = max(0, 1 - abs(q - r) / r)
            total_similarity += loco_similarity
            valid_loci_count += 1

    if valid_loci_count == 0:
        return 0

    return total_similarity / valid_loci_count

# Função para carregar o arquivo Excel e exibir o nome do arquivo selecionado
def carregar_arquivo(entry_widget):
    filename = filedialog.askopenfilename()
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, filename)

# Função para calcular a similaridade entre os arquivos Excel selecionados
def validar_similaridade():
    banco_de_dados_filename = entry_banco_de_dados.get()
    banco_de_dados = pd.read_excel(banco_de_dados_filename, engine='openpyxl', header=None)

    query_filename = entry_query.get()
    query_df = pd.read_excel(query_filename, engine='openpyxl', header=None)

    similarities = {}

    for index_query, query_row in query_df.iterrows():
        query_name = query_row.iloc[0]
        query_row = query_row.iloc[1:]

        for index_banco, banco_row in banco_de_dados.iterrows():
            db_name = banco_row.iloc[0]
            banco_row = banco_row.iloc[1:]

            similarity = calcular_similaridade(query_row, banco_row)
            similarities[db_name] = similarity

    similarities = dict(sorted(similarities.items(), key=lambda x: x[1], reverse=True))
    similarities = {k: similarities[k] for k in list(similarities)[:results_number]}

    similarity_n = 0
    for similarity in similarities.keys():
        similarity_value = similarities[similarity]
        result_text = results_texts[similarity_n]
        result_text.config(text=f"Similarity found: {similarity}: {similarity_value * 100:.2f}%")
        similarity_n += 1
        if similarity_n >= len(results_texts): break

    if not similarities:
        resultado_label.config(text="Não foi encontrada similaridade.")

root = tk.Tk()
root.title("CertBase")

label_banco_de_dados = tk.Label(root, text="Select the database:")
label_banco_de_dados.grid(row=0, column=0, padx=10, pady=5)
entry_banco_de_dados = tk.Entry(root, width=50)
entry_banco_de_dados.grid(row=0, column=1, padx=10, pady=5)
btn_banco_de_dados = tk.Button(root, text="Select", command=lambda: carregar_arquivo(entry_banco_de_dados))
btn_banco_de_dados.grid(row=0, column=2, padx=10, pady=5)

label_query = tk.Label(root, text="Select the crop file:")
label_query.grid(row=1, column=0, padx=10, pady=5)
entry_query = tk.Entry(root, width=50)
entry_query.grid(row=1, column=1, padx=10, pady=5)
btn_query = tk.Button(root, text="Select", command=lambda: carregar_arquivo(entry_query))
btn_query.grid(row=1, column=2, padx=10, pady=5)

btn_calcular = tk.Button(root, text="Calculate similarity", command=validar_similaridade)
btn_calcular.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

results_number = 3
starting_row = 3
results_texts = {}
result_n = 0
while result_n < results_number:
    resultado_label = tk.Label(root, text="")
    resultado_label.grid(row=starting_row + result_n, column=0, columnspan=3, padx=10, pady=5)
    results_texts[result_n] = resultado_label
    result_n += 1

root.mainloop()
