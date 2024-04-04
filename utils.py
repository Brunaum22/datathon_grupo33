import streamlit as st
import pandas as pd
import plotly.express as px
import re
import numpy as np
from sklearn import *
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

listEstatistic = []

def carrega_dados():
    df = pd.read_csv("files/PEDE_PASSOS_DATASET_FIAP.csv", sep=";")
    return df


def carrega_csv_ideb():
    df_table_ideb = pd.read_csv("files/ideb_territorios_3515103.csv", sep=";", encoding='latin1')
    return df_table_ideb


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
    df_ano.rename(columns={"NOME": f"NOME_{ano}"}, inplace=True)

    # Filtrando para deixar apenas as colunas do ano escolhido
    df_ano = df_ano.filter(like=f"{ano}")

    # Renomeando as colunas para retirar o ano
    df_ano.columns = df_ano.columns.str.replace(f"_{ano}", "")

    # -----------------
    # TRATANDO E CONVERTENDO COLUNAS
    # -----------------
    df_ano["INDE"] = df_ano["INDE"].apply(lambda x: 0 if re.search('[a-zA-Z]', str(x)) else x)
    df_ano["INDE"] = pd.to_numeric(df_ano["INDE"])
    df_ano["INDE"] = df_ano["INDE"].apply(lambda x: x if x <= 10 and x >= 0 else 0)

    df_ano["IEG"] = pd.to_numeric(df_ano["IEG"])
    df_ano["IAN"] = pd.to_numeric(df_ano["IAN"])
    df_ano["IDA"] = pd.to_numeric(df_ano["IDA"])

    df_ano["IAA"] = pd.to_numeric(df_ano["IAA"])
    df_ano["IPS"] = pd.to_numeric(df_ano["IPS"])
    df_ano["IPP"] = pd.to_numeric(df_ano["IPP"])
    df_ano["IPV"] = pd.to_numeric(df_ano["IPV"])

    df_ano["FASE"] = pd.to_numeric(df_ano["FASE"])

    if ano >= 2022:
        df_ano["ANO_INGRESSO"] = df_ano["ANO_INGRESSO"].astype(int)

    return df_ano


# -------------------------------------------------------
# -------------------------------------------------------

def aluno_fase_pedra_inde(df):
    # Pegando colunas com "FASE"
    df_filter1 = df.copy()
    df_filter1.rename(columns={"NOME": "NOME_FASE"}, inplace=True)
    df_filter1 = df_filter1.filter(like="FASE")
    df_filter1.rename(columns={"NOME_FASE": "NOME"}, inplace=True)
    df_filter1["FASE_TURMA_2020"] = df_filter1["FASE_TURMA_2020"].str[0]
    df_filter1.rename(columns={"FASE_TURMA_2020": "FASE_2020"}, inplace=True)
    df_filter1.fillna(0, inplace=True)

    # Pegando colunas com "INDE"
    df_filter2 = df.copy()
    df_filter2.rename(columns={"NOME": "NOME_INDE"}, inplace=True)
    df_filter2 = df_filter2.filter(like="INDE")
    df_filter2.rename(columns={"NOME_INDE": "NOME"}, inplace=True)
    df_filter2.fillna(0, inplace=True)

    # Pegando colunas com "PEDRA"
    df_filter3 = df.copy()
    df_filter3.rename(columns={"NOME": "NOME_PEDRA"}, inplace=True)
    df_filter3 = df_filter3.filter(like="PEDRA")
    df_filter3.rename(columns={"NOME_PEDRA": "NOME"}, inplace=True)
    df_filter3.fillna(0, inplace=True)

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


# -------------------------------------------------------
# -------------------------------------------------------
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

        # -------------------------------------------------------


# -------------------------------------------------------
def map_campos(df, campo):
    if campo == "PEDRA":
        map_pedras = {"Topázio": "1 - Topázio", "Ametista": "2 - Ametista", "Ágata": "3 - Ágata",
                      "Quartzo": "4 - Quartzo"}

        for coluna in df.columns:
            if coluna.startswith("PEDRA_"):
                df[f"{coluna}"] = df[f"{coluna}"].map(map_pedras)

        return df

    if campo == "FASE":
        map_fases = {0.0: "Alpha", 1.0: "Fase 1", 2.0: "Fase 2", 3.0: "Fase 3", 4.0: "Fase 4", 5.0: "Fase 5",
                     6.0: "Fase 6", 7.0: "Fase 7", 8.0: "Fase 8"}

        for coluna in df.columns:
            if coluna.startswith("FASE_"):
                df[f"{coluna}"] = df[f"{coluna}"].map(map_fases)
        return df


