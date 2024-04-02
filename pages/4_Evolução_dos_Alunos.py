#Importação das bibliotecas
import streamlit as st 
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import numpy as np
from utils import  carrega_dados, separa_anos, aluno_fase_pedra_inde, map_campos, cria_flags


##----------------------------------------------------------------------------------
# CONFIG DA PAGINA
##----------------------------------------------------------------------------------
st.set_page_config(
  page_title="Alunos",
  page_icon=":female-student:",
  layout='wide'
)

st.title("Acompanhe individualmente a performance dos alunos, veja a evolução deles(as) no decorrer do tempo!")
st.write('''
#### Veja aqui: 
- Evolução de classificação de pedra em cada ano
- Performance indivídual de cada aluno

''')



##----------------------------------------------------------------------------------
# CARREGAR DADOS E FILTROS
##----------------------------------------------------------------------------------
# Carregar dados
df = carrega_dados()

# Quantidade de anos no df
anos = []
for coluna in df.columns:
    if coluna.startswith("PEDRA_"):
        ano = coluna.split("_")[1]  # Extrair o ano da coluna
        anos.append(int(ano))
    anos.sort(reverse=True)

col_filter1,col_filter2 = st.columns(2)

#-------------
# FILTRO DE ANOS
#-------------
# PEGANDO OS ANOS QUE TEM NO DF
anos_pm = df["ANO_INGRESSO_2022"].fillna(0).astype(int).unique()
anos_pm.sort()
ano_inicio_pm = st.sidebar.multiselect("Escolha o ano de inicio", options=anos_pm, default=anos_pm)

# DF FILTRADO
df["ANO_INGRESSO_2022"] = df["ANO_INGRESSO_2022"].fillna(0).astype(int)
df_aluno = df.query(f'ANO_INGRESSO_2022 in {ano_inicio_pm}')
df_aluno = df_aluno[["NOME", "ANO_INGRESSO_2022"]]



##----------------------------------------------------------------------------------
# DF APENAS CAMPOS DESEJADOS E FILTROS+FLAGS
##----------------------------------------------------------------------------------
df_filtro_full = aluno_fase_pedra_inde(df)
df_filtro_full = pd.merge(df_filtro_full, df_aluno, on="NOME", how='inner')

# Renomeando campos, mepeando valores
df_filtro_full = map_campos(df_filtro_full, "PEDRA")


df_filtro_full["INDE_2020"] = round(df_filtro_full["INDE_2020"],3)
df_filtro_full["INDE_2021"] = round(df_filtro_full["INDE_2021"],3)
df_filtro_full["INDE_2022"] = round(df_filtro_full["INDE_2022"],3)   


#-------------
# FLAG E FILTRO VETERANO
#-------------
df_filtro_full['flag_veterano_apenas'] = df_filtro_full.apply(lambda row: cria_flags(row, 'veterano'), axis=1)
flag_pm_veterano = df_filtro_full['flag_veterano_apenas'].fillna(0).astype(int).unique()
flg_veterano = st.sidebar.multiselect("Escolha 1 se você quer apenas alunos com dados nos últimos 3 anos (1 como padrão para melhor visualização)", options=flag_pm_veterano, default=1)
df_filtro_full = df_filtro_full.query(f'flag_veterano_apenas == {flg_veterano}')


#-------------
# FLAG MUDOU PEDRA
#-------------
df_filtro_full['flag_mudou_pedra_21'] = df_filtro_full.apply(lambda row: cria_flags(row, 'evolucao_pedra_20_21'), axis=1)
df_filtro_full['flag_mudou_pedra_22'] = df_filtro_full.apply(lambda row: cria_flags(row, 'evolucao_pedra_21_22'), axis=1)
df_filtro_full['flag_mudou_pedra_20_22'] = df_filtro_full.apply(lambda row: cria_flags(row, 'evolucao_pedra_20_22'), axis=1)


#-------------
# FILTRO ALUNO
#-------------
def clear_multi():
    st.session_state.multiselect = []
    return
# st.session_state
#create your button to clear the state of the multiselect
st.sidebar.button("Limpar lista de alunos abaixo", on_click=clear_multi)

qt_alunos = df_filtro_full["NOME"].unique()
alunos = st.sidebar.multiselect("Escolha os alunos que quer acompanhar (visão tabela apenas)", options=qt_alunos, default=qt_alunos,key="multiselect")



##----------------------------------------------------------------------------------
# GRAFICOS
##----------------------------------------------------------------------------------
st.write('''
##
## Comparação "Ano vs Ano" em alteração da classificação em pedras, por fase

- Em qual fase de cada ano temos mais "detratores" e mais "promovidos"
- De 20 para 21 tivemos uma quantidade relevante de alunos que mudaram a classificação para uma melhor (33% subiram de classificação e apenas 15% caiu)
- Já de 21 para 22 foi o contrário (33% caíram de classificação e 15% apenas que subiram). Muito provavelmente por conta da pandemia, sengundo ano nesse "regime" escolar.
- Mas se olharmos, "inicio" vs "fim" da pandemia, temos de forma geral uma melhora. 32% subiram na classificação, 50% permaneceram e 18% cairam (comparando a classificação dos alunos em 2020 vs 2022)

''')

# PREPARANDO DFs
df_filtro_full_dash = map_campos(df_filtro_full, "FASE")

# Mapas
map_evolucao = {0: "Caiu de classificação de Pedra", 1: 'Continuou no mesmo nível', 2: "Subiu claasificação de Pedra"}
colors = {'Caiu de classificação de Pedra': 'red', 'Continuou no mesmo nível': 'blue', "Subiu claasificação de Pedra":"green"}
col1, col2 = st.columns(2)

