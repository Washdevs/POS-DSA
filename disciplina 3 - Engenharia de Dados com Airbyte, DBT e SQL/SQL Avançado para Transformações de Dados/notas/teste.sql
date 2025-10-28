

SELECT 
	nome,
	departamento,
	salario
	,ROW_NUMBER() OVER (PARTITION BY departamento ORDER BY salario DESC) AS rank_salario
FROM EMPREGADOS;	



SELECT
	DATA_VENDA,
	valor,
	sum(valor) OVER (PARTITION BY DATA_VENDA) AS soma_diaria,
	avg(valor) OVER (PARTITION BY DATA_VENDA) AS media_diaria
FROM VENDAS;



SELECT
	data_venda,
	valor,
	lag(valor, 1) OVER (ORDER BY data_venda) AS valor_anterior,
	lead(valor, 1) OVER (ORDER BY data_venda) AS valor_seguinte
FROM vendas;



SELECT 
	nome,
	departamento,
	salario,
	rank() OVER (PARTITION BY departamento ORDER BY salario desc) rank_salario
FROM empregados;



SELECT 
	nome,
	salario,
	ntile(4) OVER (ORDER BY salario DESC) AS quartil
FROM empregados;