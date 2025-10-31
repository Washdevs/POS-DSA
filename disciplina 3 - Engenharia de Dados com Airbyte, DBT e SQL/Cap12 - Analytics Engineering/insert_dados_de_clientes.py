import psycopg2, random, datetime

conn = psycopg2.connect(dbname="dsadb", user="dsa", password="dsa1010", host="localhost", port="5959")
cur = conn.cursor()

# Clientes
for i in range(1, 21):
    cur.execute("""
        insert into dist.clientes (nome, cidade, canal, data_cadastro, faixa_renda)
        values (%s, %s, %s, %s, %s)
    """, (
        f"Cliente_{i}",
        random.choice(['São Paulo','Curitiba','Recife','Fortaleza']),
        random.choice(['Varejo','Hospital','Farmácia']),
        datetime.date(2022, random.randint(1,12), random.randint(1,28)),
        random.choice(['Baixa','Média','Alta'])
    ))

# Produtos
for i in range(1, 16):
    cur.execute("""
        insert into dist.produtos (nome, categoria, preco, margem)
        values (%s, %s, %s, %s)
    """, (
        f"Produto_{i}",
        random.choice(['Genérico','Marca','OTC']),
        round(random.uniform(10, 150), 2),
        round(random.uniform(5, 25), 2)
    ))

# Pedidos
for _ in range(200):
    cur.execute("""
        insert into dist.pedidos (id_cliente, id_produto, quantidade, data_pedido, canal)
        values (%s, %s, %s, %s, %s)
    """, (
        random.randint(1, 20),
        random.randint(1, 15),
        random.randint(1, 8),
        datetime.date(2023 + random.randint(0,1), random.randint(1,12), random.randint(1,28)),
        random.choice(['Varejo','Hospital','Farmácia'])
    ))

conn.commit()
cur.close()
conn.close()
