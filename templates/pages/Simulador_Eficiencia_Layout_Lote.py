import streamlit as st
from PIL import Image
import pandas as pd
import lightgbm as lgb
import pickle
import os
import base64
from pathlib import Path



import numpy as np

# Caminho da logo (ajuste se necessário)
logo_path = Path("templates/logo_branca_laranja.png")

# Função para converter imagem em base64
def get_base64_image(path: Path):
    if not path.exists():
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

logo_b64 = get_base64_image(logo_path)

# Configuração da página
st.set_page_config(
    page_title="PrevIA - Predição de Evasão",
    page_icon="images/previa_azulmenor.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ocultar barra streamlit
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

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
    color: #FFFFFF !important;
    font-weight: 600;
    font-size: 1.1rem;
    cursor: pointer;
    text-decoration: none !important;
}}
.nav-link:hover {{
    color: #FFA500 !important; /* laranja claro ao passar o mouse */
    transition: color 0.2s;
}}

/* Espaço no topo para não sobrepor o conteúdo */
.app-content {{
    padding-top: 3.5rem; /* >= altura da nav */
}}

/* Garante que os links não sejam estilizados por padrão do navegador */
a, a:visited, a:active {{
    color: #FFFFFF !important;
    text-decoration: none !important;
}}
</style>

<div class="nav-container">
    <div class="nav-logo"></div>
    <div class="nav-links">
        <a class="nav-link" href="/" target="_self">Início</a>
        <a class="nav-link" href="/Simulador_Eficiencia_Layout" target="_self">Simular</a>
        <a class="nav-link" href="/Indicadores_Eficiencia_Layout" target="_self">Indicadores</a>
        <a class="nav-link" href="/Simulador_Eficiencia_Layout_Gestor" target="_self">Módulo Gestor</a>
        <a class="nav-link" href="/Simulador_Eficiencia_Layout_Lote" target="_self">Simular em Lote</a>
        <a class="nav-link" href="/Sobre" target="_self">Sobre</a>
    </div>
</div>

