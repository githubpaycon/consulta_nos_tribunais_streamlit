string = 'Processo: AIRR - 488-59.2016.5.11.0002'

lista = ['Processo: AIRR - 488-59.2016.5.11.0002', 'Número no TRT de Origem: AIRR-488/2016-0002-11.', 'Órgão Judicante: 6ª Turma', 'Relator: Ministro Augusto César Leite de Carvalho', 'Agravante(s) e Agravado (s):', 'Advogado:', 'Agravante(s) e Agravado (s):', 'Advogado:', 'Advogada:']


# esta listcomprehesino pega os textos até o 2 pontos (:)
lista_colunas = [coluna.split(':')[0] for coluna in lista]

cont = 1
colunas_com_ids = []

for coluna in lista_colunas:
    colunas_com_ids.append(f'{coluna} col{cont}')
    cont += 1

# for coluna in lista:
#     lista_colunas.append(coluna.split(':')[0])
    
print(lista_colunas)
print(colunas_com_ids)