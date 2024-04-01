# PAGINA INICIAL
#   INICIALIZAR COM AMBIENTE QUE ESTA NA PASTA env_datathon -> datathon_env\Scripts\activate

#Importação das bibliotecas
import streamlit as st 
import pandas as pd
import plotly.express as px


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

st.write('''## Por Pedra''')
st.divider()

st.write('''## Por Fase''')

st.divider()
st.write('''## Por Aluno''')


st.divider()
st.write('''# Simulador
            - Predição por grupo e também por aluno
            - "se o aluno x ficar com notas nos índices de 4, 5, 8, 10, 9, o aluno seria classificado como?"
            - "Qual dos índices o aluno precisa de menos esforço para melhorar mais essa classificação, ou qual precisa de mais ajuda?"
         ''')