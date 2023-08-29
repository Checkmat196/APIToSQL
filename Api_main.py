# Atividade
# API da Sportmonks:
# Configurar e extrair dados times
# Banco de Dados:
# Criar tabelas: Times (ID e nome)

import time

import openpyxl
import pandas as pd
import pyodbc
import requests
from pandas import json_normalize

# Parâmetros da conexão
SERVER = 'DESKTOP-295VC9D'
DATABASE = 'SPORTMONKS'
USERNAME = 'usuario'
PASSWORD = 'senha'

# Conexão com o SQL
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes'

conn = pyodbc.connect(connection_string)
cursor = conn.cursor()


# Conexão e Extração dos dados da API

URL = 'https://api.sportmonks.com/v3/football/teams'
TOKEN = 'jJDE36NINPPXX54ZJJvL0H5YjgumgRCVjnUdTNwsW6VkrBcq2YQsiCHrax3v'

URL_TOKEN = URL + '/?api_token=' + TOKEN

headers = {
    'Authorization': TOKEN
}

resposta = requests.get(URL_TOKEN)

if resposta.status_code == 200:
    dados = resposta.json()
    print(f"Sucesso, Api conectada: {resposta.status_code}")
else:
    print(f"Erro ao acessar a API. Status Code: {resposta.status_code}")
# print(resposta.text)
Normalize_Json = json_normalize(dados['data'])

time.sleep(2)

# Selecionando colunas Específicas

df_0 = Normalize_Json[['id', 'name']]

df_0 = df_0.rename(columns={
    'id': 'TEAM_ID',
    'name': 'TEAM_NAME'
})

print('Organização do Data Frame finalizada!')
time.sleep(2)

df = pd.DataFrame(df_0)

print('Gerando um arquivo para avaliar os dados')
time.sleep(2)
nome_do_arquivo = "meus_dados.xlsx"
df.to_excel(nome_do_arquivo, index=False, engine='openpyxl')
print("Tabela de times Disponível para criação")
time.sleep(2)
print('Criando a tabela')

with open('CREATE_API_SPORTMONKS_TEAMS.SQL', 'r') as file:
    sql_create_tables = file.read()
    cursor.execute(sql_create_tables)

conn.commit()
time.sleep(2)
print('Tebala Criada!')
time.sleep(2)
print('Inserindo os novos dados na tabela e atualizando os antigos.')
with open('MERGE_API_SPORTMONKS_TEAMS.SQL', 'r') as file:
    sql_merge = file.read()

for index, row in df.iterrows():
    cursor.execute(sql_merge, row['TEAM_ID'], row['TEAM_NAME'])

conn.commit()
time.sleep(2)
print('Inserção concluída!')
time.sleep(2)
print('Checando volumetria de times inserida')
sql_count = "select count(distinct TEAM_ID) from API_SPORTMONKS_TEAMS with (nolock)"
cursor.execute(sql_count)
number_of_teams = cursor.fetchone()[0]

print(f"{number_of_teams} Times foram inseridos.")
