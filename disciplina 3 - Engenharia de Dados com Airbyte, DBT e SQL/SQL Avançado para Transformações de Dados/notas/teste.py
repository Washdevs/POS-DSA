import pandas as pd

# Similar ao JOIN do SQL pode especificar colunas chave pra combinar os DataFrames
df1.merge(df2, on='key_column')  

# merge com diferentes chaves em cada dataframe: util quando os nomes das colunas chave são diferentes
df1.merge(df2, left_on='df1_key', right_on='df2_key')

# outer, inner, left, right merges: pandas permite especificar o tipo de merge similar aos joins do SQL
df1.merge(df2, on='key_column', how='outer') # Ou 'inner', left, 'right'