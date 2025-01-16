#Neste script, iremos criar o grafico para projetar o resultado

import pandas as pd
import plotly.express as px

# Caminho do arquivo CSV
file_path = "results/thread_analysis_recursive.csv"

# Função para detectar o separador do CSV
def detect_separator(file_path):
    with open(file_path, 'r') as file:
        first_line = file.readline()
        if ';' in first_line:
            return ';'
        elif ',' in first_line:
            return ','
        else:
            raise ValueError("Separador não reconhecido. Verifique o arquivo.")

# Detectar o separador
separator = detect_separator(file_path)

# Carregar o CSV com o separador detectado
df = pd.read_csv(file_path, sep=separator)

# Verificar colunas e estados das threads
print("Colunas do CSV:", df.columns.tolist())
print(df.head())

# Filtrar threads em estado de bloqueio ou espera
blocked_threads = df[df['Thread State'].str.contains('WAITING|BLOCKED', case=False, na=False)]
print(f"Total de threads em estado de espera ou bloqueio: {len(blocked_threads)}")

# Gráfico de threads em bloqueio/espera ao longo do tempo
if not blocked_threads.empty:
    blocked_threads_grouped = blocked_threads.groupby('Timestamp').size().reset_index(name='Count')
    fig = px.line(blocked_threads_grouped, x='Timestamp', y='Count', title='Threads Waiting or Blocked Over Time', markers=True)
    fig.show()
else:
    print("Nenhuma thread em estado de bloqueio ou espera foi encontrada.")

# Gráfico de threads RUNNABLE ao longo do tempo
runnable_threads = df[df['Thread State'] == 'RUNNABLE'].groupby('Timestamp').size().reset_index(name='Count')
fig_runnable = px.line(runnable_threads, x='Timestamp', y='Count', title='Runnable Threads Over Time', markers=True)
fig_runnable.show()

# Exibir as 10 chamadas mais frequentes em threads bloqueadas
if not blocked_threads.empty:
    top_calls = blocked_threads['Last Call'].value_counts().head(10)
    print("\nTop 10 chamadas mais frequentes em threads bloqueadas ou em espera:")
    print(top_calls)

    # Salvar análise em CSV
    blocked_threads.to_csv('results/blocked_threads_analysis.csv', index=False)
    print("Arquivo 'blocked_threads_analysis.csv' gerado, podes acessar a pasta.")
