import tkinter as tk
from tkinter import filedialog
import pandas as pd

def isanumber(a):
    try:
        float(repr(a))
        bool_a = True
    except:
        bool_a = False
    return bool_a

# Função para calcular a similaridade genética entre duas linhas do DataFrame
def calcular_similaridade(query, reference):
    N = (len(query) - 1) // 2  # Número de loci
    similarity = 0

    for i in range(N):
        q = query[2*i + 1]  # Tamanho do alelo da query
        r = reference[2*i + 1]  # Tamanho do alelo da referência

        # Calculando a similaridade genética para cada loco
        loco_similarity = max(0, 1 - abs(q - r) / r)
        similarity += loco_similarity

    return similarity / N  # Similaridade média entre todos os loci

# Função para carregar o arquivo Excel e exibir o nome do arquivo selecionado
def carregar_arquivo(entry_widget):
    filename = filedialog.askopenfilename()
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, filename)

# Função para calcular a similaridade entre os arquivos Excel selecionados
def validar_similaridade():
    # Carregar os dados do banco de dados em Excel
    banco_de_dados_filename = entry_banco_de_dados.get()
    banco_de_dados = pd.read_excel(banco_de_dados_filename, engine='openpyxl', header=None)

    # Carregar os dados da única linha representando o cultivar de noz pecã
    query_filename = entry_query.get()
    query_df = pd.read_excel(query_filename, engine='openpyxl', header=None)

    similarities = {}

    # Calcular a similaridade entre a query e cada linha do banco de dados
    for index_query, query_row in query_df.iterrows():
        query_name = query_row[0]

        # remove row name
        query_row.pop(0)

        # remove not number values
        for k, v in query_row.items():
            if not isanumber(v):
                query_row.pop(k)

        for index_banco, banco_row in banco_de_dados.iterrows():
            db_name = banco_row[0]

            # remove row name
            banco_row.pop(0)

            # remove not number values
            for k, v in banco_row.items():
                if not isanumber(v):
                    banco_row.pop(k)

            # calculate similarity and add to similarities
            similarity = calcular_similaridade(query_row, banco_row)
            similarities[db_name] = similarity

    # MAGIC HAPPENS - short values by greater number
    similarities = dict(sorted(similarities.items(), key=lambda x:x[1], reverse=True)) # organiza pelo maior valor
    similarities = {k: similarities[k] for k in list(similarities)[:results_number]} # pega os maiores

    # get greater similarity name and value
    similarity_n = 0 # ignore
    for similarity in similarities.keys():
        similarity_value = similarities[similarity]
        result_text = results_texts[similarity_n]
        result_text.config(text=f"Similarity found \n {similarity}: {similarity_value * 100:.2f}%")
        similarity_n += 1
        if similarity_n > len(results_texts): break

    if not similarities:
        resultado_label.config(text="Não foi encontrada similaridade.")

# Configuração da interface gráfica
root = tk.Tk()
root.title("CertBase")

# Entrada para o arquivo do banco de dados
label_banco_de_dados = tk.Label(root, text="Select the database:")
label_banco_de_dados.grid(row=0, column=0, padx=10, pady=5)
entry_banco_de_dados = tk.Entry(root, width=50)
entry_banco_de_dados.grid(row=0, column=1, padx=10, pady=5)
btn_banco_de_dados = tk.Button(root, text="Select", command=lambda: carregar_arquivo(entry_banco_de_dados))
btn_banco_de_dados.grid(row=0, column=2, padx=10, pady=5)

# Entrada para o arquivo do cultivar
label_query = tk.Label(root, text="Select the crop file:")
label_query.grid(row=1, column=0, padx=10, pady=5)
entry_query = tk.Entry(root, width=50)
entry_query.grid(row=1, column=1, padx=10, pady=5)
btn_query = tk.Button(root, text="Select", command=lambda: carregar_arquivo(entry_query))
btn_query.grid(row=1, column=2, padx=10, pady=5)

# Botão para calcular a similaridade
btn_calcular = tk.Button(root, text="Calculate similarity", command=validar_similaridade)
btn_calcular.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

# Label para exibir o resultado da similaridade
results_number = 3 # numero de resultados a ser exibido
starting_row = 3 # row inicial do tk
results_texts = {} # objeto com os textos do tk
result_n = 0 # ignore
while result_n < results_number: # do the thing
    resultado_label = tk.Label(root, text="")
    resultado_label.grid(row=starting_row+result_n, column=0, columnspan=3, padx=10, pady=5)
    results_texts[result_n] = resultado_label
    result_n+=1

root.mainloop()
