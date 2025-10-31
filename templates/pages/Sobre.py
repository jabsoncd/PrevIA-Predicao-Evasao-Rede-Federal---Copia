import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
import folium
from folium import Choropleth
from streamlit_folium import folium_static
from streamlit_folium import st_folium
import base64
import openai
import requests
import os
from dotenv import load_dotenv

from pathlib import Path

 
st.set_page_config(
    page_title="Plataforma PrevIA",
    page_icon="images/previa_azulmenor.png",

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
    section[data-testid="stSidebar"] a[href*="Home_Profissional"],
    section[data-testid="stSidebar"] a[href*="Indicadores_Eficiencia_Layout"],
    section[data-testid="stSidebar"] a[href*="Simulador_Eficiencia_Layout"] {
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
#########################################################################################################################################################


# CSS personalizado (barra azul alta com ícones dentro)
st.markdown("""
<style>
    /* 🔹 Barra superior azul */
    .nav-container {
        background-color: #152847;
        height: 2cm; /* Altura da faixa azul */
        display: flex;
        align-items: center;        /* Centraliza verticalmente os botões */
        justify-content: flex-end;  /* Alinha botões à direita */
        padding: 0 3rem;
        border-radius: 8px;
        margin-bottom: 2rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }

    /* 🔹 Botões da barra */
    .nav-button {
        background-color: transparent;
        border: none;
        color: #FFFFFF;
        font-weight: 600;
        font-size: 1.1rem;
        margin-left: 1.2rem;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    .nav-button:hover {
        background-color: rgba(255,255,255,0.15);
        border-radius: 6px;
        transition: 0.2s;
    }

    /* 🔹 Cabeçalhos e cards */
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center
    }
    .sub-header {
        font-size: 1.2rem;
        color: #4B5563;
        text-align: center
    }
    .feature-card {
        background-color: #f5f7fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #3b82f6;
    }
</style>
""", unsafe_allow_html=True)


# Caminho da logo (ajuste se necessário)
logo_path = Path("templates/logo_branca_laranja.png")


# 🔹 Ocultar sidebar
st.markdown("""
    <style>
    [data-testid="stSidebar"] {display: none;}
    </style>
""", unsafe_allow_html=True)
# Estado inicial
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

def get_base64_image(path: Path):
    if not path.exists():
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

logo_b64 = get_base64_image(logo_path)


# Barra azul com logo à esquerda e links à direita
st.markdown(f"""
<style>
.nav-container {{
    background-color: #152847;
    height: 2cm;
    display: flex;
    justify-content: space-between; /* logo à esquerda, links à direita */
    align-items: center;
    width: 100%;
    padding: 0 2rem;
    margin: 0;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 999;
    border-radius: 0; /* <- garante cantos quadrados */
    box-shadow: 0 2px 6px rgba(0,0,0,0.2)
}}

.nav-logo {{
    width: 200px; /* largura da logo */
    height: 60px; /* altura da logo */
    background-image: url("data:image/jpg;base64,{logo_b64}");
    background-size: contain;
    background-repeat: no-repeat;
    background-position: left center;
}}

.nav-links {{
    display: flex;
    gap: 2rem;
}}

.nav-link {{
    color: #FFFFFF;
    font-weight: 600;
    font-size: 1.1rem;
    cursor: pointer;
    text-decoration: none !important;
}}
.nav-link:hover {{
    color: #FFA500; /* laranja claro ao passar o mouse */
    transition: color 0.2s;
}}

/* Espaço no topo para não sobrepor o conteúdo */
.app-content {{
    padding-top: 3.5rem; /* >= altura da nav */
}}

/* Garante que os links não sejam estilizados por padrão do navegador */
a, a:visited, a:active {{
    color: white;
    text-decoration: none;
}}
</style>

<div class="nav-container">
    <div class="nav-logo"></div>
    <div class="nav-links">
        <a class="nav-link" href="/", target="_self">Início</a>
        <a class="nav-link" href="/Simulador_Eficiencia_Layout", target="_self">Simular</a>
        <a class="nav-link" href="/Indicadores_Eficiencia_Layout", target="_self">Indicadores</a>
        <a class="nav-link" href="/Indicadores_Eficiencia_Layout_Gestor", target="_self">Módulo Gestor</a>
        <a class="nav-link" href="/Sobre", target="_self">Sobre</a>
    </div>
</div>

<div class="app-content"></div>
""", unsafe_allow_html=True)







#########################################################################################################################################################
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
    st.image("images/previa_cinza_menor.png", width=300)  # ../images/



# 🔹 Conteúdo das páginas
if st.session_state.current_page == "home":
    st.markdown('<h1 class="main-header">PrevIA - Predição de Evasão na Rede Federal com Inteligência Artificial</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Conheça os indicadores relacionados a evasão em cursos técnicos na Rede Federal EPCT</p>', unsafe_allow_html=True)
# Linha divisória
# st.write("---")





####################################################################################################################

# Configurações da página
# CSS personalizado para centralização e estilo das abas
st.markdown("""
    <style>
        /* Centraliza o conteúdo na tela */
        .main > div {
            display: flex;
            justify-content: center;
        }

        /* Container centralizado e estilizado */
        .stContainer {
            background-color: #b0acac;
            padding: 40px 60px;
            border-radius: 15px;
            box-shadow: 0px 0px 15px rgba(0,0,0,0.1);
            max-width: 500px;
        }

        /* Estilo das abas */
        div[data-baseweb="tab-list"] {
            justify-content: center;
            background-color: #5a7794; /* Azul escuro */
            border-radius: 10px;
            padding: 5px;
        }

        /* Cor do texto nas abas */
        button[data-baseweb="tab"] {
            color: white !important;
            font-weight: 600 !important;
            background: transparent !important;
        }

        /* Aba selecionada */
        button[data-baseweb="tab"][aria-selected="true"] {
            background-color: #0059b3 !important; /* Azul mais claro */
            border-radius: 10px;
        }

        h1, h2, h3, h4, h5 {
            text-align: center;
            color: #00264d;
        }

        p, li {
            text-align: justify;
            color: #333;
        }
    </style>
""", unsafe_allow_html=True)

# Container centralizado
with st.container():
    st.markdown('<div class="stContainer">', unsafe_allow_html=True)

    # Criação das abas
    abas = st.tabs([
        "Apresentação",
        "Objetivo",
        "Metodologia",
        "Desenvolvimento",
        "Publicações e Referências"
    ])

    with abas[0]:
        st.subheader("Apresentação")
        st.markdown(
            """
            O **PrevIA** (Predição de Evasão na Rede Federal com Inteligência Artificial) é uma ferramenta web 
            desenvolvida no contexto da **Tese de Doutorado** vinculada ao **Programa de Pós-Graduação em Modelagem Computacional de Sistemas (PPGMC/UFT)**.  
            O projeto foi conduzido entre os anos de **2024 e 2025** com o propósito de apoiar a **tomada de decisão baseada em dados**, 
            promovendo a análise, visualização e predição do fenômeno da **evasão em cursos técnicos** ofertados pela Rede Federal de Educação Profissional, Científica e Tecnológica (RFEPCT).

            A plataforma foi concebida como um ambiente interativo e informativo, que permite aos gestores educacionais e pesquisadores
            explorar indicadores associados ao comportamento de evasão e simular cenários a partir de modelos de aprendizado de máquina.
            """
        )

    with abas[1]:
        st.subheader("Objetivo")
        st.markdown(
            """
            O principal objetivo do **PrevIA** é **apoiar estratégias de mitigação da evasão escolar** por meio da aplicação de 
            técnicas de **inteligência artificial** e **modelagem preditiva**.  
            A ferramenta busca proporcionar **subsídios analíticos e interpretativos** para gestores e pesquisadores da RFEPCT, 
            possibilitando uma compreensão mais profunda dos fatores que influenciam a permanência e o abandono escolar.

            Além disso, a iniciativa visa **fortalecer a eficiência acadêmica**, reduzir impactos **sociais e financeiros** da evasão
            e contribuir para a **formação profissional inclusiva e sustentável** no Brasil.
            """
        )

    with abas[2]:
        st.subheader("Metodologia")
        st.markdown(
            """
            O desenvolvimento do PrevIA foi estruturado conforme o modelo **CRISP-DM (Cross Industry Standard Process for Data Mining)**,
            contemplando as etapas de **compreensão do problema**, **preparo dos dados**, **modelagem**, **avaliação** e **implementação**.  
            A etapa final envolveu a criação de um **ambiente web interativo** utilizando o framework **Streamlit**, 
            permitindo a simulação de novos cenários de evasão com base no modelo treinado.
            """
        )

    with abas[3]:
        st.subheader("Desenvolvimento")
        st.markdown(
            """
            - **Período:** 2024–2025  
            - **Ambiente de desenvolvimento:** Python 3.11  
            - **Principais bibliotecas:** Streamlit, Pandas, Scikit-learn, CatBoost, SHAP  
            - **Hospedagem:** Plataforma web interativa  
            - **Base de dados:** Dados anonimizados da Rede Federal EPCT  
            """
        )

    with abas[4]:
        st.subheader("Publicações e Referências")
        st.markdown(
            """
            - DIAS, J. C. *PrevIA – Predição de Evasão na Rede Federal com Inteligência Artificial.*  
              Tese (Doutorado em Modelagem Computacional de Sistemas) – Universidade Federal do Tocantins, 2025.  
            - WIRTH, R.; HIPP, J. *CRISP-DM: Towards a Standard Process Model for Data Mining.*  
              In: Proceedings of the 4th International Conference on the Practical Applications of Knowledge Discovery and Data Mining, 2000.  
            - MOLNAR, C. *Interpretable Machine Learning.* 2nd Edition, 2022.
            """
        )

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
    <div style="
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        text-align: center;
        color: #6B7280;
        background-color: #dedede;  /* cinza claro */
        padding: 0.5rem 0;
        border-top: 2px solid #d1d5db;  /* linha no topo do rodapé */
        z-index: 1000;
    ">
        <p>© 2025 PrevIA - Universidade Federal do Tocantins</p>
        <p>Versão 0.3.1 - Brasília/DF</p>
    </div>
""", unsafe_allow_html=True)