<div class="app-content"></div>
""", unsafe_allow_html=True)

# 🔹 Conteúdo das páginas
if st.session_state.current_page == "home":
    st.markdown('<h1 class="main-header">PrevIA - Predição de Evasão na Rede Federal com Inteligência Artificial</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Sistema inteligente de análise e predição de evasão escolar na RFEPCT</p>', unsafe_allow_html=True)

    st.markdown("---")


# Função para carregar o modelo
@st.cache_resource
def load_model():
    # modelo_lightgbm_220325.pkl
    # modelo_catboost_categorico_campeao.pkl ou modelo_lightgbm_220325.pkl
    model_path = os.path.join(
        "notebooks", "modelo_catboost_categorico_campeao.pkl")  # ../
    with open(model_path, "rb") as file:
        model = pickle.load(file)
    return model
# Carregar o modelo treinado
model = load_model()




# Texto introdutório centralizado e compacto
st.markdown(
    """
    
    <p style='text-align: center; color: #3f3f4f; margin-top: 0px; margin-bottom: 0px; font-size: 16px;'>
        <strong>Funcionalidade de Simulação em Lote</strong><br>
        Utilize a plataforma de inteligência artificial para analisar a probabilidade de evasão 
        de vários estudantes simultaneamente. Ideal para instituições, coordenadores e gestores 
        que precisam avaliar grupos de alunos em cursos técnicos da Rede Federal EPCT. 
        Faça o upload de uma planilha CSV e obtenha previsões individuais para cada estudante 
        de forma rápida e eficiente.
        <br></br>
    </p>
    """,
    unsafe_allow_html=True
)

# Linha divisória final (com espaçamento menor)
st.markdown("<hr style='margin-top: 10px; margin-bottom: 10px;'>", unsafe_allow_html=True)

# Função para categorizar o risco
def categorizar_risco(prob_evasao):
    if prob_evasao < 0.50:
        return "Baixa probabilidade de evasão"
    elif 0.51 <= prob_evasao <= 0.60:
        return "Moderada chance de evasão"
    elif 0.61 <= prob_evasao <= 0.70:
        return "Considerável probabilidade de evasão"
    elif 0.71 <= prob_evasao <= 0.90:
        return "Alta chance de evasão"
    else:
        return "Muito alta chance de evasão"

# Seção de Upload de Arquivo CSV em Lote
st.subheader("⚙️ Carga de Dados em Lote")









def transformar_dados_para_array(df):
    """
    Transforma o DataFrame do CSV para o formato array com estrutura específica
    usando os nomes das colunas do modelo
    """
    dados_transformados = []
    
    for _, row in df.iterrows():
        # Criar array no formato desejado com os nomes das colunas do modelo
        array_transformado = [
            row['cor_raca'],                    # 'Parda' - cat_features[0]
            int(row['idade']),                  # 41 - variável numérica
            row['sexo'],                        # 'Feminino' - cat_features[1]
            row['renda_familiar'],              # '0<RFP<=0,5' - cat_features[2]
            row['modalidade_de_ensino'],        # 'Educação Presencial' - cat_features[3]
            row['tipo_de_oferta'],              # 'Integrado' - cat_features[4]
            row['turno'],                       # 'Vespertino' - cat_features[5]
            row['nome_de_curso'],               # 'Técnico em Informática' - cat_features[6]
            row['eixo_tecnologico_escolhido'],  # 'Informação e Comunicação' - cat_features[7]
            int(row['carga_horaria_minima']),   # 1000 - variável numérica
            row['estado_escolhido'],            # 'PI' - cat_features[8] (uf)
            row['regiao_escolhida'],            # 'Nordeste' - cat_features[9] (regiao)
            row['instituicao_escolhida'],       # 'Colégio Técnico...' - cat_features[10] (instituicao)
            row['regiao_metropolitana_ue']      # 'NÃO' - cat_features[11] (região_metropolina_ue)
        ]
        
        dados_transformados.append(array_transformado)
    
    return np.array(dados_transformados, dtype=object)

def processar_csv_para_modelo(uploaded_file):
    """
    Processa o CSV carregado e transforma para o formato do modelo
    com os nomes de colunas corretos - SEM converter categóricas
    """
    try:
        # Ler CSV
        df = pd.read_csv(uploaded_file)
        
        # Criar DataFrame com os nomes de colunas EXATOS do modelo
        df_para_modelo = pd.DataFrame({
            'cor_raca': df['cor_raca'],
            'idade': pd.to_numeric(df['idade'], errors='coerce').fillna(0).astype(int),
            'sexo': df['sexo'],
            'renda_familiar': df['renda_familiar'],
            'modalidade_de_ensino': df['modalidade_de_ensino'],
            'tipo_de_oferta': df['tipo_de_oferta'],
            'turno': df['turno'],
            'nome_de_curso': df['nome_de_curso'],
            'eixo_tecnologico': df['eixo_tecnologico_escolhido'],
            'carga_horaria_minima': pd.to_numeric(df['carga_horaria_minima'], errors='coerce').fillna(0).astype(int),
            'uf': df['estado_escolhido'],
            'regiao': df['regiao_escolhida'],
            'instituicao': df['instituicao_escolhida'],
            'região_metropolina_ue': df['regiao_metropolitana_ue']
        })
        
        return df_para_modelo
        
    except Exception as e:
        st.error(f"Erro ao processar CSV: {e}")
        return None

    


st.markdown(
    """
    <style>
    p a.download-link-custom {
        color: #007bff !important;
        text-decoration: none !important;
        font-weight: 500 !important;
    }
    p a.download-link-custom:hover {
        color: #0056b3 !important;
        text-decoration: underline !important;
    }
    </style>

    <p style='color: #3f3f4f; margin-bottom: 15px;'>
        Faça a carga de dados em lote utilizando o dicionário de dados disponível neste 
        <a href='https://drive.google.com/file/d/1hqpTKiU_bG-UJRjiLel-A0PWWFrDLCeo/view?usp=sharing' 
        target='_blank' 
        class='download-link-custom'>
        link para download do template CSV
        </a>.
        O arquivo deve conter os campos que fazem parte do formulário desta página.
    </p>
    """,
    unsafe_allow_html=True
)




# Upload do arquivo CSV
uploaded_file = st.file_uploader(
    "Faça upload do arquivo CSV:",
    type=['csv'],
    help="Selecione um arquivo CSV com os dados para predição em lote."
)

# Processar o arquivo carregado
# No seu código Streamlit, CORRIJA esta parte:
if uploaded_file is not None:
    try:
        # 🔹 CORREÇÃO: Agora a função retorna apenas um valor
        df_para_modelo = processar_csv_para_modelo(uploaded_file)
        
        if df_para_modelo is not None:
            st.subheader("📋 Dados Transformados para o Modelo")
            st.write(f"Total de registros: {len(df_para_modelo)}")
            st.write("**Colunas do modelo:**")
            st.write(list(df_para_modelo.columns))
            st.dataframe(df_para_modelo)
            
            # Verificação dos tipos de dados
            st.subheader("🔍 Verificação dos Tipos de Dados")
            st.write(df_para_modelo.dtypes)
            
            # 🔹 CORREÇÃO: Remover a parte do array que não é mais necessária
            # Já que estamos usando o DataFrame diretamente com CatBoost
            
            # Botão para processar a predição em lote
            if st.button("Prever Evasão em Lote", type="primary"):
                placeholder_mensagem = st.empty()
                placeholder_mensagem.success("🔄 Processando previsão em lote...")
                
                try:
                    # 🔹 CATBOOST: Passar o DataFrame diretamente
                    placeholder_mensagem.info("🎯 Realizando predições com CatBoost...")
                    
                    probabilidades = model.predict_proba(df_para_modelo)
                    
                    # 🔹 DEBUG: Verificar a forma das probabilidades
                    st.write(f"📊 Forma das probabilidades: {probabilidades.shape}")
                    
                    # Processar probabilidades
                    if len(probabilidades.shape) == 2 and probabilidades.shape[1] == 2:
                        probabilidades_evasao = probabilidades[:, 1]  # Classe 1 (evasão)
                    else:
                        probabilidades_evasao = probabilidades
                    
                    # Adicionar colunas de resultados
                    df_resultado = df_para_modelo.copy()
                    df_resultado['Chance de Não Evadir'] = [f"{(1 - prob):.2%}" for prob in probabilidades_evasao]
                    df_resultado['Chance de Evadir'] = [f"{prob:.2%}" for prob in probabilidades_evasao]
                    df_resultado['Categoria de Risco'] = [categorizar_risco(prob) for prob in probabilidades_evasao]
                    
                    placeholder_mensagem.empty()
                    
                    # Exibir resultados
                    st.subheader("📈 Resultados da Predição em Lote")
                    st.dataframe(df_resultado)
                    
                    # Botão para download
                    csv_resultado = df_resultado.to_csv(index=False)
                    st.download_button(
                        label="📥 Download dos Resultados em CSV",
                        data=csv_resultado,
                        file_name="resultados_predicao_evasao.csv",
                        mime="text/csv"
                    )
                    
                    # Estatísticas
                    st.subheader("📊 Estatísticas das Predições")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        alta_evasao = sum(prob > 0.7 for prob in probabilidades_evasao)
                        st.metric("Alto Risco de Evasão", alta_evasao)
                    
                    with col2:
                        moderada_evasao = sum(0.5 <= prob <= 0.7 for prob in probabilidades_evasao)
                        st.metric("Risco Moderado", moderada_evasao)
                    
                    with col3:
                        baixa_evasao = sum(prob < 0.5 for prob in probabilidades_evasao)
                        st.metric("Baixo Risco", baixa_evasao)
                        
                except Exception as e:
                    placeholder_mensagem.empty()
                    st.error(f"❌ Erro ao processar as predições: {str(e)}")
                    
    except Exception as e:
        st.error(f"❌ Erro ao ler o arquivo CSV: {str(e)}")
        st.info("💡 Verifique se o arquivo está no formato correto e contém todas as colunas necessárias.")
# Linha divisória antes do formulário individual
st.markdown("---")


# # Criando o DataFrame de entrada
# input_data = pd.DataFrame({
#     "cor_raca": ["AmarelaBranca" if cor_raca in ["Amarela", "Branca"] else cor_raca],
#     "idade": [int(idade)],
#     "sexo": (sexo),
#     "renda_familiar": (renda_familiar),
#     "modalidade_de_ensino": (modalidade_de_ensino),
#     "tipo_de_oferta": (tipo_de_oferta),
#     "turno": (turno),
#     "nome_de_curso": (nome_de_curso),
#     "eixo_tecnologico": (eixo_tecnologico_escolhido),
#     "carga_horaria_minima": [int(carga_horaria_minima)],
#     "uf": (estado_escolhido),
#     "regiao": (regiao_escolhida),
#     "instituicao": (instituicao_escolhida),
#     "região_metropolina_ue": (região_metropolina_ue)
# })

                