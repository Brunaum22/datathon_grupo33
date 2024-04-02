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
    
    if ano >= 2022:
        df_ano["ANO_INGRESSO"] = df_ano["ANO_INGRESSO"].astype(int)
    
    
    return df_ano
#-------------------------------------------------------
#-------------------------------------------------------

def aluno_fase_pedra_inde(df):    
    
    # Pegando colunas com "FASE"
    df_filter1 = df.copy()
    df_filter1.rename(columns={"NOME":"NOME_FASE"},inplace=True)
    df_filter1 = df_filter1.filter(like="FASE")
    df_filter1.rename(columns={"NOME_FASE":"NOME"},inplace=True)
    df_filter1["FASE_TURMA_2020"] = df_filter1["FASE_TURMA_2020"].str[0]
    df_filter1.rename(columns={"FASE_TURMA_2020":"FASE_2020"},inplace=True)
    df_filter1.fillna(0,inplace=True)

    # Pegando colunas com "INDE"
    df_filter2 = df.copy()
    df_filter2.rename(columns={"NOME":"NOME_INDE"},inplace=True)
    df_filter2 = df_filter2.filter(like="INDE")
    df_filter2.rename(columns={"NOME_INDE":"NOME"},inplace=True)
    df_filter2.fillna(0,inplace=True)

    # Pegando colunas com "PEDRA"
    df_filter3 = df.copy()
    df_filter3.rename(columns={"NOME":"NOME_PEDRA"},inplace=True)
    df_filter3 = df_filter3.filter(like="PEDRA")
    df_filter3.rename(columns={"NOME_PEDRA":"NOME"},inplace=True)
    df_filter3.fillna(0,inplace=True)

    # juntando em um só
    df_filtro_full = pd.merge(df_filter1, df_filter2, on="NOME")
    df_filtro_full = pd.merge(df_filtro_full, df_filter3, on="NOME")   
    
    
    
    # Convertendo
    df_filtro_full = df_filtro_full[df_filtro_full["FASE_2020"] != 'D']
    df_filtro_full = df_filtro_full[df_filtro_full["INDE_2020"] != 'D']
    df_filtro_full = df_filtro_full[df_filtro_full["INDE_2021"] != 'D']
    df_filtro_full = df_filtro_full[df_filtro_full["INDE_2022"] != 'D']
    df_filtro_full = df_filtro_full[df_filtro_full["INDE_2020"] != '#NULO!']
    df_filtro_full = df_filtro_full[df_filtro_full["INDE_2021"] != '#NULO!']
    df_filtro_full = df_filtro_full[df_filtro_full["INDE_2022"] != '#NULO!']        

    df_filtro_full["FASE_2020"] = pd.to_numeric(df_filtro_full["FASE_2020"])
    df_filtro_full["INDE_2020"] = pd.to_numeric(df_filtro_full["INDE_2020"])
    df_filtro_full["INDE_2021"] = pd.to_numeric(df_filtro_full["INDE_2021"])
    df_filtro_full["INDE_2022"] = pd.to_numeric(df_filtro_full["INDE_2022"])    
        
    return df_filtro_full


#-------------------------------------------------------
#-------------------------------------------------------
def cria_flags(row, tipo):
    if tipo == 'veterano':
        if row['INDE_2020'] > 0 and row['INDE_2021'] > 0 and row['INDE_2022'] > 0:
            return 1
        else:
            return 0

    
    status_2020 = row["PEDRA_2020"][0]
    status_2021 = row["PEDRA_2021"][0]
    status_2022 = row["PEDRA_2022"][0]

    if tipo == 'evolucao_pedra_20_21':              
        if status_2021 > status_2020:
            return 2
        if status_2021 < status_2020:
            return 0
        if status_2020 == status_2021:
            return 1
    
    if tipo == 'evolucao_pedra_20_21':              
        if status_2021 > status_2020:
            return 2
        if status_2021 < status_2020:
            return 0
        if status_2020 == status_2021:
            return 1
    
    if tipo == 'evolucao_pedra_21_22':              
        if status_2022 > status_2021:
            return 2
        if status_2022 < status_2021:
            return 0
        if status_2022 == status_2021:
            return 1
    
    if tipo == 'evolucao_pedra_20_22':              
        if status_2020 > status_2021:
            return 2
        if status_2020 < status_2021:
            return 0
        if status_2020 == status_2021:
            return 1 
        
#-------------------------------------------------------
#-------------------------------------------------------
def map_campos(df,campo):
    if campo == "PEDRA":
        map_pedras = {"Topázio":"1 - Topázio","Ametista":"2 - Ametista", "Ágata": "3 - Ágata", "Quartzo": "4 - Quartzo"}
        
        for coluna in df.columns:
            if coluna.startswith("PEDRA_"):        
                df[f"{coluna}"] = df[f"{coluna}"].map(map_pedras)
        
        return df

    if campo == "FASE":
        map_fases = {0.0:"Alpha", 1.0:"Fase 1", 2.0:"Fase 2", 3.0:"Fase 3", 4.0:"Fase 4", 5.0:"Fase 5", 6.0:"Fase 6", 7.0:"Fase 7", 8.0:"Fase 8"}
        
        for coluna in df.columns:
            if coluna.startswith("FASE_"):        
                df[f"{coluna}"] = df[f"{coluna}"].map(map_fases)
        return df

   