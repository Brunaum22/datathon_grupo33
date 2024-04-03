# PAGINA INICIAL
#   INICIALIZAR COM AMBIENTE QUE ESTA NA PASTA env_datathon -> datathon_env\Scripts\activate

# Importação das bibliotecas
import re
import numpy as np
import pandas as pd
import streamlit as st
from utils import carrega_dados, carrega_csv_ideb, verifica_fase
import plotly.express as px

# ----------------------------------------------------------------------------------
# CONFIG DA PAGINA
# ----------------------------------------------------------------------------------
st.set_page_config(
    page_title="Passos Magicos",
    page_icon=":male-student:",
    layout='wide')


# ----------------------------------------------------------------------------------
# Carregar dados e formatar df
# ----------------------------------------------------------------------------------

df = carrega_dados()

df_2020 = pd.DataFrame()
df_2021 = pd.DataFrame()
df_2022 = pd.DataFrame()

for col in df.columns:
    if re.search('2020', col, re.IGNORECASE):
        # print(f"Campo com 2020 : {col}")
        df_2020["ANO"] = 2020
        df_2020[col] = df[col]
    elif re.search('2021', col, re.IGNORECASE):
        # print(f"Campo com 2021 : {col}")
        df_2021["ANO"] = 2021
        df_2021[col] = df[col]
    elif re.search('2022', col, re.IGNORECASE):
        # print(f"Campo com 2022 : {col}")
        df_2022["ANO"] = 2022
        df_2022[col] = df[col]
    else:
        df_2020[col] = df[col]
        df_2021[col] = df[col]
        df_2022[col] = df[col]

for col in df_2020.columns:
    # print(col)
    if re.search('2020', col, re.IGNORECASE):
        df_2020 = df_2020.rename(columns={col: col[:-5]})

for col in df_2021.columns:
    # print(col)
    if re.search('2021', col, re.IGNORECASE):
        df_2021 = df_2021.rename(columns={col: col[:-5]})

for col in df_2022.columns:
    # print(col)
    if re.search('2022', col, re.IGNORECASE):
        df_2022 = df_2022.rename(columns={col: col[:-5]})

df_concat = pd.concat([df_2020, df_2021, df_2022])

df_concat["NULO"] = df_concat.isnull().sum(1)
df_concat["NULO"] = df_concat["NULO"].map({41: True, np.NaN: True})
df_concat["NULO"] = df_concat["NULO"].map({True: True, np.NaN: False})
df_concat = df_concat.query("NULO == False")

df_base = df_concat[df_concat.columns[:-1]]

dffilter_base = df_base[df_base['INDE'].notnull()]

# ----------------------------------------------------------------------------------
# df final, com os dados de 2022, sem nulos para a coluna FASE #
dffilter_base_2022 = dffilter_base.query("ANO == 2022")


# ----------------------------------------------------------------------------------
dffilter_base_2022['FASE_IDEB'] = dffilter_base_2022.apply(verifica_fase, axis=1)
dffilter_base_2022['FASE_IDEB'] = dffilter_base_2022['FASE_IDEB'].replace({
    'Ano inicial': 'Anos Iniciais',
    'Ano final': 'Anos Finais',
    'Ensino medio': 'Ensino Médio'})

# ----------------------------------------------------------------------------------
# criando df IDEB de Embu-Guaçu
# ----------------------------------------------------------------------------------
ideb_embu = {
    'MUNICIPIO': ['Embu-guaçu', 'Embu-guaçu', 'Embu-guaçu'],
    'ANO_ESCOLAR': ['Anos Iniciais', 'Anos Finais', 'Ensino Medio'],
    'APRENDIZADO': [5.8584, 5.1828, 4.3872],
    'FLUXO': [0.9968, 0.997, 0.99]}

ideb_embu = pd.DataFrame(ideb_embu)
ideb_embu['ANO_ESCOLAR'] = ideb_embu['ANO_ESCOLAR'].replace({'Ensino Medio': 'Ensino Médio'})
ideb_embu = ideb_embu.set_index('ANO_ESCOLAR')
ideb_embu['IDEB'] = (ideb_embu['APRENDIZADO'] * ideb_embu['FLUXO']).round(1)

