import streamlit as st 
import pandas as pd
import plotly.express as px
import re 

def carrega_dados():
    df = pd.read_csv("files/PEDE_PASSOS_DATASET_FIAP.csv", sep=";")
    return df

# FUNCAO PARA PODER PADRONIZAR AS INFORMACOES, BASEADO NA ESCOLHA DA PESSOA NA PAGINA
def separa_anos(df, ano):  
    # Se for 2020, limpar df
    df["FASE_2020"] = df["FASE_TURMA_2020"].str[0]
    df["TURMA_2020"] = df["FASE_TURMA_2020"].str[1]
    
    # #Limpando info errada q foi inputado no df
    df = df[df["FASE_2020"] != 'D']    
        
    # Retirando alunos que não estava no ano escolhido  
    df_ano = df[df[f"PEDRA_{ano}"].notna()]
    
    # Renomeando a coluna de nome para poder manter no df depois
    df_ano.rename(columns={"NOME":f"NOME_{ano}"}, inplace=True)
    
    # Filtrando para deixar apenas as colunas do ano escolhido
    df_ano = df_ano.filter(like=f"{ano}")
    
    # Renomeando as colunas para retirar o ano
    df_ano.columns = df_ano.columns.str.replace(f"_{ano}","")

    #-----------------
    # TRATANDO E CONVERTENDO COLUNAS
    #-----------------
    df_ano["INDE"] = df_ano["INDE"].apply(lambda x: 0 if re.search('[a-zA-Z]', str(x)) else x)     
    df_ano["INDE"] = pd.to_numeric(df_ano["INDE"]) 
    df_ano["INDE"] = df_ano["INDE"].apply(lambda x: x if x <= 10 and x >= 0 else 0)
    
    df_ano["IEG"] = pd.to_numeric(df_ano["IEG"] )
    df_ano["IAN"] = pd.to_numeric(df_ano["IAN"] )
    df_ano["IDA"] = pd.to_numeric(df_ano["IDA"] )
    
    df_ano["IAA"] = pd.to_numeric(df_ano["IAA"] )
    df_ano["IPS"] = pd.to_numeric(df_ano["IPS"] )
    df_ano["IPP"] = pd.to_numeric(df_ano["IPP"] )
    df_ano["IPV"] = pd.to_numeric(df_ano["IPV"] )
    
    df_ano["FASE"] = pd.to_numeric(df_ano["FASE"])
    
    # Rankeando as pedras
    #map_pedras = {"Quartzo":"1 - Quartzo", "Ágata":"2 - Ágata", "Ametista":"3 - Ametista", "Topázio":"4 - Topázio"}
    #df_ano["PEDRA"] = df_ano["PEDRA"].map(map_pedras)
    
    return df_ano
