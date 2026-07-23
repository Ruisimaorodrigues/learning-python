import pandas as pd

dados = {
    "produto": ["A", "B", "C"],
    "vendas": [120, 180, 150],
}

df = pd.DataFrame(dados)

print(df)
print(f"Total: {df['vendas'].sum()}")