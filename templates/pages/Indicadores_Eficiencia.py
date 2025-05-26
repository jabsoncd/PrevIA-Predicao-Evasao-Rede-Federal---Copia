import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
import folium
from folium import Choropleth
from streamlit_folium import folium_static
import openai
import requests
import os
from dotenv import load_dotenv 


st.set_page_config(
    page_title="Plataforma PrevIA",
    page_icon="previa_azulmenor.png",

    layout="wide",
    initial_sidebar_state="expanded"  # collapsed expanded
)

# Ocultar barra streamlit
hide_st_style = """
    <style>:
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 🔹 Ocultar apenas os links Home, Indicadores e Simulador do sidebar
# st.markdown(
#     """ 
#     <style>
#     section[data-testid="stSidebar"] a[href*="templates/Home_Eficiencia"],
#     section[data-testid="stSidebar"] a[href*="pages/Indicadores_Eficiencia"],
#     section[data-testid="stSidebar"] a[href*="pages/Simulador_Eficiencia"] {
#         display: none !important;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )
# CSS para ocultar links com nomes específicos no sidebar
st.markdown(
    """
    <style>
    section[data-testid="stSidebar"] a[href*="Home_Eficiencia"],
    section[data-testid="stSidebar"] a[href*="Indicadores_Eficiencia"],
    section[data-testid="stSidebar"] a[href*="Simulador_Eficiencia"] {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Estilo CSS para customizar o fundo da barra lateral
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-color: #f5f7fa;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# Carregar os dados
# @st.cache_data
# microdados_eficiencia_academica_RedeFederal_2023_tecnico_RegiaoMetropolitana #base_redeFederal_2022_tecnico_regiaoMetropolitana
file_path = 'artifacts/microdados_eficiencia_academica_RedeFederal_2023_tecnico_RegiaoMetropolitana.csv'
# '../artifacts/base_redeFederal_2022_tecnico_regiaoMetropolitana.csv'
df = pd.read_csv(file_path, delimiter=';')


# Criar colunas para centralizar a imagem
# Ajuste as proporções conforme necessário
col1, col2, col3 = st.sidebar.columns([1, 5, 1])
with col2:  # Centraliza a imagem na coluna do meio
    st.image("images/previa_cinza_menor.png", width=300)

# 🔹 Centraliza o título
st.markdown("<h2 style='text-align: center; color: #12125c; margin-bottom: 5px;'>Inteligência Artificial para Predição da Evasão na Rede Federal EPCT</h2>", unsafe_allow_html=True)

# 🔹 Texto introdutório centralizado
st.markdown("<p style='text-align: center; color: #1e1e8f; margin-top: 0px;'>Plataforma para análise do comportamento da evasão na RFEPCT.</p>", unsafe_allow_html=True)

# 🔹 Texto introdutório centralizado
st.markdown("<p style='text-align: center; color: #3f3f4f; margin-top: 0px;'>Olá! Conheça os indicadores relacionados a evasão na Rede Federal EPCT </p>", unsafe_allow_html=True)
# Linha divisória
st.write("---")
# Botão para voltar à página Home.py
st.markdown(
    """
    <style>
        .botao-voltar {
            position: absolute;
            top: 10px;
            left: 10px;
            background-color: #004A99; /* Azul escuro */
            color: white !important;
            padding: 10px 20px;
            text-decoration: none;
            font-size: 16px;
            font-weight: bold;
            border: none;
            display: inline-block;
            text-align: center;
            cursor: pointer;
            margin-top: -20px;
        }
        .botao-voltar:hover {
            background-color: #003366; /* Azul mais escuro no hover */
        }
    </style>
    <a class="botao-voltar" href="https://previa.streamlit.app/~/+/" target="_self">Voltar para Home</a>
    """,
    unsafe_allow_html=True
)
st.markdown("<p style='text-align: center; color: #3f3f4f; margin-top: 0px;'> </p>",
            unsafe_allow_html=True)
st.write("---")


# Menu
st.sidebar.title("Filtros")

st.sidebar.markdown("Situação das Matrículas")
CATEGORIA_SITUACAO = st.sidebar.multiselect(
    key=1,
    label="Categoria da Situação",
    placeholder="Selecione a situação",
    options=df["CATEGORIA_SITUACAO"].unique(),
)
st.sidebar.markdown("---")
st.sidebar.markdown("Demográficos")
REGIAO = st.sidebar.multiselect(
    key=2,
    label="Região",
    placeholder="Selecione a Região",
    options=sorted(df["REGIAO"].unique()),
)
UF = st.sidebar.multiselect(
    key=3,
    label="Unidade da Federação",
    placeholder="Selecione a UF",
    options=sorted(df["UF"].unique()),
)
INSTITUICAO = st.sidebar.multiselect(
    key=4,
    label="Instituição",
    placeholder="Selecione a Instituição",
    # format_func=lambda x: "Todos" if x == -1 else f"INSTITUICAO {x}",
    options=sorted(df["INSTITUICAO"].unique()),
    # default=df["INSTITUICAO"].unique()
)
UNIDADE_DE_ENSINO = st.sidebar.multiselect(
    key=5,
    label="Unidade de Ensino",
    placeholder="Selecione a Unidade de Ensino",
    # format_func=lambda x: "Todos" if x == -1 else f"INSTITUICAO {x}",
    options=sorted(df["UNIDADE_DE_ENSINO"].unique()),
    # default=df["INSTITUICAO"].unique()
)
REGIÃO_METROPOLINA_UE = st.sidebar.multiselect(
    key=6,
    label="Unidade de Ensino",
    placeholder="Selecione a Região Metropolitana",
    # format_func=lambda x: "Todos" if x == -1 else f"INSTITUICAO {x}",
    options=sorted(df["REGIÃO_METROPOLINA_UE"].unique()),
    # default=df["INSTITUICAO"].unique()
)
st.sidebar.markdown("---")
st.sidebar.markdown("Sociais")
COR_RACA = st.sidebar.multiselect(
    key=7,
    label="Cor/Raça",
    placeholder="Selecione a Cor/Raça",
    options=sorted(df["COR_RACA"].unique())
)
SEXO = st.sidebar.multiselect(
    key=8,
    label="Gênero",
    placeholder="Selecione o Gênero",
    options=sorted(df["SEXO"].unique())
)
RENDA_FAMILIAR = st.sidebar.multiselect(
    key=9,
    label="Renda Familiar",
    placeholder="Selecione a Renda Familiar",
    options=sorted(df["RENDA_FAMILIAR"].unique())
)
st.sidebar.markdown("---")
st.sidebar.markdown("Cursos")
EIXO_TECNOLOGICO = st.sidebar.multiselect(
    key=10,
    label="Eixo tecnológico",
    placeholder="Selecione o Eixo tecnológico",
    options=sorted(df["EIXO_TECNOLOGICO"].unique())
)
NOME_DE_CURSO = st.sidebar.multiselect(
    key=11,
    label="Curso técnico",
    placeholder="Selecione o curso técnico",
    options=sorted(df["NOME_DE_CURSO"].unique())
)
MODALIDADE_DE_ENSINO = st.sidebar.multiselect(
    key=12,
    label="Modalidade de ensino",
    placeholder="Selecione a modalidade de ensino",
    options=sorted(df["MODALIDADE_DE_ENSINO"].unique())
)
TIPO_DE_OFERTA = st.sidebar.multiselect(
    key=13,
    label="Tipo de Oferta",
    placeholder="Selecione o Tipo de Oferta",
    options=sorted(df["TIPO_DE_OFERTA"].unique())
)
TURNO = st.sidebar.multiselect(
    key=14,
    label="Turno",
    placeholder="Selecione o turno",
    options=sorted(df["TURNO"].unique())
)


# Filtrando o DataFrame de acordo com as seleções da sidebar
filtered_df = df.copy()

# Aplicando os filtros, verificando se o filtro não está vazio
if CATEGORIA_SITUACAO:
    filtered_df = filtered_df[filtered_df['CATEGORIA_SITUACAO'].isin(
        CATEGORIA_SITUACAO)]

if REGIAO:
    filtered_df = filtered_df[filtered_df['REGIAO'].isin(REGIAO)]

if UF:
    filtered_df = filtered_df[filtered_df['UF'].isin(UF)]

if INSTITUICAO:
    filtered_df = filtered_df[filtered_df['INSTITUICAO'].isin(INSTITUICAO)]

if UNIDADE_DE_ENSINO:
    filtered_df = filtered_df[filtered_df['INSTITUICAO'].isin(
        UNIDADE_DE_ENSINO)]

if REGIÃO_METROPOLINA_UE:
    filtered_df = filtered_df[filtered_df['INSTITUICAO'].isin(
        REGIÃO_METROPOLINA_UE)]

if COR_RACA:
    filtered_df = filtered_df[filtered_df['COR_RACA'].isin(COR_RACA)]

if SEXO:
    filtered_df = filtered_df[filtered_df['SEXO'].isin(SEXO)]

if RENDA_FAMILIAR:
    filtered_df = filtered_df[filtered_df['RENDA_FAMILIAR'].isin(
        RENDA_FAMILIAR)]

if EIXO_TECNOLOGICO:
    filtered_df = filtered_df[filtered_df['EIXO_TECNOLOGICO'].isin(
        EIXO_TECNOLOGICO)]

if NOME_DE_CURSO:
    filtered_df = filtered_df[filtered_df['NOME_DE_CURSO'].isin(NOME_DE_CURSO)]

if MODALIDADE_DE_ENSINO:
    filtered_df = filtered_df[filtered_df['MODALIDADE_DE_ENSINO'].isin(
        MODALIDADE_DE_ENSINO)]

if TIPO_DE_OFERTA:
    filtered_df = filtered_df[filtered_df['TURNO'].isin(TIPO_DE_OFERTA)]

if TURNO:
    filtered_df = filtered_df[filtered_df['TURNO'].isin(TURNO)]


st.write(" ")
st.write(" ")


# # CSS customizado para estilizar os botões
# st.markdown("""
#     <style>
#         .button-container {
#             display: flex;
#             justify-content: space-between;
#             width: 100%;
#             margin-top: 20px;
#         }
#         .button-container button {
#             flex: 1;
#             margin: 0;
#             background-color: #4CAF50;
#             color: white;
#             border: none;
#             padding: 15px 0;
#             text-align: center;
#             cursor: pointer;
#             font-size: 16px;
#             transition: background-color 0.3s;
#             font-weight: bold;
#         }
#         .button-container button:hover {
#             background-color: #45a049;
#         }
#         .button-container button:active {
#             background-color: #3e8e41;
#         }
#     </style>
# """, unsafe_allow_html=True)

# # Se não houver uma chave de estado para a aba selecionada, vamos definir a padrão.
# if 'selected_tab' not in st.session_state:
#     st.session_state.selected_tab = "📈 Indicadores Demográficos"

# # Criando os botões com CSS personalizado
# st.markdown("""
#     <div class="button-container">
#         <button onclick="window.location.href='#'">📈 Indicadores Demográficos</button>
#         <button onclick="window.location.href='#'">Sociais</button>
#         <button onclick="window.location.href='#'">🗃 Cursos</button>
#         <button onclick="window.location.href='#'">Mapa da Evasão</button>
#     </div>
# """, unsafe_allow_html=True)


# CSS para alinhar os botões corretamente e manter a letra branca no botão selecionado
st.markdown("""
    <style>
        .button-row {
            display: flex;
            width: 100%;
        }
        .stButton button {
            flex-grow: 5;
            width: 100% !important;
            height: 50px;
            background-color: #004A99;
            color: white !important;  /* Garante que o texto sempre seja branco */
            border: none;
            text-align: center;
            cursor: pointer;
            font-size: 17px;
            font-weight: bold;
            transition: background-color 0.3s, transform 0.3s;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        /* Primeiro botão - cantos arredondados à esquerda */
        div[data-testid="stHorizontalBlock"] > div:first-child .stButton button {
            border-radius: 0;
        }
        /* Último botão - cantos arredondados à direita */
        div[data-testid="stHorizontalBlock"] > div:last-child .stButton button {
            border-radius: 0;
        }
        /* Botões do meio - sem arredondamento */
        div[data-testid="stHorizontalBlock"] > div:not(:first-child):not(:last-child) .stButton button {
            border-radius: 0;
        }
        /* Efeito hover */
        .stButton button:hover {
            background-color: #4554a0;
            transform: scale(1.05);
        }
        /* Efeito ao clicar */
        .stButton button:active {
            background-color: #3e428e;
        }
        /* Mantém a cor branca mesmo quando o botão estiver selecionado */
        .stButton button:focus, .stButton button:visited {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)


# Se não houver uma chave de estado para a aba selecionada, definir padrão.
if 'selected_tab' not in st.session_state:
    st.session_state.selected_tab = "📈 Demográficos"

# Criar colunas igualmente distribuídas
cols = st.columns(4)

# Botões de navegação dentro das colunas
with cols[0]:
    if st.button("📈 Demográficos"):
        st.session_state.selected_tab = "📈 Demográficos"

with cols[1]:
    if st.button("📊 Sociais"):
        st.session_state.selected_tab = "📊 Sociais"

with cols[2]:
    if st.button("🗃 Cursos"):
        st.session_state.selected_tab = "🗃 Cursos"

with cols[3]:
    if st.button("🗺 Mapa da Evasão"):
        st.session_state.selected_tab = "🗺 Mapa da Evasão"


# Exibir conteúdo com base na seleção do botão
if st.session_state.selected_tab == "📈 Demográficos":
    st.header("Demográficos")
    st.write("Indicadores Demográficos")

    # Contagem dos valores para cada status
    status_counts = filtered_df['CATEGORIA_SITUACAO'].value_counts()

    # Exibindo os totais em cartões
    # Verificando as categorias exatas com base nos valores encontrados
    evadidos = status_counts.get("Evadidos", 0)
    em_curso = status_counts.get("Em Curso", 0)
    concluintes = status_counts.get("Concluídos", 0)
    total = evadidos + em_curso + concluintes

    # Calculando percentuais
    evadidos_pct = evadidos / total * 100
    em_curso_pct = em_curso / total * 100
    concluintes_pct = concluintes / total * 100

    # Usando colunas para exibir os cards lado a lado
    col1, col2, col3 = st.columns(3)

    # Exibindo as métricas nos cartões, com formatação de número e cores diferentes
    with col1:
        st.markdown("<div style='background-color: #fa5923; padding: 4px; border-radius: 20px; text-align: center; color: white;'>"
                    "<h3>Evadidos</h3>"
                    f"<h2 style='color:white'>{evadidos:,.0f}".replace(
                        ',', '.')+"</h2>"
                    f"<p style='color:white;font-size:16px'>({evadidos_pct:.2f}%)</p>"
                    "</div>", unsafe_allow_html=True
                    )

    with col2:
        st.markdown("<div style='background-color: #0f91f5; padding: 4px; border-radius: 20px; text-align: center; color: white;'>"
                    "<h3>Em Curso</h3>"
                    f"<h2 style='color:white'>{em_curso:,.0f}".replace(
                        ',', '.')+"</h2>"
                    f"<p style='color:white;font-size:16px'>({em_curso_pct:.2f}%)</p>"
                    "</div>", unsafe_allow_html=True
                    )

    with col3:
        st.markdown("<div style='background-color: #10de73; padding: 4px; border-radius: 20px; text-align: center; color: white;'>"
                    "<h3>Concluintes</h3>"
                    f"<h2 style='color:white'>{concluintes:,.0f}".replace(
                        ',', '.')+"</h2>"
                    f"<p style='color:white;font-size:16px'>({concluintes_pct:.2f}%)</p>"
                    "</div>", unsafe_allow_html=True
                    )

    # Gráfico de barras com total de evadidos, em curso e concluintes
    fig1 = px.bar(x=status_counts.index,
                  y=status_counts.values,
                  title='Total de Evadidos, Em Curso e Concluintes',
                  labels={'x': 'Categoria', 'y': 'Quantidade'},
                  color=status_counts.index,  # Diferentes cores para cada categoria
                  color_discrete_sequence=px.colors.qualitative.Bold,  # Paleta de cores ajustada
                  template="plotly_dark"  # Fundo preto
                  )
    st.plotly_chart(fig1)

    # Configuração da chave de API
    # load_dotenv()  # Carrega variáveis do .env
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Adicionar CSS personalizado
    st.markdown("""
        <style>
            /* Estilo do botão */
            .stButton>button {
                background-color: #191ea6;  /* Cor de fundo */
                color: white;               /* Cor do texto */
                border: 2px solid #191ea6;  /* Cor da borda */
                padding: 10px 24px;         /* Tamanho do botão */
                font-size: 16px;            /* Tamanho da fonte */
                border-radius: 8px;         /* Bordas arredondadas */
                cursor: pointer;           /* Cursor de mão */
            }
            /* Efeito ao passar o mouse sobre o botão */
            .stButton>button:hover {
                background-color: #1a73ab;  /* Cor de fundo ao passar o mouse */
                border-color: #1a73ab;      /* Cor da borda ao passar o mouse */
                color: white;               /* Cor do texto */
            }
        </style>
    """, unsafe_allow_html=True)
    # Criação do botão "Insights chatGPT"
    if st.button('Insights chatGPT', key="insights_button"):
        # Solicitar insights via ChatGPT

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": f'O dataset a seguir corresponde aos dados de matrículas em cursos técnicos separados por categorias de matrículas: Em curso, Concluintes e Evadidos. Me informe 3 insights sobre este dataset {fig1}'}
            ],
            temperature=0.7,
            max_tokens=500  # Limite o tamanho da resposta
        )

        # Exibir os insights
        st.markdown(response['choices'][0]['message']['content'])

    # Agrupar os evadidos por instituição
    evadidos_por_instituicao = filtered_df[filtered_df['CATEGORIA_SITUACAO']
                                           == 'Evadidos']['INSTITUICAO'].value_counts().reset_index()
    evadidos_por_instituicao.columns = ['Instituição', 'Número de Evadidos']

    # Criar o treemap
    fig2 = px.treemap(
        evadidos_por_instituicao,
        path=['Instituição'],  # Define a hierarquia do treemap
        values='Número de Evadidos',
        title='Evadidos por Instituição',
        color='Número de Evadidos',  # Cor baseada na quantidade de evadidos
        color_continuous_scale='Viridis'  # Escolhe uma escala de cores
    )
    fig2.update_traces(
        # hovertemplate='<b>%{label}</b><br>Número de Evadidos: %{value:,d}<extra></extra>'
        hovertemplate='<b>%{label}</b><br>Número de Evadidos: %{value:,d}<br>Percentual sobre matrículas: %{customdata[0]}%<extra></extra>'
    )
    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig2)

    # Criação do botão "Insights chatGPT"
    if st.button('Insights chatGPT', key="insights_button2"):
        # Solicitar insights via ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": f'O dataset a seguir corresponde aos dados de matrículas em cursos técnicos separados por categorias de matrículas: Em curso, Concluintes e Evadidos. Me informe 3 insights sobre este dataset {fig2}'}
            ],
            temperature=0.7,
            max_tokens=500  # Limite o tamanho da resposta
        )

        # Exibir os insights
        st.markdown(response['choices'][0]['message']['content'])

    # Agrupar os evadidos por instituição
    evadidos_por_instituicao = filtered_df[filtered_df['CATEGORIA_SITUACAO']
                                           == 'Evadidos']['INSTITUICAO'].value_counts().reset_index()
    evadidos_por_instituicao.columns = ['Instituição', 'Número de Evadidos']

    # Gráfico de mapa do Brasil com a quantidade de evadidos por UF
    uf_counts = filtered_df[filtered_df['CATEGORIA_SITUACAO']
                            == 'Evadidos']['UF'].value_counts().reset_index()
    uf_counts.columns = ['uf', 'count']

    evadidos_por_instituicao = filtered_df[filtered_df['CATEGORIA_SITUACAO']
                                           == 'Evadidos']['UF'].value_counts()
    # figuf = px.bar(x=evadidos_por_instituicao.index, y=evadidos_por_instituicao.values, labels={
    #     'x': 'UF', 'y': 'Número de Evadidos'}, title='Evadidos por UF',
    #     color=evadidos_por_instituicao.index,  # Cores diferentes por UF
    #     color_discrete_sequence=px.colors.qualitative.Bold)  # Paleta de cores vibrante)
    # Criando gráfico de barras com fundo preto
    figuf = px.bar(
        x=evadidos_por_instituicao.index,
        y=evadidos_por_instituicao.values,
        labels={'x': 'UF', 'y': 'Número de Evadidos'},
        title='Evadidos por UF',
        color=evadidos_por_instituicao.index,  # Cores diferentes por UF
        color_discrete_sequence=px.colors.qualitative.Bold,  # Paleta de cores vibrantes
        template="plotly_dark"  # Fundo preto
    )
    st.plotly_chart(figuf)

    # Criação do botão "Insights chatGPT"
    if st.button('Insights chatGPT', key="insights_button3"):
        # Solicitar insights via ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": f'O dataset a seguir corresponde aos dados de matrículas em cursos técnicos separados por categorias de matrículas: Em curso, Concluintes e Evadidos. Me informe 3 insights sobre este dataset {figuf}'}
            ],
            temperature=0.7,
            max_tokens=500  # Limite o tamanho da resposta
        )

        # Exibir os insights
        st.markdown(response['choices'][0]['message']['content'])


elif st.session_state.selected_tab == "📊 Sociais":
    st.header("Sociais")
    st.write("Indicadores Sociais")
    # Adicione o código relevante aqui

    # Contagem dos valores para cada status
    status_counts = filtered_df['CATEGORIA_SITUACAO'].value_counts()

    # Exibindo os totais em cartões
    # Verificando as categorias exatas com base nos valores encontrados
    evadidos = status_counts.get("Evadidos", 0)
    em_curso = status_counts.get("Em Curso", 0)
    concluintes = status_counts.get("Concluídos", 0)
    total = evadidos + em_curso + concluintes

    # Calculando percentuais
    evadidos_pct = evadidos / total * 100
    em_curso_pct = em_curso / total * 100
    concluintes_pct = concluintes / total * 100

    # Usando colunas para exibir os cards lado a lado
    col1, col2, col3 = st.columns(3)

    # Exibindo as métricas nos cartões, com formatação de número e cores diferentes
    with col1:
        st.markdown("<div style='background-color: #fa5923; padding: 4px; border-radius: 20px; text-align: center; color: white;'>"
                    "<h3>Evadidos</h3>"
                    f"<h2 style='color:white'>{evadidos:,.0f}".replace(
                        ',', '.')+"</h2>"
                    f"<p style='color:white;font-size:16px'>({evadidos_pct:.2f}%)</p>"
                    "</div>", unsafe_allow_html=True
                    )

    with col2:
        st.markdown("<div style='background-color: #0f91f5; padding: 4px; border-radius: 20px; text-align: center; color: white;'>"
                    "<h3>Em Curso</h3>"
                    f"<h2 style='color:white'>{em_curso:,.0f}".replace(
                        ',', '.')+"</h2>"
                    f"<p style='color:white;font-size:16px'>({em_curso_pct:.2f}%)</p>"
                    "</div>", unsafe_allow_html=True
                    )

    with col3:
        st.markdown("<div style='background-color: #10de73; padding: 4px; border-radius: 20px; text-align: center; color: white;'>"
                    "<h3>Concluintes</h3>"
                    f"<h2 style='color:white'>{concluintes:,.0f}".replace(
                        ',', '.')+"</h2>"
                    f"<p style='color:white;font-size:16px'>({concluintes_pct:.2f}%)</p>"
                    "</div>", unsafe_allow_html=True
                    )

    # Gráfico de evadidos por renda familiar
    fig4 = px.histogram(df[df['CATEGORIA_SITUACAO'] == 'Evadidos'],
                        x='RENDA_FAMILIAR',
                        title='Evadidos por Renda Familiar')
    st.plotly_chart(fig4)

    # Criação do botão "Insights chatGPT"
    if st.button('Insights chatGPT', key="insights_button4"):
        # Solicitar insights via ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": f'O dataset a seguir corresponde aos dados de matrículas em cursos técnicos separados por categorias de matrículas: Em curso, Concluintes e Evadidos. Me informe 3 insights sobre este dataset {fig4}'}
            ],
            temperature=0.7,
            max_tokens=500  # Limite o tamanho da resposta
        )

        # Exibir os insights
        st.markdown(response['choices'][0]['message']['content'])

    # Gráfico de colunas de evadidos por sexo
    sexo_counts = filtered_df[filtered_df['CATEGORIA_SITUACAO']
                              == 'Evadidos']['SEXO'].value_counts()
    # Gráfico de barras com fundo preto e cores personalizadas para o gráfico de "Evadidos por Sexo"
    fig5 = px.bar(
        x=sexo_counts.index,
        y=sexo_counts.values,
        title='Evadidos por Sexo',
        labels={'x': 'Sexo', 'y': 'Quantidade de Evadidos'},
        # Cores diferentes para cada categoria (Masculino e Feminino)
        color=sexo_counts.index,
        color_discrete_sequence=px.colors.qualitative.Bold,  # Paleta de cores
        template="plotly_dark"  # Fundo preto
    )
    st.plotly_chart(fig5)

    # Criação do botão "Insights chatGPT"
    if st.button('Insights chatGPT', key="insights_button5"):
        # Solicitar insights via ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": f'O dataset a seguir corresponde aos dados de matrículas em cursos técnicos separados por categorias de matrículas: Em curso, Concluintes e Evadidos. Me informe 3 insights sobre este dataset {fig5}'}
            ],
            temperature=0.7,
            max_tokens=500  # Limite o tamanho da resposta
        )

        # Exibir os insights
        st.markdown(response['choices'][0]['message']['content'])

    # Gráfico de dispersão de evadidos por idade
    # fig6 = px.scatter(df[df['CATEGORIA_SITUACAO'] == 'Evadidos'], x='IDADE', y='REGIAO', title='Evadidos por Idade', labels={'id': 'Número de Evadidos'})
    # st.plotly_chart(fig6)

    # Gráfico de pizza de evadidos por cor e raça
    cor_raca_counts = filtered_df[filtered_df['CATEGORIA_SITUACAO']
                                  == 'Evadidos']['COR_RACA'].value_counts()
    fig7 = px.bar(
        x=cor_raca_counts.index,
        y=cor_raca_counts.values,
        title='Evadidos por Cor/Raça',
        labels={'x': 'Cor/Raça', 'y': 'Quantidade de Evadidos'},
        color=cor_raca_counts.index,  # Cores diferentes para cada categoria de cor/race
        color_discrete_sequence=px.colors.qualitative.Bold,  # Paleta de cores
        template="plotly_dark"  # Fundo preto
    )
    st.plotly_chart(fig7)

    # Criação do botão "Insights chatGPT"
    if st.button('Insights chatGPT', key="insights_button6"):
        # Solicitar insights via ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": f'O dataset a seguir corresponde aos dados de matrículas em cursos técnicos separados por categorias de matrículas: Em curso, Concluintes e Evadidos. Me informe 3 insights sobre este dataset {fig7}'}
            ],
            temperature=0.7,
            max_tokens=500  # Limite o tamanho da resposta
        )

        # Exibir os insights
        st.markdown(response['choices'][0]['message']['content'])


elif st.session_state.selected_tab == "🗃 Cursos":
    st.header("Cursos")
    st.write("Indicadores Cursos")
    # Adicione o código relevante aqui

    # Contagem dos valores para cada status
    status_counts = filtered_df['CATEGORIA_SITUACAO'].value_counts()

    # Exibindo os totais em cartões
    # Verificando as categorias exatas com base nos valores encontrados
    evadidos = status_counts.get("Evadidos", 0)
    em_curso = status_counts.get("Em Curso", 0)
    concluintes = status_counts.get("Concluídos", 0)
    total = evadidos + em_curso + concluintes

    # Calculando percentuais
    evadidos_pct = evadidos / total * 100
    em_curso_pct = em_curso / total * 100
    concluintes_pct = concluintes / total * 100

    # Usando colunas para exibir os cards lado a lado
    col1, col2, col3 = st.columns(3)

    # Exibindo as métricas nos cartões, com formatação de número e cores diferentes
    with col1:
        st.markdown("<div style='background-color: #fa5923; padding: 4px; border-radius: 20px; text-align: center; color: white;'>"
                    "<h3>Evadidos</h3>"
                    f"<h2 style='color:white'>{evadidos:,.0f}".replace(
                        ',', '.')+"</h2>"
                    f"<p style='color:white;font-size:16px'>({evadidos_pct:.2f}%)</p>"
                    "</div>", unsafe_allow_html=True
                    )

    with col2:
        st.markdown("<div style='background-color: #0f91f5; padding: 4px; border-radius: 20px; text-align: center; color: white;'>"
                    "<h3>Em Curso</h3>"
                    f"<h2 style='color:white'>{em_curso:,.0f}".replace(
                        ',', '.')+"</h2>"
                    f"<p style='color:white;font-size:16px'>({em_curso_pct:.2f}%)</p>"
                    "</div>", unsafe_allow_html=True
                    )

    with col3:
        st.markdown("<div style='background-color: #10de73; padding: 4px; border-radius: 20px; text-align: center; color: white;'>"
                    "<h3>Concluintes</h3>"
                    f"<h2 style='color:white'>{concluintes:,.0f}".replace(
                        ',', '.')+"</h2>"
                    f"<p style='color:white;font-size:16px'>({concluintes_pct:.2f}%)</p>"
                    "</div>", unsafe_allow_html=True
                    )

    # Gráfico de Treemap de Evadidos por Eixo Tecnológico
    evadidos_por_eixo = filtered_df[filtered_df['CATEGORIA_SITUACAO']
                                    == 'Evadidos']['EIXO_TECNOLOGICO'].value_counts().reset_index()
    evadidos_por_eixo.columns = ['Eixo tecnológico', 'Número de Evadidos']
    fig9 = px.treemap(
        evadidos_por_eixo,
        # Caminho hierárquico, nível 1: Eixo Tecnológico
        path=['Eixo tecnológico'],
        values='Número de Evadidos',  # Valor a ser representado proporcionalmente
        title='Evadidos por Eixo Tecnológico do Curso',
        color='Número de Evadidos',  # Cores diferentes para cada Eixo Tecnológico
        color_discrete_sequence=px.colors.qualitative.Bold,  # Paleta de cores
        template="plotly_dark"  # Fundo preto
    )
   # Exibir o gráfico de Eixo Tecnológico
    st.plotly_chart(fig9)

    # Criação do botão "Insights chatGPT"
    if st.button('Insights chatGPT', key="insights_button7"):
        # Solicitar insights via ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": f'O dataset a seguir corresponde aos dados de matrículas em cursos técnicos separados por categorias de matrículas: Em curso, Concluintes e Evadidos. Me informe 3 insights sobre este dataset {fig9}'}
            ],
            temperature=0.7,
            max_tokens=500  # Limite o tamanho da resposta
        )

        # Exibir os insights
        st.markdown(response['choices'][0]['message']['content'])

    # Contagem de evadidos por curso técnico
    evadidos_por_curso = filtered_df[filtered_df['CATEGORIA_SITUACAO']
                                     == 'Evadidos']['NOME_DE_CURSO'].value_counts()

    # Ordenar os cursos por número de evadidos em ordem decrescente e pegar os 20 primeiros
    top_20_cursos = evadidos_por_curso.sort_values(ascending=True).head(20)

    # Gráfico de barras horizontais
    fig8 = px.bar(
        x=top_20_cursos.values,
        y=top_20_cursos.index,
        orientation='h',  # Gráfico de barras horizontais
        labels={'x': 'Número de Evadidos', 'y': 'Curso Técnico'},
        title='Evadidos por Curso Técnico',
        # color=top_20_cursos.index,  # Cores diferentes para cada curso
        # Paleta de cores (sequential)
        color_discrete_sequence=px.colors.qualitative.Bold,
        template="plotly_dark"  # Fundo preto
    )

    # Ajuste para adicionar barra de rolagem
    fig8.update_layout(
        # Ajustar margens para melhorar o layout
        margin=dict(l=150, r=50, t=50, b=50),
        # Ajuste da exibição do eixo X
        xaxis=dict(title='Número de Evadidos', tickangle=0),
        yaxis=dict(title='Curso Técnico'),  # Ajuste do eixo Y
        showlegend=False  # Esconde a legenda
    )
    # Exibir o gráfico
    st.plotly_chart(fig8)

    # Criação do botão "Insights chatGPT"
    if st.button('Insights chatGPT', key="insights_button8"):
        # Solicitar insights via ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": f'O dataset a seguir corresponde aos dados de matrículas em cursos técnicos separados por categorias de matrículas: Em curso, Concluintes e Evadidos. Me informe 3 insights sobre este dataset {fig8}'}
            ],
            temperature=0.7,
            max_tokens=500  # Limite o tamanho da resposta
        )

        # Exibir os insights
        st.markdown(response['choices'][0]['message']['content'])

    # Limitar a listagem aos 20 cursos mais evadidos
    top_20_cursos = evadidos_por_curso.sort_values(ascending=False)
    # Listagem com o ranking de evadidos pelo nome do curso técnico
    st.markdown(
        "<h2 style='font-size:16px;'>Ranking de Evadidos pelo Nome do Curso Técnico</h2>",
        unsafe_allow_html=True
    )
    # Criar DataFrame para exibir a tabela
    ranking_cursos = top_20_cursos.reset_index()
    ranking_cursos.columns = ['Curso Técnico', 'Número de Evadidos']
    # Exibir a tabela com barra de rolagem
    st.dataframe(ranking_cursos, use_container_width=True)

    # Criação do botão "Insights chatGPT"
    if st.button('Insights chatGPT', key="insights_button12"):
        # Solicitar insights via ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": f'O dataset a seguir corresponde aos dados de matrículas em cursos técnicos separados por categorias de matrículas: Em curso, Concluintes e Evadidos. Me informe 3 insights sobre este dataset {ranking_cursos}'}
            ],
            temperature=0.7,
            max_tokens=500  # Limite o tamanho da resposta
        )

        # Exibir os insights
        st.markdown(response['choices'][0]['message']['content'])

    # Contagem de evadidos por Modalidade de Ensino (Presencial / EaD)
    modalidade_counts = filtered_df[filtered_df['CATEGORIA_SITUACAO']
                                    == 'Evadidos']['MODALIDADE_DE_ENSINO'].value_counts()

    # Criando o gráfico de barras
    fig10 = px.bar(
        x=modalidade_counts.index,  # Modalidades
        y=modalidade_counts.values,  # Número de Evadidos
        labels={'x': 'Modalidade de Ensino', 'y': 'Número de Evadidos'},
        title='Evadidos por Modalidade de Ensino',
        color=modalidade_counts.index,  # Cor diferente para cada Modalidade
        color_discrete_sequence=px.colors.qualitative.Bold,  # Paleta de cores
        template="plotly_dark"  # Fundo preto
    )
    # Exibindo o gráfico
    st.plotly_chart(fig10)

    # Criação do botão "Insights chatGPT"
    if st.button('Insights chatGPT', key="insights_button9"):
        # Solicitar insights via ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": f'O dataset a seguir corresponde aos dados de matrículas em cursos técnicos separados por categorias de matrículas: Em curso, Concluintes e Evadidos. Me informe 3 insights sobre este dataset {fig10}'}
            ],
            temperature=0.7,
            max_tokens=500  # Limite o tamanho da resposta
        )

        # Exibir os insights
        st.markdown(response['choices'][0]['message']['content'])

    # Contagem de evadidos por Tipo de Oferta (Subsequente/Concomitante/Integrado)
    tipo_oferta_counts = filtered_df[filtered_df['CATEGORIA_SITUACAO']
                                     == 'Evadidos']['TIPO_DE_OFERTA'].value_counts()

    # Criando o gráfico de barras
    fig11 = px.bar(
        x=tipo_oferta_counts.index,  # Tipos de Oferta
        y=tipo_oferta_counts.values,  # Número de Evadidos
        labels={'x': 'Tipo da Oferta', 'y': 'Número de Evadidos'},
        title='Evadidos por Tipo da Oferta',
        color=tipo_oferta_counts.index,  # Cores diferentes para cada Tipo de Oferta
        color_discrete_sequence=px.colors.qualitative.Bold,  # Paleta de cores
        template="plotly_dark"  # Fundo preto
    )
    # Exibindo o gráfico
    st.plotly_chart(fig11) 

    # Criação do botão "Insights chatGPT"
    if st.button('Insights chatGPT', key="insights_button10"):
        # Solicitar insights via ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": f'O dataset a seguir corresponde aos dados de matrículas em cursos técnicos separados por categorias de matrículas: Em curso, Concluintes e Evadidos. Me informe 3 insights sobre este dataset {fig11}'}
            ],
            temperature=0.7,
            max_tokens=500  # Limite o tamanho da resposta
        )

        # Exibir os insights
        st.markdown(response['choices'][0]['message']['content'])

    # Contagem de evadidos por Turno
    turno_counts = filtered_df[filtered_df['CATEGORIA_SITUACAO']
                               == 'Evadidos']['TURNO'].value_counts()

    # Ordenar em ordem decrescente
    turno_counts = turno_counts.sort_values(ascending=False)
    # Criando o gráfico de barras
    fig12 = px.bar(
        x=turno_counts.index,  # Turnos
        y=turno_counts.values,  # Número de Evadidos
        labels={'x': 'Turno', 'y': 'Número de Evadidos'},
        title='Evadidos por Turno',
        color=turno_counts.index,  # Cores diferentes para cada Turno
        color_discrete_sequence=px.colors.qualitative.Bold,  # Paleta de cores
        template="plotly_dark"  # Fundo preto
    )

    # Exibindo o gráfico
    st.plotly_chart(fig12)

    # Criação do botão "Insights chatGPT"
    if st.button('Insights chatGPT', key="insights_button11"):
        # Solicitar insights via ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": f'O dataset a seguir corresponde aos dados de matrículas em cursos técnicos separados por categorias de matrículas: Em curso, Concluintes e Evadidos. Me informe 3 insights sobre este dataset {fig12}'}
            ],
            temperature=0.7,
            max_tokens=500  # Limite o tamanho da resposta
        )

        # Exibir os insights
        st.markdown(response['choices'][0]['message']['content'])


elif st.session_state.selected_tab == "🗺 Mapa da Evasão":
    st.header("Mapa da Evasão - Proporção de evadidos")
    st.write("Mapa da Evasão no Brasil")
    # Adicione o código relevante aqui

    # Configuração da página no Streamlit
    # st.set_page_config(page_title="Mapa de Evadidos", layout="wide")

    # Carregar datasets
    data_path = 'artifacts/microdados_eficiencia_academica_RedeFederal_2023_tecnico_RegiaoMetropolitana.csv'
    data_geo = pd.read_csv(data_path, sep=';')

    codUF_path = 'artifacts/codigo_estados.csv'
    data_cod = pd.read_csv(codUF_path, sep=';', encoding='ISO-8859-1')

    # Converter colunas para string
    data_geo['UF'] = data_geo['UF'].astype(str)
    data_cod['SG_UF'] = data_cod['SG_UF'].astype(str)

    # Merge entre dados e códigos de UF
    data_geo_merge = pd.merge(
        data_geo, data_cod, left_on='UF', right_on='SG_UF', how='left')

    # Total de matrículas por UF
    total_por_uf = data_geo_merge.groupby(
        'NM_UF').size().reset_index(name='total_matriculas')

    # Total de evadidos por UF
    evadidos = data_geo_merge[data_geo_merge['CATEGORIA_SITUACAO'] == 'Evadidos']
    evadidos_por_uf = evadidos.groupby(
        'NM_UF').size().reset_index(name='evadidos')

    # Merge para calcular proporção
    proporcao_df = pd.merge(
        total_por_uf, evadidos_por_uf, on='NM_UF', how='left')
    proporcao_df['evadidos'] = proporcao_df['evadidos'].fillna(0)
    proporcao_df['proporcao'] = (
        proporcao_df['evadidos'] / proporcao_df['total_matriculas']) * 100

    # Carregar shapefile dos estados do Brasil (GeoJSON)
    geojson_path = 'BR_UF_2024.geojson'
    gdf_estados = gpd.read_file(geojson_path) 

    # Dissolver para obter geometria por estado
    gdf_estados = gdf_estados.dissolve(by='NM_UF', as_index=False) 

    # Merge com dados de proporção
    gdf_mapa = gdf_estados.merge(proporcao_df, on='NM_UF', how='left')
    gdf_mapa['proporcao'] = gdf_mapa['proporcao'].fillna(0)

    # Centro aproximado do Brasil
    latitude_centro = -14.2350
    longitude_centro = -51.9253

    # Criar mapa base
    mapa = folium.Map(location=[
                      latitude_centro, longitude_centro], tiles="Cartodb Positron", zoom_start=5)

    # Mapa coroplético com proporção
    Choropleth(
        geo_data=gdf_estados,
        data=gdf_mapa,
        columns=['NM_UF', 'proporcao'],
        key_on='properties.NM_UF',
        fill_color='YlOrRd',
        nan_fill_color='white',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Proporção de Evadidos (%) por Estado'
    ).add_to(mapa)

    # Estilo para destaque
    def estilo(x): return {"fillColor": "white",
                           "color": "black", "fillOpacity": 0.001, "weight": 0.001}

    def estilo_destaque(x): return {
        "fillColor": "darkblue", "color": "black", "fillOpacity": 0.5, "weight": 1}

    # Adicionar tooltip com proporção
    highlight = folium.features.GeoJson(
        data=gdf_mapa,
        style_function=estilo,
        highlight_function=estilo_destaque,
        tooltip=folium.features.GeoJsonTooltip(
            fields=['NM_UF', 'proporcao'],
            aliases=['Estado:', 'Proporção de Evadidos (%):'],
            localize=True,
            style=("background: white; color: black"),
            labels=True,
            sticky=True
        )
    )
    highlight.add_to(mapa)

    # Controles
    folium.LayerControl().add_to(mapa)

    # Exibir
    folium_static(mapa, width=1400, height=800)
    # # folium_static(mapa, width=None, height=900)  # Largura automática, altura grande para tela cheia

    # st.title("Mapa Dinâmico do Brasil - Evadidos")
    # Carregar os datasets
    # data_path = '../artifacts/microdados_eficiencia_academica_RedeFederal_2023_tecnico_RegiaoMetropolitana.csv' # #base_redeFederal_2022_tecnico_regiaoMetropolitana
    # codUF_path = '../artifacts/codigo_estados.csv'
    # # Arquivo de limites geográficos
    # geojson_path = '../artifacts/BR_Municipios_2023/BR_Municipios_2023.geojson'

    # # Tentar carregar os arquivos e exibir mensagem de erro caso falhem
    # try:
    #     data_geo = pd.read_csv(data_path, sep=';')
    #     data_cod = pd.read_csv(codUF_path, sep=';', encoding='ISO-8859-1')
    #     gdf_estados = gpd.read_file(geojson_path)
    # except Exception as e:
    #     st.error(f"Erro ao carregar os arquivos: {e}")
    #     st.stop()

    # # Processamento dos dados
    # data_geo['UF'] = data_geo['UF'].astype(str)
    # data_cod['SG_UF'] = data_cod['SG_UF'].astype(str)

    # # Realizar o merge entre os datasets
    # data_geo_merge = pd.merge(
    #     data_geo, data_cod, left_on='UF', right_on='SG_UF', how='left')

    # # Filtrar os evadidos
    # evadidos = data_geo_merge[data_geo_merge['CATEGORIA_SITUACAO'] == 'Evadidos']

    # # Agrupar os dados por estado e contar os evadidos
    # quantitativo_evadidos = evadidos.groupby(
    #     'NM_UF').size().reset_index(name='quantidade')

    # # Ajustar o shapefile dos estados para merge
    # gdf_estados = gdf_estados.dissolve(by='NM_UF', as_index=False)
    # gdf_estados = gdf_estados.rename(columns={'NM_UF': 'NM_UF'})

    # # Merge entre os dados geográficos e os quantitativos
    # gdf_mapa = gdf_estados.merge(quantitativo_evadidos, on='NM_UF', how='left')
    # gdf_mapa['quantidade'] = gdf_mapa['quantidade'].fillna(
    #     0)  # Substituir valores NaN por zero

    # # Criar o mapa base
    # latitude_centro = -14.2350
    # longitude_centro = -51.9253
    # mapa = folium.Map(location=[
    #                 latitude_centro, longitude_centro], tiles="Cartodb Positron", zoom_start=5)

    # # Adicionar camada coroplética
    # Choropleth(
    #     geo_data=gdf_estados,
    #     data=gdf_mapa,
    #     columns=['NM_UF', 'quantidade'],
    #     key_on='properties.NM_UF',
    #     fill_color='viridis',
    #     nan_fill_color='white',
    #     fill_opacity=0.7,
    #     line_opacity=0.2,
    #     legend_name='Número de Evadidos por Estado'
    # ).add_to(mapa)

    # # Funções de estilo para destaque
    # def estilo(x): return {"fillColor": "white",
    #                     "color": "black", "fillOpacity": 0.001, "weight": 0.001}

    # def estilo_destaque(x): return {
    #     "fillColor": "darkblue", "color": "black", "fillOpacity": 0.5, "weight": 1}

    # # Adicionar destaque e tooltip ao mapa
    # highlight = folium.features.GeoJson(
    #     data=gdf_mapa,
    #     style_function=estilo,
    #     highlight_function=estilo_destaque,
    #     tooltip=folium.features.GeoJsonTooltip(
    #         fields=['NM_UF', 'quantidade'],
    #         aliases=['Estado:', 'Evadidos:'],
    #         localize=True,
    #         style=("background: white; color: black")
    #     )
    # )

    # highlight.add_to(mapa)
    # folium.LayerControl().add_to(mapa)

    # # Exibir o mapa no Streamlit

    # folium_static(mapa, width=1400, height=800)
    # # # folium_static(mapa, width=None, height=900)  # Largura automática, altura grande para tela cheia

#########################################################################################################################################################################


# Footer
# Exibir a imagem do footer dentro de um div com a classe definida no CSS
# st.markdown(
#     f"""
#     <div class="footer">
#         <img src="data:image/png;base64,{st.image("../images/footer.png", width=1400, caption="")}" />
#     </div>
#     """,
#     unsafe_allow_html=True
# )
