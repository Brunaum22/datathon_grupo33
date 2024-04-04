# PAGINA INICIAL
#   INICIALIZAR COM AMBIENTE QUE ESTA NA PASTA env_datathon -> datathon_env\Scripts\activate

#Importação das bibliotecas
import streamlit as st 
import pandas as pd
import plotly.express as px
from sklearn import *
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


from utils import *


##----------------------------------------------------------------------------------
# CONFIG DA PAGINA
##----------------------------------------------------------------------------------
st.set_page_config(
  page_title="Classificação Estudantes",
  page_icon=":male-student:",
  layout='wide'
)


st.title("Veja abaixo a classificação dos estudantes :nerd_face:")

st.write(
'''
### O que é KNN? 
- É um algoritmo de aprendizado de máquina usado para classificação e regressão. Esse modelo classifica ou prevê uma nova amostra com base na “proximidade” dela com outras amostras conhecidas no conjunto de dados.

### O que foi considerado para a nossa classificação?
- Indíces que compõe o INDE ("IPV", "IDA", "IPP", "IAN", "IAA", "IPS", "IEG") mais as NOTA_PORT, NOTA_ING, NOTA_MAT
         
''')

##----------------------------------------------------------------------------------
# CARREGAR DADOS E FILTROS
##----------------------------------------------------------------------------------
# Carregar dados
df = carrega_dados()
df_total = trata_base_classif(df, "p")

st.write('''## Por Pedra''')
df_trat_pedra = trata_base_classif(df_total, "p", ['STATUS', 'ANO', 'NOME', 'PEDRA', "IPV", "IDA", "IPP", "NOTA_PORT", "NOTA_ING", "IAN", "NOTA_MAT", "IAA", "IPS", "IEG"])
pedras = trata_base_classif(df_total, "p", ["PEDRA"])
selecao_pedra = st.selectbox("Selecione a pedra que deseja filtrar:", options=pedras["PEDRA"].unique())
df_filtrado = filtra(df_trat_pedra, "pedra", selecao_pedra)
st.dataframe(df_filtrado)

col1, col2 = st.columns(2)
col1.metric("Quantidade de Alunos com Boas Notas:", len(df_filtrado[df_filtrado['STATUS']=="BOM"]))
col2.metric("Quantidade de Alunos com Ponto de Atenção:", len(df_filtrado[df_filtrado['STATUS']=="DESENVOLVER"]))

on_pedra = st.toggle("Deseja acessar o Simulador usando o modelo KNN? ")

if on_pedra:
    st.info('Qual dos indicadores gostaria de aumentar para realizar a simulação?', icon="ℹ️")
    
    valor_IPV = container("IPV")
    valor_IDA = container("IDA")
    valor_IPP = container("IPP")
    valor_NOTA_PORT = container("NOTA_PORT")
    valor_NOTA_ING = container("NOTA_ING")
    valor_NOTA_MAT = container("NOTA_MAT")
    valor_IAN = container("IAN")
    valor_IAA = container("IAA")
    valor_IPS = container("IPS")
    valor_IEG = container("IEG")

    if st.button("Executar a Simulação"):
        if (valor_IPV != 0 or valor_IDA != 0 or valor_IPP != 0 or valor_NOTA_PORT != 0 or valor_NOTA_ING != 0 or valor_NOTA_MAT != 0 or valor_IAN != 0 or valor_IAA != 0 or valor_IPS != 0 or valor_IEG != 0):
          #df_filtrado['novo_IPV'] = ((valor_IPV / 100) * df_filtrado['IPV']) + df_filtrado['IPV']
          novosIndicadoresPercentuais(df_filtrado, "IPV", valor_IPV)
          novosIndicadoresPercentuais(df_filtrado, "IDA", valor_IDA)
          novosIndicadoresPercentuais(df_filtrado, "IPP", valor_IPP)
          novosIndicadoresPercentuais(df_filtrado, "NOTA_PORT", valor_NOTA_PORT)
          novosIndicadoresPercentuais(df_filtrado, "NOTA_ING", valor_NOTA_ING)
          novosIndicadoresPercentuais(df_filtrado, "IAN", valor_IAN)
          novosIndicadoresPercentuais(df_filtrado, "NOTA_MAT", valor_NOTA_MAT)
          novosIndicadoresPercentuais(df_filtrado, "IAA", valor_IAA)
          novosIndicadoresPercentuais(df_filtrado, "IPS", valor_IPS)
          novosIndicadoresPercentuais(df_filtrado, "IEG", valor_IEG)
          
          resultsFinal = modeloKNN(df_filtrado)
          st.dataframe(resultsFinal)
          col1, col2 = st.columns(2)

          qtd_apos_simul_BOM = len(resultsFinal[resultsFinal['novo_STATUS']=="BOM"])
          qtd_apos_simul_DES = len(resultsFinal[resultsFinal['novo_STATUS']=="DESENVOLVER"])

          qtd_ant_simul_BOM = len(df_filtrado[df_filtrado['STATUS']=="BOM"])
          qtd_ant_simul_DES = len(df_filtrado[df_filtrado['STATUS']=="DESENVOLVER"])

          diff_qtd_ant_simul_BOM = round((qtd_apos_simul_BOM - qtd_ant_simul_BOM) / qtd_ant_simul_BOM , 4)
          diff_qtd_ant_simul_BOM = "{:.2%}".format(diff_qtd_ant_simul_BOM)

          diff_qtd_ant_simul_DES = round((qtd_apos_simul_DES - qtd_ant_simul_DES) / qtd_ant_simul_DES , 4)
          diff_qtd_ant_simul_DES = "{:.2%}".format(diff_qtd_ant_simul_DES)


          col1.metric("Quantidade de Alunos com Boas Notas após Simulação:", len(resultsFinal[resultsFinal['novo_STATUS']=="BOM"]), diff_qtd_ant_simul_BOM)
          col2.metric("Quantidade de Alunos com Ponto de Atenção após Simulação::", len(resultsFinal[resultsFinal['novo_STATUS']=="DESENVOLVER"]), diff_qtd_ant_simul_DES)
        else:
           st.error("Necessário alterar algum dos indicadores para realizar a simulação")



