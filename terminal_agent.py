import os 
from dotenv import load_dotenv
import openai
import mysql.connector

load_dotenv ()

host = os.getenv('host')
password = os.getenv('password')
port = os.getenv('port')
user = os.getenv('user')
database = os.getenv('database')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

conn = mysql.connector.connect(
    host= host,
    user= user,
    password= password,
    database= database,
    port= port
)

cursor = conn.cursor()

cursor.execute('SHOW TABLE')

tabelas = cursor.fetchall()
colunas = {}
for tabela in tabelas:
    cursor.execute(f"DESCRIBE {tabelas[0]};")
    colunas_tabelas = cursor.fetchall()
    colunas[tabela[0]] = [coluna[0] for coluna in colunas_tabelas]
    
    cursor.close()
    conn.close()

#construir a nossa inteligencia artificial

prompt = f"""
você é uma assistente de SQL que opera para o banco de dados ficticio chamado Dio Bank.
Vocé deve gerar queries baseadas na seguinte estrutura do banco de dados:
{colunas}
pergunta: {input("faça a sua pergunta:")}
resposta em SQL:

"""

openai.api_key = OPENAI_API_KEY

response = openai.ChatCompletion.create(
    model = 'gpt-4.1',
    menssages = [{'role': 'system', 'content': 'Você é um assistente de SQL'},
                {'role': 'user', 'content': prompt}],
    max_tokens = 150,
    temperature = 0 #quanto mais proximo do 0, maior vai ser a sua deterministica e quanto mais longe do 0 e mais perto do 1 ele vai ser completamente alucinada
    )

query_gerada = response['choices'][0]['message']['content']

query_gerada = query_gerada.replace("'''sql''' ","").replace("'''","")

if query_gerada.lower().startswith('sql'):
    query_gerada = query_gerada[3:].strip()
    
   conn = mysql.connector.connect(
    host= host,
    user= user,
    password= password,
    database= database,
    port= port
)