# ----------------------------------------------------------------------------------
# criando df IDEB da Passos
# ----------------------------------------------------------------------------------
ideb_passos = pd.DataFrame(columns=['MUNICIPIO', 'ANO_ESCOLAR', 'APRENDIZADO', 'FLUXO'])
ideb_passos['MUNICIPIO'] = ['Passos', 'Passos', 'Passos']
ideb_passos['ANO_ESCOLAR'] = dffilter_base_2022['FASE_IDEB'].unique()  # Valores únicos da coluna "FASE_IDEB"
ideb_passos['APRENDIZADO'] = dffilter_base_2022.groupby('FASE_IDEB')[['NOTA_PORT', 'NOTA_MAT']].mean().mean(
    axis=1).values
ideb_passos['FLUXO'] = 1
ideb_passos['ANO_ESCOLAR'] = ideb_passos['ANO_ESCOLAR'].replace({
    'Ano inicial': 'Anos Iniciais',
    'Ano final': 'Anos Finais',
    'Ensino medio': 'Ensino Médio'})

ideb_passos['IDEB'] = (ideb_passos['APRENDIZADO'] * ideb_passos['FLUXO']).round(1)
ideb_passos = ideb_passos.set_index('ANO_ESCOLAR')
ideb_passos = ideb_passos.reindex(['Anos Iniciais', 'Anos Finais', 'Ensino Médio'])

# -------------------
# TITULO da página
# -------------------
st.title("Comparando a PM com a região de Embu-Guaçu:female-student:")

st.markdown('''
## O que é o IDEB e como ele é calculado?\n
Sigla para "Índice de Desenvolvimento da Educação Básica", é um indicador que mede a qualidade do ensino nas escolas públicas, 
criado em 2007 pelo governo federal.
\n\nÉ calculado como a média dos resultados padronizados do Saeb (Sistema de Avaliação de Educação Básica) de português 
e matemática multiplicados pela taxa de aprovação do Censo Escolar (fluxo).
''')

st.write(
    "Acesse o IDEB completo da região de Embu-Guaçu aqui: [IDEB Embu-Guaçu](https://qedu.org.br/municipio/3515103-embu-guacu/ideb)")

# -------------------
# LISTAS
# -------------------
opcoes_anos = ['Anos Iniciais', 'Anos Finais', 'Ensino Médio']

# ----------------------------------------------------------------------------------
# Grafico IDEB Passos Magicos x Região
# ----------------------------------------------------------------------------------
df_ideb_concat = pd.concat([ideb_embu, ideb_passos])

col1_ideb, col2_ideb, col3_ideb = st.columns(3)
with col2_ideb:
    fig = px.bar(df_ideb_concat, x=df_ideb_concat.index, y='IDEB', color='MUNICIPIO', text='IDEB', barmode='group',
                 color_discrete_map={'Embu-guaçu': 'green', 'Passos': 'blue'})
    fig.update_layout(
        title='Comparação do IDEB entre Embu-Guaçu e Passos',
        xaxis_title='Ano Escolar',
        yaxis_title='IDEB')
    fig.update_traces(texttemplate='%{text:.2f}', textposition='inside',
                      textfont=dict(size=15, color='white', family='Arial'))
    st.plotly_chart(fig)

st.divider()

# ----------------------------------------------------------------------------------
# Descrição dos critérios de notas (PORT, MAT e APRENDIZADO)
# ----------------------------------------------------------------------------------
st.markdown(''' ## Para classificar o Aprendizado, os seguintes critérios foram utilizados:\n ''')

col1_crit, col2_crit, col3_crit = st.columns(3)
with col1_crit:
    st.subheader('''
    - Anos iniciais:
    Aprendizado adequado :green[≥ 7,5]\n
    Acima da média (bem posicionados) :orange[≥ 5,8]\n
    Abaixo da média (ou perto dela) :orange[≥ 5,0]\n 
    Muito abaixo da média esperada :red[< 5,0] ''')

with col2_crit:
    st.subheader('''
    - Anos finais:
    Aprendizado adequado :green[≥ 6,7]\n
    Acima da média (bem posicionados) :orange[≥ 5,4]\n
    Abaixo da média (ou perto dela) :orange[≥ 4,6]\n
    Muito abaixo da média esperada :red[< 4,6] ''')

