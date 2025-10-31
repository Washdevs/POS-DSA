import csv
import psycopg2
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms.ollama import Ollama

from langchain_ollama import OllamaLLM
llm = OllamaLLM(model="llama3")

output_parser = StrOutputParser()

def dsa_gera_insights():
    conn = psycopg2.connect(
        dbname="dsadb",
        user="dsa",
        password="dsa1010",
        host="localhost",
        port="5959"
    )
    cursor = conn.cursor()

    query = """
    select
        c.id_cliente,
        c.nome,
        count(ped.id_pedido) as total_pedidos,
        avg(ped.quantidade) as media_qtd,
        sum(pr.preco * ped.quantidade) as total_gasto,
        max(ped.data_pedido) as ultima_compra,
        extract(day from now() - max(ped.data_pedido)) as dias_desde_ultima,
        case when extract(day from now() - max(ped.data_pedido)) < 30 then 1 else 0 end as comprou_ultimo_mes
    from dist.clientes c
    join dist.pedidos ped on ped.id_cliente = c.id_cliente
    join dist.produtos pr on pr.id_produto = ped.id_produto
    group by c.id_cliente, c.nome;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    clientes_txt = ""
    for row in rows:
        (
            id_cliente,
            nome,
            total_pedidos,
            media_qtd,
            total_gasto,
            ultima_compra,
            dias_desde_ultima,
            comprou_ultimo_mes
        ) = row
        clientes_txt += (
            f"- Cliente {nome}: {total_pedidos} pedidos, gasto R${total_gasto:.2f}, "
            f"média {media_qtd:.1f} itens, última compra há {int(dias_desde_ultima)} dias.\n"
        )

    prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Você é um analista de dados que deve responder de forma objetiva, direta e em formato executivo. "
     "Não explique o modelo matemático nem o método. "
     "Use apenas as informações fornecidas e gere uma conclusão preditiva clara, em uma linha por cliente. "
     "Formato de saída obrigatório: "
     "'Cliente <nome> provavelmente comprará novamente em <n> dias com probabilidade de <p>%.' "
     "Se possível, estime também a quantidade provável de pedidos."
     "Proíba qualquer saída que contenha código Python, fórmulas, ou termos técnicos (como regressão, beta, logit, coeficiente)." 
    "Se o modelo tentar explicar, ignore a explicação e responda apenas com o resultado preditivo final."),
    ("user", "Dados dos clientes:\n{clientes}")
    ])
    chain = prompt | llm | output_parser

    response = chain.invoke({'clientes': clientes_txt})

    with open('lab5-insights_teste.csv', 'w', newline='', encoding='utf-8') as f:
        csv.writer(f).writerows([["Insight"], [response]])

    return response

if __name__ == "__main__":
    print("Gerando insights probabilísticos...")
    resultado = dsa_gera_insights()
print(resultado.encode('utf-8', errors='ignore').decode('utf-8'))