# Identificar se a fase do aluno na PM é "Ano Inicial, Final ou Ensino Médio"
def verifica_fase(row):
    fase = row['FASE']
    if pd.isna(fase):
        return None  # Se algum dos valores for nulo
    elif fase <= 2:
        return "Ano inicial"
    elif 2 < fase < 5:
        return "Ano final"
    elif 5 <= fase < 8:
        return "Ensino medio"
    else:
        return "Universidade"


def converterFloat(df, campo):
    df[campo] = round(pd.to_numeric(df[campo],"coerce"), 2)

def trata_base_classif(df, tipo,  campos=[]):
    df_2020 = pd.DataFrame()
    df_2021 = pd.DataFrame()
    df_2022 = pd.DataFrame()

    for col in df.columns:
        if re.search('2020', col , re.IGNORECASE):
            #print(f"Campo com 2020 : {col}")
            df_2020["ANO"] = 2020
            df_2020[col] = df[col]
        elif re.search('2021', col , re.IGNORECASE):
            #print(f"Campo com 2021 : {col}")
            df_2021["ANO"] = 2021
            df_2021[col] = df[col]
        elif re.search('2022', col , re.IGNORECASE):
            #print(f"Campo com 2022 : {col}")
            df_2022["ANO"] = 2022
            df_2022[col] = df[col]
        else:
            df_2020[col] = df[col]
            df_2021[col] = df[col]
            df_2022[col] = df[col]

    for col in df_2020.columns:
        #print(col)
        if re.search('2020', col , re.IGNORECASE):
            df_2020 = df_2020.rename(columns={col: col[:-5]})

    for col in df_2021.columns:
        #print(col)
        if re.search('2021', col , re.IGNORECASE):
            df_2021 = df_2021.rename(columns={col: col[:-5]})

    for col in df_2022.columns:
        #print(col)
        if re.search('2022', col , re.IGNORECASE):
            df_2022 = df_2022.rename(columns={col: col[:-5]})

    df_concat = pd.concat([df_2020, df_2021, df_2022])

    df_concat["NULO"] = df_concat.isnull().sum(1)
    df_concat["NULO"] = df_concat["NULO"].map({41: True, np.NaN: True})
    df_concat["NULO"] = df_concat["NULO"].map({True: True, np.NaN: False})

    df_concat = df_concat.query("NULO == False")
    df_base = df_concat[df_concat.columns[:-1]]
    dffilter_base = df_base[df_base['INDE'].notnull()]
    if (tipo == "p"):
        dffilter_base = dffilter_base[dffilter_base['NOTA_PORT'].notnull()]
        dffilter_base = dffilter_base[dffilter_base['NOTA_ING'].notnull()]
        dffilter_base = dffilter_base[dffilter_base['NOTA_MAT'].notnull()]

    dffilter_base['FASE_NUM'] = dffilter_base['FASE_TURMA'].str.slice(0, 1)
    converterFloat(dffilter_base, "INDE")
    converterFloat(dffilter_base, "IPV")
    converterFloat(dffilter_base, "IDA")
    converterFloat(dffilter_base, "IPP")
    converterFloat(dffilter_base, "NOTA_PORT")
    converterFloat(dffilter_base, "NOTA_ING")
    converterFloat(dffilter_base, "IAN")
    converterFloat(dffilter_base, "NOTA_MAT")
    converterFloat(dffilter_base, "IAA")
    converterFloat(dffilter_base, "IPS")
    converterFloat(dffilter_base, "IEG")

    capturarMediaPedra(dffilter_base)
    dffilter_base['MEDIA'] = dffilter_base['PEDRA'].apply(gerarMedia)
    dffilter_base['STATUS'] = np.where(dffilter_base['INDE'] <= dffilter_base['MEDIA'], 'DESENVOLVER', 'BOM')

    
    if len(campos) != 0:
        return dffilter_base[campos]

    return dffilter_base