with col3_crit:
    st.subheader('''
    - Ensino médio:
    Aprendizado adequado :green[≥ 6,7]\n
    Acima da média (bem posicionados) :orange[≥ 5,0]\n
    Abaixo da média (ou perto dela) :orange[≥ 4,2]\n
    Muito abaixo da média esperada :red[< 4,2] ''')

st.write("\n")
st.write("FONTE: https://qedu.org.br/uf/35-sao-paulo")
st.divider()


# ----------------------------------------------------------------------------------
# Plot média das notas (PORT, MAT e APRENDIZADO)
# ----------------------------------------------------------------------------------


def verifica_nota_port():
    if fase_selecionada == 'Anos Iniciais':
        if mean_port >= 7.5:
            return ":green[Aprendizado adequado!]"
        elif mean_port >= 5.8:
            return ":orange[Acima da média (bem posicionados)!]"
        elif mean_port >= 5:
            return ":orange[Abaixo da média (ou perto dela)!]"
        else:
            return ":red[Muito abaixo da média esperada!]"
    elif fase_selecionada == 'Anos Finais':
        if mean_port >= 6.7:
            return ":green[Aprendizado adequado!]"
        elif mean_port >= 5.4:
            return ":orange[Acima da média (bem posicionados)!]"
        elif mean_port >= 4.6:
            return ":orange[Abaixo da média (ou perto dela)!]"
        else:
            return ":red[Muito abaixo da média esperada!]"
    elif fase_selecionada == 'Ensino Médio':
        if mean_port >= 6.7:
            return ":green[Aprendizado adequado!]"
        elif mean_port >= 5:
            return ":orange[Acima da média (bem posicionados)!]"
        elif mean_port >= 4.2:
            return ":orange[Acima da média (bem posicionados)!]"
        else:
            return ":red[Muito abaixo da média esperada!]"


def verifica_nota_mat():
    if fase_selecionada == 'Anos Iniciais':
        if mean_mat >= 7.5:
            return ":green[Aprendizado adequado!]"
        elif mean_mat >= 5.8:
            return ":orange[Acima da média (bem posicionados)!]"
        elif mean_mat >= 5:
            return ":orange[Acima da média (bem posicionados)!]"
        else:
            return ":red[Muito abaixo da média esperada!]"
    elif fase_selecionada == 'Anos Finais':
        if mean_mat >= 6.7:
            return ":green[Aprendizado adequado!]"
        elif mean_mat >= 5.4:
            return ":orange[Acima da média (bem posicionados)!]"
        elif mean_mat >= 4.6:
            return ":orange[Acima da média (bem posicionados)!]"
        else:
            return ":red[Muito abaixo da média esperada!]"
    elif fase_selecionada == 'Ensino Médio':
        if mean_mat >= 6.7:
            return ":green[Aprendizado adequado!]"
        elif mean_mat >= 5:
            return ":orange[Acima da média (bem posicionados)!]"
        elif mean_mat >= 4.2:
            return ":orange[Acima da média (bem posicionados)!]"
        else:
            return ":red[Muito abaixo da média esperada!]"


# Ajustando SELECTBOX
col1_select, col2_select, col3_select = st.columns(3)
fase_selecionada = col2_select.selectbox("", opcoes_anos, key='fase_selecionada')

# Ajustando colunas do conteúdo
col1_nota, col2_nota, col3_nota, col4 = st.columns([1.5, 0.5, 1, 1])
with col1_nota:
    df_notas = dffilter_base_2022[dffilter_base_2022['FASE_IDEB'] == fase_selecionada]
    mean_port = df_notas['NOTA_PORT'].mean()
    mean_mat = df_notas['NOTA_MAT'].mean()
    aprendizado = (mean_port + mean_mat) / 2

    if fase_selecionada == 'Anos Iniciais':
        st.subheader("Do 1º ano ao 5º ano escolar")
        st.write("\n")
        st.subheader(f"Português: {verifica_nota_port()}")
        st.subheader(f"Matemática: {verifica_nota_mat()}")

    elif fase_selecionada == 'Anos Finais':
        st.subheader("Do 6º ano ao 9º ano escolar")
        st.write("\n")
        st.subheader(f"Português: {verifica_nota_port()}")
        st.subheader(f"Matemática: {verifica_nota_mat()}")

    elif fase_selecionada == 'Ensino Médio':
        st.subheader("Período dos 3 anos do Ensino Médio")
        st.write("\n")
        st.subheader(f"Português: {verifica_nota_port()}")
        st.subheader(f"Matemática: {verifica_nota_mat()}")

