# Primeira etapa: importar as bibliotecas relevantes
import random
import mysql.connector
from faker import Faker

# Criar conexão com o banco de dados MySQL
conn = mysql.connector.connect(
    host='sql10.freesqldatabase.com',
    user='sql10794055',
    password='Gr7uAeyKGM',
    database='sql10794055',
    port=3306
)

cursor = conn.cursor()

# Tabela clientes
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    cliente_id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    cpf VARCHAR(11),
    email VARCHAR(100)
)
""")

# Tabela enderecos
cursor.execute("""
CREATE TABLE IF NOT EXISTS enderecos (
    endereco_id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    rua VARCHAR(255),
    cidade VARCHAR(100),
    estado VARCHAR(50),
    cep VARCHAR(8),
    FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id)
)
""")

# Tabela pagamentos
cursor.execute("""
CREATE TABLE IF NOT EXISTS pagamentos (
    pagamento_id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    valor DECIMAL(10, 2),
    data_pagamento DATE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id)
)
""")

# Tabela movimentacoes
cursor.execute("""
CREATE TABLE IF NOT EXISTS movimentacoes (
    movimentacao_id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    tipo_movimentacao VARCHAR(50),
    valor DECIMAL(10, 2),
    data_movimentacao DATE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id)
)
""")

# Instanciar gerador de dados falsos
fake = Faker()

# Gerar e inserir dados falsos
for i in range(1000):
    nome = fake.name()
    cpf = str(random.randint(11111111111, 99999999999))
    email = fake.email()

    rua = fake.street_address()
    cidade = fake.city()
    estado = fake.state()
    cep = fake.zipcode()

    tipo_movimentacao = random.choice(['depósito', 'pix', 'crédito', 'empréstimo', 'título', 'transferência'])
    valor_movimentacao = round(random.uniform(50.0, 10000.0), 2)
    data_movimentacao = fake.date_this_year()

    valor_pagamento = round(random.uniform(50.0, 10000.0), 2)
    data_pagamento = fake.date_this_year()

    # Inserir cliente
    cursor.execute("""
        INSERT INTO clientes (nome, cpf, email)
        VALUES (%s, %s, %s)
    """, (nome, cpf, email))

    client_id = cursor.lastrowid

    # Inserir endereço
    cursor.execute("""
        INSERT INTO enderecos (cliente_id, rua, cidade, estado, cep)
        VALUES (%s, %s, %s, %s, %s)
    """, (client_id, rua, cidade, estado, cep))

    # Inserir movimentação
    cursor.execute("""
        INSERT INTO movimentacoes (cliente_id, tipo_movimentacao, valor, data_movimentacao)
        VALUES (%s, %s, %s, %s)
    """, (client_id, tipo_movimentacao, valor_movimentacao, data_movimentacao))

    # Inserir pagamento
    cursor.execute("""
        INSERT INTO pagamentos (cliente_id, valor, data_pagamento)
        VALUES (%s, %s, %s)
    """, (client_id, valor_pagamento, data_pagamento))

# Confirmar alterações
conn.commit()
