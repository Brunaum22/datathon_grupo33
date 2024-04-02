# PAGINA INICIAL
#   INICIALIZAR COM AMBIENTE QUE ESTA NA PASTA env_datathon -> datathon_env\Scripts\activate

#Importação das bibliotecas
import streamlit as st 
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import numpy as np
from utils import  carrega_dados, separa_anos




##----------------------------------------------------------------------------------
# CONFIG DA PAGINA
##----------------------------------------------------------------------------------
st.set_page_config(
  page_title="KPIs da PM",
  page_icon=":bar_chart:",
  layout='wide'
)

st.title("Acompanhe abaixo alguns dos principais indicadores da PM! :chart_with_upwards_trend:")
st.write('''
#### Veja aqui: 
- Principais KPI's
- Indicadores que compõe o INDE
- Monte sua correlação e regressão entre os indicadores
- Informação por Fase
- Informação por Pedra

Obs.: Métricas em comparação ao ano anterior
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


#-------------
# FILTRO DE ANO LETIVO
#-------------
ano_escolhido = st.sidebar.selectbox("Escolha o ano que deseja ver", options=anos)

ano_anterior = ano_escolhido - 1
valida_ano_anterior = lambda ano_anterior: ano_escolhido if ano_anterior not in anos else ano_anterior 
ano_anterior = valida_ano_anterior(ano_anterior)


# Filtrando df pelo ano que foi selecionados
df_ano_escolhido = separa_anos(df, ano_escolhido)

# Df do ano anterior
df_ano_anterior_escolhido = separa_anos(df, ano_anterior)


#-------------
# Filtro de fases
#-------------
fases = df_ano_escolhido["FASE"].unique()
fases.sort()

fases_escolhidas = st.sidebar.multiselect("Selecione as fases que deseja ver: ", options=fases, default=fases )
df_ano_escolhido = df_ano_escolhido.query(f"FASE in {fases_escolhidas}")

#-------------
# Filtro de Pedras
#-------------
pedras = df_ano_escolhido["PEDRA"].unique()
pedras.sort()
pedras_escolhidas = st.sidebar.multiselect("Selecione as pedras que deseja ver: ", options=pedras,default=pedras)
df_ano_escolhido = df_ano_escolhido.query(f"PEDRA in {pedras_escolhidas}")

#-------------
# Filtro INDE
#-------------
inde = df_ano_escolhido["INDE"].unique()
inde_max = df_ano_escolhido["INDE"].max()
inde_min = df_ano_escolhido["INDE"].min()

inde_select = st.sidebar.slider("Selecione o range de INDE que deseja filtrar: ", 0.0, 10.0,(inde_min, inde_max))
min_inde = inde_select[0]
max_inde = inde_select[1]
df_ano_escolhido = df_ano_escolhido.query(f"INDE >= {min_inde} and INDE <= {max_inde}")




##----------------------------------------------------------------------------------
# KPI MACROS
# Mostrando a partir do que foi selecionado de ano
##----------------------------------------------------------------------------------
st.write(''' 
         # 
         ## KPI's principais
''')

col1, col2, col3 = st.columns(3)

# Quantidade de alunos
qtd_alunos = df_ano_escolhido["NOME"].nunique()
qtd_alunos_ano_anterior = df_ano_anterior_escolhido["NOME"].nunique()
diff_alunos = round((qtd_alunos - qtd_alunos_ano_anterior) / qtd_alunos_ano_anterior , 4)
diff_alunos = "{:.2%}".format(diff_alunos)

col1.metric("Quantidade alunos matriculados no ano", qtd_alunos, diff_alunos)

# Média de INDE
media_inde = round(df_ano_escolhido["INDE"].mean(), 3)
media_inde_anterior = round(df_ano_anterior_escolhido["INDE"].mean(), 3)
diff_inde = round((media_inde - media_inde_anterior) / media_inde_anterior, 4)
diff_inde = "{:.2%}".format(diff_inde)

col2.metric("Média do INDE dos alunos", media_inde, diff_inde)


# PONTO DE VIRADA, % alunos q atingiram ponto de virada
ponto_virada_alunos = df_ano_escolhido[df_ano_escolhido["PONTO_VIRADA"] == 'Sim']["NOME"].nunique()
porc_ponto_virada = round(ponto_virada_alunos / qtd_alunos, 4)
porc_ponto_virada_format = "{:.2%}".format(porc_ponto_virada)

ponto_virada_anterior = df_ano_anterior_escolhido[df_ano_anterior_escolhido["PONTO_VIRADA"] == 'Sim']["NOME"].nunique()
porc_pv_anterior = round(ponto_virada_anterior / qtd_alunos_ano_anterior, 4)
diff_pv = porc_ponto_virada - porc_pv_anterior
diff_pv = "{:.2%}".format(diff_pv)

col3.metric("**% alunos que atingiram ponto virada**",porc_ponto_virada_format, diff_pv)


st.divider()


##----------------------------------------------------------------------------------
# KPI MACROS
#   Média dos indicadores
##----------------------------------------------------------------------------------
st.write(''' 
         ## Indicadores que compõe o INDE
''')

st.write(''' 
         # 
         #### Indicadores acadêmicos
''')
col1, col2, col3 = st.columns(3)

ian = round(df_ano_escolhido["IAN"].mean(),2)
ian_anterior = round(df_ano_anterior_escolhido["IAN"].mean(),2)
diff_ian = round((ian/ian_anterior) - 1, 4) 
diff_ian = "{:.2%}".format(diff_ian)

ida = round(df_ano_escolhido['IDA'].mean(),2)
ida_anterior = round(df_ano_anterior_escolhido["IDA"].mean(),2)
diff_ida = round((ida/ida_anterior) - 1, 4) 
diff_ida = "{:.2%}".format(diff_ida)

ieg = round(df_ano_escolhido["IEG"].mean(),2)
ieg_anterior = round(df_ano_anterior_escolhido["IEG"].mean(),2)
diff_ieg = round((ieg/ieg_anterior) - 1, 4) 
diff_ieg = "{:.2%}".format(diff_ieg)


col1.metric("Média de IAN dos alunos", ian, diff_ian)
col2.metric("Média de IDA dos alunos", ida, diff_ida)
col3.metric("Média de IEG dos alunos", ieg, diff_ieg)


#-------------
# KPI PSCICOSOCCIAL
#-------------
st.write(''' 
         # 
         #### Indicadores psicossocial
''')
col1, col2 = st.columns(2)

iaa = round(df_ano_escolhido["IAA"].mean(),2)
iaa_anterior = round(df_ano_anterior_escolhido["IAA"].mean(),2)
diff_iaa = round((iaa/iaa_anterior) - 1, 4) 
diff_iaa = "{:.2%}".format(diff_iaa)

ips = round(df_ano_escolhido['IPS'].mean(),2)
ips_anterior = round(df_ano_anterior_escolhido["IPS"].mean(),2)
diff_ips = round((ips/ips_anterior) - 1, 4) 
diff_ips = "{:.2%}".format(diff_ips)

col1.metric("Média de IAA dos alunos", iaa, diff_iaa)
col2.metric("Média de IPS dos alunos", ips, diff_ips)


#-------------
# KPI Psicopegagócico
#-------------
st.write(''' 
         # 
         #### Indicadores psicopedagógico
''')
col1, col2 = st.columns(2)

ipp = round(df_ano_escolhido["IPP"].mean(),2)
ipp_anterior = round(df_ano_anterior_escolhido["IPP"].mean(),2)
diff_ipp = round((ipp/ipp_anterior) - 1, 4) 
diff_ipp = "{:.2%}".format(diff_ipp)

ipv = round(df_ano_escolhido['IPV'].mean(),2)
ipv_anterior = round(df_ano_anterior_escolhido["IPV"].mean(),2)
diff_ipv = round((ipv/ipv_anterior) - 1, 4) 
diff_ipv = "{:.2%}".format(diff_ipv)

col1.metric("Média de IPP dos alunos", ipp, diff_ipp)
col2.metric("Média de IPV dos alunos", ipv, diff_ipv)



##----------------------------------------------------------------------------------
# CORRELAÇÃO ENTRE INDICADORES
##----------------------------------------------------------------------------------
st.write(''' 
         # 
         ## Entenda a relação entre os indicadores com a regressão abaixo
''')
plt.figure(figsize=(20,8))

# Pegando as métricas para correlação
opcoes_eixos = ['INDE','IAN', 'IDA', 'IEG', 'IAA', 'IPS', 'IPP', 'IPV']

col1, col2 = st.columns(2)
eixo_y = col1.selectbox("Selecione qual indicador você ver a correlação (eixo y)", options=opcoes_eixos)
eixo_x = col2.selectbox("Selecione o indicador que você quer correlacionar (eixo x)", options=opcoes_eixos)


x = df_ano_escolhido[f"{eixo_x}"]
y = df_ano_escolhido[f"{eixo_y}"]

# Calc linha de regressao e coef de determinacao
coef = np.polyfit(x, y, 1)
poly1d_fn = np.poly1d(coef)
r_squared = np.corrcoef(x, y)[0, 1] ** 2
 
df_plot = pd.DataFrame({f"{eixo_x}": x, f"{eixo_y}": y})
fig = px.scatter(df_plot, x=f"{eixo_x}", y=f"{eixo_y}", title=f'Gráfico de regressão entre {eixo_x} com {eixo_y} (R² = {r_squared:.2f})')

# Adicionando a linha de regressão
fig.add_scatter(x=df_plot[f"{eixo_x}"], y=poly1d_fn(df_plot[f"{eixo_x}"]), mode='lines', name='Linha de Regressão', line=dict(color='red'))

# Exibindo o gráfico
st.plotly_chart(fig)


st.divider()


##----------------------------------------------------------------------------------
# FASES
##----------------------------------------------------------------------------------
st.write(''' 
         ## Métricas e informações por Fase
         #
''')

map_fases = {0.0:"Alpha", 1.0:"Fase 1", 2.0:"Fase 2", 3.0:"Fase 3", 4.0:"Fase 4", 5.0:"Fase 5", 6.0:"Fase 6", 7.0:"Fase 7", 8.0:"Fase 8"}

##-----------------
# Quantidade de aluno por fase
##-----------------
st.write(''' 
         #### Quantidade de alunos e a média do INDE por fase
''')
fase_aluno = df_ano_escolhido.query("PEDRA != '#NULO!' ").groupby(by="FASE")["NOME"].count()
fase_aluno = pd.DataFrame(fase_aluno)
fase_aluno.reset_index(inplace=True)

fase_aluno["FASE"] = fase_aluno["FASE"].map(map_fases)

fig2 = px.bar(fase_aluno, y="NOME", x="FASE", text="NOME",title="Quantidade de aluno por fase")
st.plotly_chart(fig2)


##-----------------
# Média de INDE por fase
##-----------------
fase_inde = df_ano_escolhido.query("PEDRA != '#NULO!' ").groupby(by="FASE")["INDE"].mean()
fase_inde = pd.DataFrame(fase_inde)
fase_inde['INDE'] = round(fase_inde["INDE"], 3)
fase_inde.reset_index(inplace=True)
fase_inde["FASE"] = fase_inde["FASE"].map(map_fases)
fase_inde.sort_values(by="FASE", inplace=True, ascending=False)

fig3 = px.bar(fase_inde, y="FASE", x="INDE", text="INDE",title="Média do INDE por fase", orientation='h')
st.plotly_chart(fig3)


##-----------------
# Indicadores por fase
##-----------------
st.write(''' 
        ##
        #### Indicadores Acadêmicos por Fase
''')

df_grouped = df_ano_escolhido.groupby("FASE")[["IAN", "IDA", "IEG"]].mean().reset_index().sort_values(by="FASE",ascending=False)
df_grouped["FASE"] = df_grouped["FASE"].map(map_fases)


fig4, axs = plt.subplots(1,3, figsize=(10,3))
axs[0].barh(df_grouped["FASE"], df_grouped["IAN"], color='red', label="IAN")
axs[0].set_title('IAN')
for i, v in enumerate(round(df_grouped["IAN"], 1)):
    axs[0].text(v, i, str(v), ha='right', va='center')
axs[0].set_ylabel('FASES')

axs[1].barh(df_grouped["FASE"], df_grouped["IDA"], color='blue', label="IDA")
axs[1].set_title('IDA')
for i, v in enumerate(round(df_grouped["IDA"], 1)):
    axs[1].text(v, i, str(v), ha='right', va='center')
axs[1].set_yticklabels([])

axs[2].barh(df_grouped["FASE"], df_grouped["IEG"], color='green', label="IEG")
axs[2].set_title('IEG')
for i, v in enumerate(round(df_grouped["IEG"], 1)):
    axs[2].text(v, i, str(v), ha='right', va='center')
axs[2].set_yticklabels([])

st.pyplot(fig4)


st.write(''' 
         ## 
         #### Indicadores Psicossocial por Fase
''')

df_grouped = df_ano_escolhido.groupby("FASE")[["IAA", "IPS"]].mean().reset_index().sort_values(by="FASE",ascending=False)
df_grouped["FASE"] = df_grouped["FASE"].map(map_fases)

fig5, axs = plt.subplots(1,2, figsize=(10,3))
axs[0].barh(df_grouped["FASE"], df_grouped["IAA"], color='magenta', label="IAA")
axs[0].set_title('IAA')
for i, v in enumerate(round(df_grouped["IAA"], 1)):
    axs[0].text(v, i, str(v), ha='right', va='center')
axs[0].set_ylabel('FASES')

axs[1].barh(df_grouped["FASE"], df_grouped["IPS"], color='brown', label="IPS")
axs[1].set_title('IPS')
for i, v in enumerate(round(df_grouped["IPS"], 1)):
    axs[1].text(v, i, str(v), ha='right', va='center',color="white")
axs[1].set_yticklabels([])

st.pyplot(fig5)


st.write(''' 
         ## 
         #### Indicadores Psicopegagógicos por Fase
''')

df_grouped = df_ano_escolhido.groupby("FASE")[["IPP", "IPV"]].mean().reset_index().sort_values(by="FASE",ascending=False)
df_grouped["FASE"] = df_grouped["FASE"].map(map_fases)

fig5, axs = plt.subplots(1,2, figsize=(10,3))
axs[0].barh(df_grouped["FASE"], df_grouped["IPP"], color='purple', label="IPP")
axs[0].set_title('IPP')
for i, v in enumerate(round(df_grouped["IPP"], 1)):
    axs[0].text(v, i, str(v), ha='right', va='center',color="white")
axs[0].set_ylabel('FASES')

axs[1].barh(df_grouped["FASE"], df_grouped["IPV"], color='orange', label="IPV")
axs[1].set_title('IPV')
for i, v in enumerate(round(df_grouped["IPV"], 1)):
    axs[1].text(v, i, str(v), ha='right', va='center')
axs[1].set_yticklabels([])

st.pyplot(fig5)

##-----------------
# Quantidade de bolsista por fase
##-----------------

st.write(''' 
         #### Alunos Bolsistas por Fase
''')
if "BOLSISTA" in df_ano_escolhido.columns:

  bolsista_aluno = df_ano_escolhido.query("PEDRA != '#NULO!' ").groupby(by=["FASE","BOLSISTA"])["NOME"].count()
  bolsista_aluno = pd.DataFrame(bolsista_aluno)
  bolsista_aluno.reset_index(inplace=True)
  bolsista_aluno["FASE"] = bolsista_aluno["FASE"].map(map_fases)
  
  # Pivotando para passar valores de linha para coluna
  bolsista_aluno = bolsista_aluno.pivot_table(index="FASE", columns="BOLSISTA", values="NOME", aggfunc='sum', fill_value=0)
  bolsista_aluno.reset_index(inplace=True)
  
  # Criando total e percentual
  bolsista_aluno["total"] = (bolsista_aluno["Sim"] + bolsista_aluno["Não"])
  bolsista_aluno["perc_bolsista"] = round(bolsista_aluno["Sim"] / bolsista_aluno["total"], 4) * 100
  bolsista_aluno.rename(columns={"Sim":"qt_alunos_bolsista", "Não":"qt_alunos_nao_bolsista"}, inplace=True) # Renomeando colunas
  
  # Fazendo plot
  fig, ax1 = plt.subplots(figsize=(6,2.5))
  
  ax1.bar(bolsista_aluno["FASE"], bolsista_aluno["qt_alunos_bolsista"], color="blue", alpha=0.5, width=0.7)
  ax1.set_xlabel("Fase", fontsize=7)
  ax1.set_ylabel("Alunos bolsistas", color='blue', fontsize=7)
  ax1.tick_params('y', colors='blue')
  
  ax2 = ax1.twinx()
  ax2.plot(bolsista_aluno["FASE"], bolsista_aluno["perc_bolsista"], color='red')
  ax2.set_xlabel("Fase", fontsize=7)
  ax2.set_ylabel("% de alunos bolsista", color='red', fontsize=7)
  ax2.tick_params('y', colors='red')
  
  plt.title("Quantidade de alunos bolsista por fase e o %", fontsize=10)
  
  st.pyplot(fig)

else:
  st.markdown('#### <span style="color:red"> Não há informação de bolsista nesse ano</span>', unsafe_allow_html=True)

st.divider()



##----------------------------------------------------------------------------------
# PEDRAS
##----------------------------------------------------------------------------------
st.write(''' 
         ## Métricas e informações por Pedra
         #
''')


##-----------------
# Quantidade de aluno por PEDRA
##-----------------
st.write(''' 
         #### Quantidade de alunos e a média do INDE por PEDRA
''')
PEDRA_aluno = df_ano_escolhido.query("PEDRA != '#NULO!' ").groupby(by="PEDRA")["NOME"].count()
PEDRA_aluno = pd.DataFrame(PEDRA_aluno)
PEDRA_aluno.reset_index(inplace=True)

fig2 = px.bar(PEDRA_aluno, y="NOME", x="PEDRA", text="NOME",title="Quantidade de aluno por PEDRA")
st.plotly_chart(fig2)


##-----------------
# Média de INDE por PEDRA
##-----------------
PEDRA_inde = df_ano_escolhido.query("PEDRA != '#NULO!' ").groupby(by="PEDRA")["INDE"].mean()
PEDRA_inde = pd.DataFrame(PEDRA_inde)
PEDRA_inde['INDE'] = round(PEDRA_inde["INDE"], 3)
PEDRA_inde.reset_index(inplace=True)
PEDRA_inde.sort_values(by="PEDRA", inplace=True, ascending=False)

fig3 = px.bar(PEDRA_inde, y="PEDRA", x="INDE", text="INDE",title="Média do INDE por PEDRA", orientation='h')
st.plotly_chart(fig3)



##-----------------
# Indicadores por fase
##-----------------
st.write(''' 
        ##
        #### Indicadores Acadêmicos por PEDRA
''')
df_grouped = df_ano_escolhido.groupby("PEDRA")[["IAN", "IDA", "IEG"]].mean().reset_index().sort_values(by="PEDRA",ascending=False)


fig4, axs = plt.subplots(1,3, figsize=(10,3))
axs[0].barh(df_grouped["PEDRA"], df_grouped["IAN"], color='red', label="IAN")
axs[0].set_title('IAN')
for i, v in enumerate(round(df_grouped["IAN"], 1)):
    axs[0].text(v, i, str(v), ha='right', va='center')
axs[0].set_ylabel('PEDRAS')

axs[1].barh(df_grouped["PEDRA"], df_grouped["IDA"], color='blue', label="IDA")
axs[1].set_title('IDA')
for i, v in enumerate(round(df_grouped["IDA"], 1)):
    axs[1].text(v, i, str(v), ha='right', va='center')
axs[1].set_yticklabels([])

axs[2].barh(df_grouped["PEDRA"], df_grouped["IEG"], color='green', label="IEG")
axs[2].set_title('IEG')
for i, v in enumerate(round(df_grouped["IEG"], 1)):
    axs[2].text(v, i, str(v), ha='right', va='center')
axs[2].set_yticklabels([])

st.pyplot(fig4)


st.write(''' 
         ## 
         #### Indicadores Psicossocial por PEDRA
''')

df_grouped = df_ano_escolhido.groupby("PEDRA")[["IAA", "IPS"]].mean().reset_index().sort_values(by="PEDRA",ascending=False)

fig5, axs = plt.subplots(1,2, figsize=(10,3))
axs[0].barh(df_grouped["PEDRA"], df_grouped["IAA"], color='magenta', label="IAA")
axs[0].set_title('IAA')
for i, v in enumerate(round(df_grouped["IAA"], 1)):
    axs[0].text(v, i, str(v), ha='right', va='center')
axs[0].set_ylabel('PEDRAS')

axs[1].barh(df_grouped["PEDRA"], df_grouped["IPS"], color='brown', label="IPS")
axs[1].set_title('IPS')
for i, v in enumerate(round(df_grouped["IPS"], 1)):
    axs[1].text(v, i, str(v), ha='right', va='center',color="white")
axs[1].set_yticklabels([])

st.pyplot(fig5)


st.write(''' 
         ## 
         #### Indicadores Psicopegagógicos por PEDRA
''')

df_grouped = df_ano_escolhido.groupby("PEDRA")[["IPP", "IPV"]].mean().reset_index().sort_values(by="PEDRA",ascending=False)

fig5, axs = plt.subplots(1,2, figsize=(10,3))
axs[0].barh(df_grouped["PEDRA"], df_grouped["IPP"], color='purple', label="IPP")
axs[0].set_title('IPP')
for i, v in enumerate(round(df_grouped["IPP"], 1)):
    axs[0].text(v, i, str(v), ha='right', va='center',color="white")
axs[0].set_ylabel('PEDRAS')

axs[1].barh(df_grouped["PEDRA"], df_grouped["IPV"], color='orange', label="IPV")
axs[1].set_title('IPV')
for i, v in enumerate(round(df_grouped["IPV"], 1)):
    axs[1].text(v, i, str(v), ha='right', va='center')
axs[1].set_yticklabels([])

st.pyplot(fig5)

##-----------------
# Quantidade de bolsista por PEDRA
##-----------------

st.write(''' 
         #### Alunos Bolsistas por PEDRA
''')
if "BOLSISTA" in df_ano_escolhido.columns:

  bolsista_aluno = df_ano_escolhido.query("PEDRA != '#NULO!' ").groupby(by=["PEDRA","BOLSISTA"])["NOME"].count()
  bolsista_aluno = pd.DataFrame(bolsista_aluno)
  bolsista_aluno.reset_index(inplace=True)

  
  # Pivotando para passar valores de linha para coluna
  bolsista_aluno = bolsista_aluno.pivot_table(index="PEDRA", columns="BOLSISTA", values="NOME", aggfunc='sum', fill_value=0)
  bolsista_aluno.reset_index(inplace=True)
  
  # Criando total e percentual
  bolsista_aluno["total"] = (bolsista_aluno["Sim"] + bolsista_aluno["Não"])
  bolsista_aluno["perc_bolsista"] = round(bolsista_aluno["Sim"] / bolsista_aluno["total"], 4) * 100
  bolsista_aluno.rename(columns={"Sim":"qt_alunos_bolsista", "Não":"qt_alunos_nao_bolsista"}, inplace=True) # Renomeando colunas
  
  # Fazendo plot
  fig, ax1 = plt.subplots(figsize=(6,2.5))
  
  ax1.bar(bolsista_aluno["PEDRA"], bolsista_aluno["qt_alunos_bolsista"], color="blue", alpha=0.5, width=0.7)
  ax1.set_xlabel("PEDRA", fontsize=7)
  ax1.set_ylabel("Alunos bolsistas", color='blue', fontsize=7)
  ax1.tick_params('y', colors='blue')
  
  ax2 = ax1.twinx()
  ax2.plot(bolsista_aluno["PEDRA"], bolsista_aluno["perc_bolsista"], color='red')
  ax2.set_xlabel("PEDRA", fontsize=7)
  ax2.set_ylabel("% de alunos bolsista", color='red', fontsize=7)
  ax2.tick_params('y', colors='red')
  
  plt.title("Quantidade de alunos bolsista por PEDRA e o %", fontsize=10)
  
  st.pyplot(fig)

else:
  st.markdown('#### <span style="color:red"> Não há informação de bolsista nesse ano</span>', unsafe_allow_html=True)

st.divider()