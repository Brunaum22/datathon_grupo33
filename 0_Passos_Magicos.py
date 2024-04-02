# PAGINA INICIAL
#   INICIALIZAR COM AMBIENTE QUE ESTA NA PASTA env_datathon -> datathon_env\Scripts\activate

# Importação das bibliotecas
import streamlit as st 
import pandas as pd
import plotly.express as px


##----------------------------------------------------------------------------------
# CONFIG DA PAGINA
##----------------------------------------------------------------------------------
st.set_page_config(
  page_title="Passos Magicos",
  page_icon=":male-student:"
)

st.title("Bem vindo(a) a Plataforma de Analytics da Passos Magicos! :star2:")

st.image("files/passos_magicos_logo.png")


st.markdown("<h1 style='text-align: center; '>Quem somos</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

col1.write(
  '''
  A **Associação Passos Mágicos** tem uma trajetória de mais de 30 anos de atuação, trabalhando na transformação da vida de crianças e jovens de baixa renda os levando a melhores oportunidades de vida.)
  '''
)

col2.write(
  '''
  A transformação, idealizada por Michelle Flues e Dimetri Ivanoff, começou em 1992, atuando dentro de orfanatos, no município de Embu-Guaçu.
  '''  
)

col3.write(
  '''
  Em 2016, depois de anos de atuação, decidem ampliar o programa para que mais jovens tivessem acesso a essa fórmula mágica para transformação que inclui: educação de qualidade, auxílio psicológico/psicopedagógico, ampliação de sua visão de mundo e protagonismo. Passaram então a atuar como um projeto social e educacional, criando assim a Associação Passos Mágicos.
  '''
)


##----------------------
##----------------------
st.divider()
st.markdown("<h1 style='text-align: center; '>Missão e visão</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

col1.write(
  '''
    ### Missão
    Nossa missão é transformar a vida de jovens e crianças, oferecendo ferramentas para levá-los a melhores oportunidades de vida.
  '''
)

col2.write(
  '''
    ### Visão
    Nossa visão é viver em um Brasil no qual todas as crianças e jovens têm iguais oportunidades para realizarem seus sonhos e são agentes transformadores de suas próprias vidas.
  '''
)

##----------------------
##----------------------
st.divider()

st.markdown("<h1 style='text-align: center;'> Nossos valores </h1>", unsafe_allow_html = True)
col1, col2 = st.columns(2)

col1.write(
''' 
- Empatia :two_hearts: 
 
- Amor ao aprendizado :heart:

- Poder em acreditar em si e no próximo :smile:

- Pertencimento 	:dolls:

'''
)


col2.write(
'''
- Gratidão :shamrock:

- Busca pelo saber 	:female-technologist:

- Educação que transforma e ajuda a transformar :student:

- Aprender a aprender 	:female-teacher:
'''
)



##----------------------
##----------------------
st.divider()

st.markdown("<h1 style='text-align: center;'> O que fazemos? </h1>", unsafe_allow_html = True)

col1, col2, col3 = st.columns(3)

col1.write(
'''
### Aceleração do Conhecimento
- Educação de qualidade, programas educacionais, assistência psicológica e ampliação da visão de mundo. Conheça mais sobre nosso trabalho.

- A Associação Passos Mágicos oferece aulas de alfabetização, língua portuguesa e matemática para crianças e adolescentes, de 7 a 17 anos, que sejam baixa renda e moradores do município de Embu-Guaçu. Os alunos são divididos por nível de conhecimento, determinado por meio de uma prova de sondagem que é realizada ao ingressarem na Passos Mágicos, e são inseridos em turmas que variam da alfabetização até o nível 8
'''
)

col2.write(
'''
### Programas Especiais

- Conheça nosso projeto de apadrinhamento e de intercâmbio, visando uma maior integração dos alunos com diferentes ambientes e culturas.

- A Associação Passos Mágicos oferece oportunidades para alunos destacados, permitindo que estudem em escolas particulares por meio do programa de apadrinhamento.

- Mensalmente, a ONG promove encontros para apresentar seus programas, incluindo o de apadrinhamento, onde alunos com evolução demonstrada têm suas histórias compartilhadas com potenciais doadores. 
'''
)

col3.write(
'''
### Eventos e Ações Sociais

- Anualmente, em prol dos alunos, são promovidas campanhas de arrecadação para presentear as centenas de crianças e adolescentes Passos Mágicos.

'''
)


##----------------------
##----------------------
st.divider()
st.write("Saiba mais no site: https://passosmagicos.org.br/")

st.write('''
          ## Criado por: 
          - Bruno Silva Lopes ( rm350566 )
          - Henrique Eiji Hashimoto ( rm350096 )
          - Rodrigo Araújo ( rm349801 ) 
          - Roney Molina ( rm430014 )

         ''')

