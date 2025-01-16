
#script versão 4##
import os
import pandas as pd

# Função para processar arquivos de thread dumps, incluindo subpastas
def processo_thread_dumps(directory):
    rows = []  # Lista para guardar as informações das threads

    # Percorrer todas as pastas e arquivos dentro do diretório
    for root, _, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)  # Caminho completo do arquivo

            if os.path.isfile(file_path):  # Verifica se é um arquivo
                with open(file_path, 'r') as file:
                    lines = file.readlines()  # Lê todas as linhas do arquivo

                timestamp = lines[0].strip()  # Pega o timestamp (primeira linha)

                current_thread = {}
                for line in lines:
                    if line.startswith('"'):  # Nova thread detectada
                        if current_thread:  # Salva a thread anterior
                            rows.append(current_thread)
                        thread_name = line.split('"')[1]  # Nome da thread
                        current_thread = {"Timestamp": timestamp, "Thread Name": thread_name}

                    # Identificar as colunas 'Last Call' e 'Custom Call'
                    elif "java.lang.Thread.State" in line:
                        current_thread["Thread State"] = line.split(":")[-1].strip()
                    elif "at " in line and not current_thread.get("Last Call"):
                        last_call = line.strip()
                        current_thread["Last Call"] = last_call
                        current_thread["Custom Call"] = "No"  # Marcado como "No" por padrão

                if current_thread:
                    rows.append(current_thread)

    # Retornar DataFrame pandas
    return pd.DataFrame(rows)

# Diretório principal que contém subpastas
directory = "C:/Users/wagner.n.santos/Documents/thread-dump-analysis/crossjoin_td_test"

# Processar e salvar os resultados
df = processo_thread_dumps(directory)
df.to_csv("results/thread_analysis_recursive.csv", index=False)

print("Arquivo gerado! Gravou na pasta resultados.")