st.divider()

# st.write('''## Por Fase''')
# df_trat_fase = trata_base_classif(df_total, "f", ['FASE_NUM', 'FASE_TURMA', 'STATUS', 'ANO', 'NOME', 'PEDRA', "IPV", "IDA", "IPP", "NOTA_PORT", "NOTA_ING", "IAN", "NOTA_MAT", "IAA", "IPS", "IEG"])
# st.dataframe(df_trat_fase)
# fase = trata_base_classif(df_total, "f", ["FASE_NUM"])
# fase = fase.sort_values(by='FASE_NUM')
# selecao_fase = st.selectbox("Selecione a fase que deseja filtrar:", options=fase["FASE_NUM"].unique())
# #df_filtrado = filtra(df_trat_fase, "fase", selecao_fase)
# st.dataframe(df_filtrado)

# col1, col2 = st.columns(2)
# col1.metric("Quantidade de Alunos com Boas Notas:", len(df_filtrado[df_filtrado['STATUS']=="BOM"]))
# col2.metric("Quantidade de Alunos com Ponto de Atenção:", len(df_filtrado[df_filtrado['STATUS']=="DESENVOLVER"]))

# st.divider()

# st.write('''## Por Aluno''')
# df_trat_nome = trata_base_classif(df_total, ['STATUS', 'ANO', 'NOME', 'PEDRA', "IPV", "IDA", "IPP", "NOTA_PORT", "NOTA_ING", "IAN", "NOTA_MAT", "IAA", "IPS", "IEG"])
# nome_digitado = st.text_input("Nome do Aluno: ")
# df_filtrado = filtra(df_trat_nome, "nome", nome_digitado)
# st.dataframe(df_filtrado)


# col1, col2 = st.columns(2)
# col1.metric("Quantidade de Alunos com Boas Notas:", len(df_filtrado[df_filtrado['STATUS']=="BOM"]))
# col2.metric("Quantidade de Alunos com Ponto de Atenção:", len(df_filtrado[df_filtrado['STATUS']=="DESENVOLVER"]))

# on_aluno = st.toggle("Filtar aluno e alterar os indicadores")

# if on_aluno:
#     st.info('Qual dos indicadores gostaria de aumentar ou diminuir para realizar a simulação?', icon="ℹ️")
    
#     valor_IPV = container("IPV")
#     valor_IDA = container("IDA")
#     valor_IPP = container("IPP")
#     valor_NOTA_PORT = container("NOTA_PORT")
#     valor_NOTA_ING = container("NOTA_ING")
#     valor_NOTA_MAT = container("NOTA_MAT")
#     valor_IAN = container("IAN")
#     valor_IAA = container("IAA")
#     valor_IPS = container("IPS")
#     valor_IEG = container("IEG")

#     if st.button("Executar a Simulação"):
#         if (valor_IPV != 0 or valor_IDA != 0 or valor_IPP != 0 or valor_NOTA_PORT != 0 or valor_NOTA_ING != 0 or valor_NOTA_MAT != 0 or valor_IAN != 0 or valor_IAA != 0 or valor_IPS != 0 or valor_IEG != 0):
#           #df_filtrado['novo_IPV'] = ((valor_IPV / 100) * df_filtrado['IPV']) + df_filtrado['IPV']
#           novosIndicadoresPercentuais(df_filtrado, "IPV", valor_IPV)
#           novosIndicadoresPercentuais(df_filtrado, "IDA", valor_IDA)
#           novosIndicadoresPercentuais(df_filtrado, "IPP", valor_IPP)
#           novosIndicadoresPercentuais(df_filtrado, "NOTA_PORT", valor_NOTA_PORT)
#           novosIndicadoresPercentuais(df_filtrado, "NOTA_ING", valor_NOTA_ING)
#           novosIndicadoresPercentuais(df_filtrado, "IAN", valor_IAN)
#           novosIndicadoresPercentuais(df_filtrado, "NOTA_MAT", valor_NOTA_MAT)
#           novosIndicadoresPercentuais(df_filtrado, "IAA", valor_IAA)
#           novosIndicadoresPercentuais(df_filtrado, "IPS", valor_IPS)
#           novosIndicadoresPercentuais(df_filtrado, "IEG", valor_IEG)
          
#           resultsFinal = modeloKNN(df_filtrado)
#           st.dataframe(resultsFinal)
#         else:
#            st.error("Necessário alterar algum dos indicadores para realizar a simulação")


# st.divider()



# st.write('''# Simulador
#             - Predição por grupo e também por aluno
#             - "se o aluno x ficar com notas nos índices de 4, 5, 8, 10, 9, o aluno seria classificado como?"
#             - "Qual dos índices o aluno precisa de menos esforço para melhorar mais essa classificação, ou qual precisa de mais ajuda?"
#          ''')