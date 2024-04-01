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
  page_title="Passos Magicos",
  page_icon=":male-student:",
  layout='wide'
)


st.title("Comparando a PM com demais escolas da cidade 	:female-student:")


