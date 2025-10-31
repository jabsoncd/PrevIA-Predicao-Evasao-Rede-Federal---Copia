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