# DASH - EVOLUÇÃO DE 20 -> 21
df_dash_20_21 = pd.DataFrame(df_filtro_full_dash.query("flag_mudou_pedra_21 in (0,1,2)").groupby(["FASE_2020","flag_mudou_pedra_21"])["NOME"].count())
df_dash_20_21.reset_index(inplace=True)
df_dash_20_21.rename(columns={"":"FASE", "":"Flag_mudo_pedra", "NOME":"qt_alunos"},inplace=True) # renomear colunas
df_dash_20_21["flag_mudou_pedra_21"] = df_dash_20_21["flag_mudou_pedra_21"].map(map_evolucao)

# Plot
fig = px.bar(df_dash_20_21, y="qt_alunos", x="FASE_2020", color="flag_mudou_pedra_21",color_discrete_map=colors, text="qt_alunos", title="Comparação entre 2020 e 2021")
col1.plotly_chart(fig)

# DASH - EVOLUÇÃO DE 20 -> 22
df_dash_20_22 = pd.DataFrame(df_filtro_full_dash.query("flag_mudou_pedra_20_22 in (0,1,2)").groupby(["FASE_2020","flag_mudou_pedra_20_22"])["NOME"].count())
df_dash_20_22.reset_index(inplace=True)
df_dash_20_22.rename(columns={"":"FASE", "":"Flag_mudo_pedra", "NOME":"qt_alunos"},inplace=True) # renomear colunas
df_dash_20_22["flag_mudou_pedra_20_22"] = df_dash_20_22["flag_mudou_pedra_20_22"].map(map_evolucao)

# Plot
fig = px.bar(df_dash_20_22, y="qt_alunos", x="FASE_2020", color="flag_mudou_pedra_20_22",color_discrete_map=colors, text="qt_alunos", title="Comparação entre 2020 e 2022")
col2.plotly_chart(fig)



# DASH - EVOLUÇÃO DE 21 -> 22
df_dash_21_22 = pd.DataFrame(df_filtro_full_dash.query("flag_mudou_pedra_22 in (0,1,2)").groupby(["FASE_2021","flag_mudou_pedra_22"])["NOME"].count())
df_dash_21_22.reset_index(inplace=True)
df_dash_21_22.rename(columns={"":"FASE", "":"Flag_mudo_pedra", "NOME":"qt_alunos"},inplace=True) # renomear colunas
df_dash_21_22["flag_mudou_pedra_22"] = df_dash_21_22["flag_mudou_pedra_22"].map(map_evolucao)

# Plot
fig = px.bar(df_dash_21_22, y="qt_alunos", x="FASE_2021", color="flag_mudou_pedra_22",color_discrete_map=colors, text="qt_alunos", title="Comparação entre 2021 e 2022")
st.plotly_chart(fig)




##----------------------------------------------------------------------------------
# PLOT Tabelas
##----------------------------------------------------------------------------------
df_filtro_full.rename(columns={"ANO_INGRESSO_2022":"ANO_INICIO_PM"}, inplace=True)
st.table(df_filtro_full[['ANO_INICIO_PM', 'NOME', 'FASE_2020', 'FASE_2021', 'FASE_2022', 
                         'PEDRA_2020', 'PEDRA_2021', "PEDRA_2022", 
                         'INDE_2020', 'INDE_2021', 'INDE_2022']])




# df_ano_escolhido = separa_anos(df, 2022)
# df_ano_2021 = separa_anos(df, 2021)
# df_ano_2020 = separa_anos(df, 2020)
# df_ano_escolhido = df_ano_escolhido.query("ANO_INGRESSO <= 2020")

# df_full = pd.merge(df_ano_escolhido, df_ano_2021[["NOME","FASE","INDE","PEDRA","IAA","IEG","IPS","IDA","IPP","IPV","IAN"]], on="NOME", how="inner",suffixes=["_2022","_2021"])
# df_full = pd.merge(df_ano_escolhido, df_ano_2020[["NOME","FASE","INDE","PEDRA","IAA","IEG","IPS","IDA","IPP","IPV","IAN"]], on="NOME", how="inner",suffixes=["_2022","_2020"])


# df_aluno = df[["NOME", 'FASE_TURMA_2020', "FASE_2021", "FASE_2022", "INDE_2020", "INDE_2021", "INDE_2022", "PEDRA_2020", "PEDRA_2021", "PEDRA_2022"]]






#-------------
# Filtro de Pedras
#-------------
# pedras = df_ano_escolhido["PEDRA"].unique()
# pedras.sort()
# pedras_escolhidas = st.sidebar.multiselect("Selecione as pedras que deseja ver: ", options=pedras,default=pedras)
# df_ano_escolhido = df_ano_escolhido.query(f"PEDRA in {pedras_escolhidas}")

# #-------------
# # Filtro INDE
# #-------------
# inde = df_ano_escolhido["INDE"].unique()
# inde_max = df_ano_escolhido["INDE"].max()
# inde_min = df_ano_escolhido["INDE"].min()

# inde_select = st.sidebar.slider("Selecione o range de INDE que deseja filtrar: ", 0.0, 10.0,(inde_min, inde_max))
# min_inde = inde_select[0]
# max_inde = inde_select[1]
# df_ano_escolhido = df_ano_escolhido.query(f"INDE >= {min_inde} and INDE <= {max_inde}")



##----------------------------------------------------------------------------------

##----------------------------------------------------------------------------------



