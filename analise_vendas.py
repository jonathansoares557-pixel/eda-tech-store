# %% [markdown]
# # EDA Tech Store — Análise de Vendas
# Análise exploratória do arquivo `vendas.csv`.

# %%
import pandas as pd
import matplotlib.pyplot as plt

# %% [markdown]
# ## 1. Carregar os dados

# %%
df = pd.read_csv("vendas.csv", encoding="utf-8")
# o arquivo pode trazer a coluna de data como "data"
df = df.rename(columns={"data": "data_venda"})
df["data_venda"] = pd.to_datetime(df["data_venda"])
df["receita"] = df["quantidade"] * df["preco_unitario"]

# %% [markdown]
# ## 2. Informações básicas

# %%
print("Primeiras 5 linhas:")
print(df.head().to_string(index=False))

print(f"\nTotal de registros: {len(df)}")
print(f"Receita total: R$ {df['receita'].sum():,.2f}")

# %% [markdown]
# ## 3. Consultas específicas

# %%
# Vendas da categoria "Eletrônicos"
eletronicos = df[df["categoria"] == "Eletrônicos"]
print(f"Vendas de Eletrônicos: {len(eletronicos)} registros")
print(eletronicos.head(10).to_string(index=False))

# %%
# Produto mais vendido (em quantidade)
por_produto = df.groupby("produto")["quantidade"].sum().sort_values(ascending=False)
print(f"Produto mais vendido: {por_produto.idxmax()} ({por_produto.max()} unidades)")

# %%
# Região com maior valor de compras
por_regiao = df.groupby("regiao")["receita"].sum().sort_values(ascending=False)
print(f"Região com maior valor de compras: {por_regiao.idxmax()} (R$ {por_regiao.max():,.2f})")

# %% [markdown]
# ## 4. Visualizações (desafio extra)

# %%
receita_cat = df.groupby("categoria")["receita"].sum().sort_values(ascending=False)
ax = receita_cat.plot(kind="bar", color="#4C78A8", figsize=(8, 5))
ax.set_title("Receita por categoria")
ax.set_xlabel("")
ax.set_ylabel("Receita (R$)")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("receita_por_categoria.png", dpi=150)
plt.show()

# %%
mensal = df.groupby(df["data_venda"].dt.to_period("M"))["receita"].sum()
mensal.index = mensal.index.to_timestamp()
ax = mensal.plot(kind="line", marker="o", color="#F58518", figsize=(9, 5))
ax.set_title("Evolução das vendas por mês")
ax.set_xlabel("Mês")
ax.set_ylabel("Receita (R$)")
ax.grid(alpha=.3)
plt.tight_layout()
plt.savefig("vendas_por_mes.png", dpi=150)
plt.show()

# %% [markdown]
# ## 5. Tabela dinâmica e relatório Excel (extras)

# %%
pivot = pd.pivot_table(df, values="receita", index="regiao", columns="categoria",
                       aggfunc="sum", fill_value=0, margins=True, margins_name="Total")
print(pivot.round(2).to_string())

with pd.ExcelWriter("relatorio_vendas.xlsx") as xw:
    resumo = pd.DataFrame({
        "Métrica": ["Total de registros", "Receita total (R$)", "Produto mais vendido",
                    "Região com maior valor"],
        "Valor": [len(df), round(df["receita"].sum(), 2), por_produto.idxmax(), por_regiao.idxmax()],
    })
    resumo.to_excel(xw, sheet_name="Resumo", index=False)
    receita_cat.rename("receita").to_frame().to_excel(xw, sheet_name="Receita por categoria")
    mensal.rename("receita").to_frame().to_excel(xw, sheet_name="Receita mensal")
    pivot.to_excel(xw, sheet_name="Região x Categoria")
    for ws in xw.book.worksheets:
        for col in ws.columns:
            ws.column_dimensions[col[0].column_letter].width = max(len(str(c.value or "")) for c in col) + 3
print("\nRelatório salvo em relatorio_vendas.xlsx")