with col3_nota:
    df_plot = pd.DataFrame({'Fase IDEB': [fase_selecionada, fase_selecionada, fase_selecionada],
                            'Média da Nota': [mean_port, mean_mat, aprendizado],
                            'Disciplina': ['Português', 'Matemática', 'Aprendizado'],
                            'Nota': [mean_port, mean_mat, aprendizado]})

    fig = px.bar(df_plot, x='Disciplina', y='Média da Nota', text='Nota', color='Disciplina',
                 title=f'Médias por Disciplina na Passos Mágicos para: {fase_selecionada}',
                 color_discrete_map={'Português': 'Lightgreen', 'Matemática': 'skyblue', 'Aprendizado': 'lightblue'})
    fig.update_traces(texttemplate='%{text:.2f}', textposition='inside',
                      textfont=dict(size=20, color='black', family='Arial'))
    st.plotly_chart(fig)

st.divider()

# ----------------------------------------------------------------------------------
# Tabela de ranking IDEB da região de Embu-Guaçu + simulação da posição da PM
# ----------------------------------------------------------------------------------
df_table = carrega_csv_ideb()
# Preparando novo 'ideb_passos_new' para tabela
ideb_passos_new = ideb_passos.reset_index()
ideb_passos_new = ideb_passos_new.rename(columns={'ANO_ESCOLAR': 'FASE_IDEB', 'MUNICIPIO': 'ESCOLA'})
ideb_passos_new = ideb_passos_new[['ESCOLA', 'FASE_IDEB', 'IDEB']]
ideb_passos_new['ESCOLA'] = ideb_passos_new['ESCOLA'].replace({'Passos': 'PASSOS MÁGICOS'})

ideb_passos_concat = pd.concat([ideb_passos_new, df_table])
ideb_passos_concat.sort_values(by=['IDEB'], ascending=False)

# Ajustando SELECTBOX 2
col1_select_2, col2_select_2, col3_select_2 = st.columns(3)
fase_selecionada_2 = col2_select_2.selectbox("", opcoes_anos, key='fase_selecionada_2')

df_notas = dffilter_base_2022[dffilter_base_2022['FASE_IDEB'] == fase_selecionada_2]
mean_port = df_notas['NOTA_PORT'].mean()
mean_mat = df_notas['NOTA_MAT'].mean()
aprendizado_2 = (mean_port + mean_mat) / 2

# Ajustando colunas do conteúdo
col1_tabela, col2_tabela = st.columns([1.7, 1])
with col1_tabela:
    st.subheader("Ranking das escolas com os maiores IDEBs + Passos Mágicos "
                 "\n(Considerando base oficial da página do IDEB: https://qedu.org.br/municipio/3515103-embu-guacu/baixar-dados)")

    st.write("\n")
    st.markdown(f"_:green[Filtro ativo: {fase_selecionada_2}]_")
    st.dataframe(
        ideb_passos_concat.query(f"FASE_IDEB == '{fase_selecionada_2}'").sort_values(by=['IDEB'], ascending=False),
        hide_index=True)

    st.write("\n")
    st.write(
        'Com esta tabela podemos simular a posição da Passos Mágicos no ranking das escolas com os melhores IDEBs, se fosse considerada uma escola.\n\n'
        'Com isso, percebemos a sua importância e relevância no desenvolvimento da qualidade de ensino da região.')

with col2_tabela:
    st.subheader("Quanto seria o IDEB da Passos Mágicos em 2022?")
    st.markdown(f"_:green[Filtro ativo: {fase_selecionada_2}]_")

    for i in range(100, 89, -1):
        fluxo = i / 100
        st.markdown(
            f"IDEB seria :green[{aprendizado_2 * fluxo:,.2f}] se o fluxo fosse {fluxo:,.2f}, para {fase_selecionada_2};", )

    st.write("\n")
    st.write('* Fluxo: é a taxa de aprovação. Um fluxo de 1 é obtido caso 100% dos alunos forem aprovados.')
    st.write('* IDEB: é obtido pelo produto entre o campo "Aprendizado" e "Fluxo".')
    st.write('* Aprendizado: é obtido pela média aritmética das notas entre Português e Matemática. (Port + Mat)/2')

st.divider()
