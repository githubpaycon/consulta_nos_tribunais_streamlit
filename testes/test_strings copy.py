from tkinter.tix import DisplayStyle
import pandas as pd

venda = {
    'Produtos': ['biblia', 'Agua', 'Monitor'],
    'precos': [0, 1.50, 325],
    'qtd': [1, 1, 1]
}

vendas_df = pd.DataFrame(venda)