def container(variavel):
    container = st.container(border=True)
    return container.slider("% " + variavel, 0, 100, 0)

def filtra(df, tipo, valor):
    if tipo == "pedra":
        return df.query("PEDRA == '" + valor + "'")
    elif tipo == "fase":
        return df.query("FASE_NUM == '" + valor + "'")
    elif tipo == "nome":
        if valor != "":
            return df.query("NOME == '" + valor + "'")
        else:
            return df
        
def capturarMediaPedra(df):
    
    dados_estatist = df.groupby('PEDRA').describe()
    
    for x in dados_estatist.index:
        varEstatistc = []
        varEstatistc.append(x)
        varEstatistc.append(dados_estatist.loc[(x), ('INDE', '50%')])
        listEstatistic.append(varEstatistc)
    
    return listEstatistic

def gerarMedia(pedra):
  for x in listEstatistic:
    if pedra == x[0]:
      return x[1]

def novosIndicadoresPercentuais(df, ind, valor):
    if ind != 0:
        nome_var = "novo_" + ind
        df[nome_var] = ((valor / 100) * df[ind]) + df[ind]
        return df

def modeloKNN(df_filtrado):
        df_mod_semna = df_filtrado[["STATUS", "IPV", "IDA", "IPP", "NOTA_PORT", "NOTA_ING", "IAN", "NOTA_MAT", "IAA", "IPS", "IEG"]].dropna(axis=0, how='any')
        x = df_mod_semna[["IPV", "IDA", "IPP", "NOTA_PORT", "NOTA_ING", "IAN", "NOTA_MAT", "IAA", "IPS", "IEG"]]
        y = df_mod_semna['STATUS']

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, stratify=y, random_state=42)

        modelo_classificador = KNeighborsClassifier(n_neighbors=5)

        modelo_classificador.fit(x_train, y_train)

        #vars = df_filtrado["IPV"], df_filtrado["IDA"], df_filtrado["IPP"], df_filtrado["NOTA_PORT"], df_filtrado["NOTA_ING"], df_filtrado["IAN"], df_filtrado["NOTA_MAT"], df_filtrado["IAA"], df_filtrado["IPS"], df_filtrado["IEG"]

        resultsFinal = []
        for i in range(len(df_filtrado)):
          var = [df_filtrado.iloc[i, 14], df_filtrado.iloc[i, 15], df_filtrado.iloc[i, 16], df_filtrado.iloc[i, 17], df_filtrado.iloc[i, 18], df_filtrado.iloc[i, 19], df_filtrado.iloc[i, 20], df_filtrado.iloc[i, 21], df_filtrado.iloc[i, 22], df_filtrado.iloc[i, 23]]
          results = []
          results.append(df_filtrado.iloc[i, 0])
          results.append(modelo_classificador.predict([var]))
          results.append(df_filtrado.iloc[i, 1])
          results.append(df_filtrado.iloc[i, 2])
          results.append(df_filtrado.iloc[i, 3])
          results.append(df_filtrado.iloc[i, 4])
          results.append(df_filtrado.iloc[i, 5])
          results.append(df_filtrado.iloc[i, 6])
          results.append(df_filtrado.iloc[i, 7])
          results.append(df_filtrado.iloc[i, 8])
          results.append(df_filtrado.iloc[i, 9])
          results.append(df_filtrado.iloc[i, 10])
          results.append(df_filtrado.iloc[i, 11])
          results.append(df_filtrado.iloc[i, 12])
          results.append(df_filtrado.iloc[i, 13])

          resultsFinal.append(results)

        novos_nomes = {
            0: "STATUS",
            1: "novo_STATUS",
            2: "ANO",
            3: "NOME",
            4: "PEDRA",
            5: "IPV",
            6: "IDA",
            7: "IPP",
            8: "NOTA_PORT",
            9: "NOTA_ING",
            10: "IAN",
            11: "NOTA_MAT",
            12: "IAA",
            13: "IPS",
            14: "IEG"
        }       
        df_resultado = pd.DataFrame(resultsFinal)
        df_resultado = df_resultado.rename(columns=novos_nomes)
        return df_resultado
