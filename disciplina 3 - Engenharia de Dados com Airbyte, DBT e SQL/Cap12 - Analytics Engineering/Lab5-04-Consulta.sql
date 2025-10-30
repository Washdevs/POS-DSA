-- Lab 5 - Analytics Engineering - Python, SQL e LLM Para Extrair Insights em Pipelines de Engenharia de Dados
-- SQL - Consulta para obter o total de compra por cliente

select
	c.nome,
	count(co.id_compra ) as total_compras,
	sum(p.preco) as total_gasto
from
	lab5.clientes c
join 
	lab5.compras co on co.id_cliente = c.id_cliente
join 
	lab5.produtos p on co.id_produto = p.id_produto
group by c.nome;