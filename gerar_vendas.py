"""Gera um vendas.csv de exemplo (use apenas se não tiver o seu próprio)."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
catalogo = {
    "Notebook": ("Eletrônicos", 3500), "Smartphone": ("Eletrônicos", 2200),
    "Fone Bluetooth": ("Eletrônicos", 250), "Smart TV": ("Eletrônicos", 2800),
    "Mouse": ("Periféricos", 80), "Teclado Mecânico": ("Periféricos", 320),
    "Monitor": ("Periféricos", 900), "Webcam": ("Periféricos", 180),
    "Cadeira Gamer": ("Móveis", 1200), "Mesa Escritório": ("Móveis", 750),
    "HD Externo": ("Armazenamento", 420), "Pen Drive": ("Armazenamento", 45),
}
regioes = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]
n = 500
produtos = rng.choice(list(catalogo), n)
df = pd.DataFrame({
    "produto": produtos,
    "categoria": [catalogo[p][0] for p in produtos],
    "quantidade": rng.integers(1, 11, n),
    "preco_unitario": [round(catalogo[p][1] * rng.uniform(0.9, 1.1), 2) for p in produtos],
    "regiao": rng.choice(regioes, n, p=[.08, .17, .10, .40, .25]),
    "data_venda": pd.to_datetime("2025-01-01") + pd.to_timedelta(rng.integers(0, 365, n), unit="D"),
})
df.sort_values("data_venda").to_csv("vendas.csv", index=False)
print("vendas.csv gerado com", n, "linhas")
