import streamlit as st
from PIL import Image
import pandas as pd
import lightgbm as lgb
import pickle
import os
import base64

from pathlib import Path

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
    text-decoration: none;
}}
.nav-link:hover {{
    color: #FFA500; /* laranja claro ao passar o mouse */
    transition: color 0.2s;
}}

/* Espaço no topo para não sobrepor o conteúdo */
.app-content {{
    padding-top: 3.5rem; /* >= altura da nav */
}}
</style>

<div class="nav-container">
    <div class="nav-logo"></div>
    <div class="nav-links">
        <span class="nav-link" onclick="window.location.href='#home';">Início</span>
        <span class="nav-link" onclick="window.location.href='#simular';">Simular</span>
        <span class="nav-link" onclick="window.location.href='#indicadores';">Indicadores</span>
        <span class="nav-link" onclick="window.location.href='#gestor';">Módulo Gestor</span>
        <span class="nav-link" onclick="window.location.href='#sobre';">Sobre</span>
    </div>
</div>

<div class="app-content"></div>
""", unsafe_allow_html=True)











# 🔹 Conteúdo das páginas
if st.session_state.current_page == "home":
    st.markdown('<h1 class="main-header">PrevIA - Predição de Evasão na Rede Federal com Inteligência Artificial</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Sistema inteligente de análise e predição de evasão escolar na RFEPCT</p>', unsafe_allow_html=True)

    st.markdown("---")





##########################################################################################################################################################
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
# Título do painel
# st.image("images/previa_gemini.png", width=200)
# Título do painel com imagem centralizada
# https://raw.githubusercontent.com/jabsoncd/PrevIA-Predicao-Evasao-Rede-Federal---Copia/main/images/previa_gemini.png
# st.markdown(
#     """
#     <div style='text-align: center;'>
#         <img src='https://github.com/jabsoncd/PrevIA-Predicao-Evasao-Rede-Federal---Copia/blob/main/images/previa_gemini.png' width='280'/>
#     </div>
#     """,
#     unsafe_allow_html=True
# )
# st.markdown("<h2 style='text-align: center; color: #12125c; margin-bottom: 5px;'>Inteligência Artificial para Predição da Evasão na Rede Federal EPCT</h2>", unsafe_allow_html=True)
# st.markdown("<p style='text-align: center; color: #1e1e8f;'>Plataforma para análise do comportamento da evasão na RFEPCT.</p>", unsafe_allow_html=True)
# <hr style='margin-top: 10px; margin-bottom: 10px;' />
# st.markdown("---")
# # 🔹 Texto introdutório centralizado
# st.markdown("<p style='text-align: center; color: #3f3f4f; margin-top: 0px;'>Olá! Faça agora a sua simulação e descubra a probabilidade de evasão em um curso técnico da Rede Federal EPCT. Nossa plataforma utiliza um modelo avançado de aprendizado de máquina treinado com dados históricos de matrículas de estudantes para analisar padrões e prever a chance de permanência ou evasão no curso. Essa ferramenta pode ajudá-lo a tomar decisões mais informadas, seja para o seu próprio percurso acadêmico ou para apoiar alguém que está considerando ingressar em um curso técnico. Experimente e veja as possibilidades! </p>", unsafe_allow_html=True)
# # Linha divisória
# st.write("---")
# Título e subtítulo com margens ajustadas
# st.markdown(
#     """
#     <h2 style='text-align: center; color: #12125c; margin-bottom: 5px;'>
#         Inteligência Artificial para Predição da Evasão na Rede Federal EPCT
#     </h2>
#     <p style='text-align: center; color: #1e1e8f; margin-top: 0px; margin-bottom: 10px;'>
#         Plataforma para análise do comportamento da evasão na RFEPCT.
#     </p>
#     <hr style='margin-top: 10px; margin-bottom: 10px;' />
#     """,
#     unsafe_allow_html=True
# )
# Texto introdutório centralizado e compacto
st.markdown(
    """
    <p style='text-align: center; color: #3f3f4f; margin-top: 0px; margin-bottom: 0px; font-size: 16px;'>
        Olá! Faça agora a sua simulação e descubra a probabilidade de evasão em um curso técnico da Rede Federal EPCT.
        Nossa plataforma utiliza um modelo avançado de aprendizado de máquina treinado com dados históricos de matrículas de estudantes
        para analisar padrões e prever a chance de permanência ou evasão no curso.
        Essa ferramenta pode ajudá-lo a tomar decisões mais informadas, seja para o seu próprio percurso acadêmico
        ou para apoiar alguém que está considerando ingressar em um curso técnico. Experimente e veja as possibilidades!
    </p>
    """,
    unsafe_allow_html=True
)

# Linha divisória final (com espaçamento menor)
st.markdown("<hr style='margin-top: 10px; margin-bottom: 10px;'>", unsafe_allow_html=True)

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
            border-radius: 5px;
            text-decoration: none;
            font-size: 16px;
            font-weight: bold;
            border: none;
            display: inline-block;
            text-align: center;
            cursor: pointer;
        }
        .botao-voltar:hover {
            background-color: #003366; /* Azul mais escuro no hover */
        }
    </style>
    <a class="botao-voltar" href="https://previa-beta.streamlit.app/~/+/" target="_self">Voltar para Home</a> 
    """,
    unsafe_allow_html=True
)

 
st.write(" ")
st.write(" ")
st.write(" ")


st.header("Simulador de Evasão em Cursos Técnicos")

st.subheader("Dados da Instituição")

# Dicionário com regiões, UFs e instituições federais
regioes = {
    "Norte": {
        "AC": ["Instituto Federal do Acre"],
        "AM": ["Instituto Federal do Amazonas", ],
        "AP": ["Instituto Federal do Amapá"],
        "PA": ["Instituto Federal do Pará", "Escola de Música da UFPA", "ETDUFPA"],
        "RO": ["Instituto Federal de Rondônia"],
        "RR": ["Instituto Federal de Roraima", "Escola Agrotécnica da UFRR"],
        "TO": ["Instituto Federal do Tocantins"]
    },
    "Nordeste": {
        "AL": ["Instituto Federal de Alagoas", "Escola Técnica de Artes da UFAL"],
        "BA": ["Instituto Federal da Bahia", "Instituto Federal Baiano"],
        "CE": ["Instituto Federal do Ceará"],
        "MA": ["Instituto Federal do Maranhão", "Colégio Universitário da UFMA"],
        "PB": ["Instituto Federal da Paraíba", "Escola Técnica de Saúde de Cajazeiras da UFCG", "Colégio Agrícola Vidal de Negreiros da UFPB", "UFPB-ESTES"],
        "PE": ["Instituto Federal de Pernambuco", "Instituto Federal do Sertão Pernambucano", "Colégio Agrícola Dom Agostinho Ikas da UFRPE"],
        "PI": ["Instituto Federal do Piauí", "Colégio Técnico de Teresina da UFPI", "Colégio Técnico de Bom Jesus da UFPI", "Colégio Técnico de Floriano da UFPI"],
        "RN": ["Instituto Federal do Rio Grande do Norte", "Escola de Saúde da UFRN", "Escola Agrícola de Jundiaí da UFRN", "Escola de Música da UFRN"],
        "SE": ["Instituto Federal de Sergipe"]
    },
    "Centro-Oeste": {
        "DF": ["Instituto Federal de Brasília"],
        "GO": ["Instituto Federal de Goiás", "Instituto Federal Goiano"],
        "MS": ["Instituto Federal do Mato Grosso do Sul"],
        "MT": ["Instituto Federal do Mato Grosso"]
    },
    "Sudeste": {
        "ES": ["Instituto Federal do Espírito Santo"],
        "MG": ["Instituto Federal de Minas Gerais", "Instituto Federal do Triângulo Mineiro", "Instituto Federal do Norte de Minas Gerais", "Instituto Federal do Sul de Minas Gerais", "Instituto Federal do Sudeste de Minas Gerais", "Centro Federal de Educação Tecnológica de Minas Gerais", "Colégio Técnico da UFMG", "Teatro Universitário da UFMG", "Escola Técnica de Saúde da UFU", "Centro de Ensino e Desenvolvimento Agrário da UFV", "UFTM-CEFORES"],
        "RJ": ["Instituto Federal do Rio de Janeiro", "Instituto Federal Fluminense", "Centro Federal de Educação Tecnológica Celso Suckow da Fonseca", "Colégio Pedro II", "Colégio Técnico da UFRRJ"],
        "SP": ["Instituto Federal de São Paulo"]
    },
    "Sul": {
        "PR": ["Instituto Federal do Paraná"],
        "SC": ["Instituto Federal de Santa Catarina", "Instituto Federal Catarinense"],
        "RS": ["Instituto Federal do Rio Grande do Sul", "Instituto Federal Sul-rio-grandense", "Instituto Federal Farroupilha", "Colégio Técnico Industrial da UFSM", "Colégio Politécnico da UFSM"]
    }
}

regiao_escolhida = st.selectbox("Região", ["Selecione uma região"] + list(
    regioes.keys()), help="Selecione a Região que estuda ou deseja estudar.")

# Se o usuário não escolher uma região válida, exibir mensagem de erro
if regiao_escolhida == "Selecione uma região":
    st.markdown(
        """
    <div style="
        border-radius: 5px; 
        color: red; 
        background-color: white;
        display: inline-block;">
        *selecione selecione primeiro uma Região.
        <p>
    </div>
    """,
        unsafe_allow_html=True
    )


# Se uma região for escolhida, listar os estados (UFs) dessa região
if regiao_escolhida != "Selecione uma região":
    estado_opcoes = ["Selecione um Estado"] + \
        list(regioes[regiao_escolhida].keys())
else:
    estado_opcoes = ["Selecione um Estado"]

estado_escolhido = st.selectbox("Estado:", estado_opcoes,
                                index=0,
                                help="Selecione o Estado que estuda ou deseja estudar.")

# Se uma UF for escolhida, listar as instituições dessa UF
if estado_escolhido != "Selecione um Estado":
    instituicao_opcoes = ["Selecione uma Instituição"] + \
        regioes[regiao_escolhida][estado_escolhido]
else:
    instituicao_opcoes = ["Selecione uma Instituição"]

instituicao_escolhida = st.selectbox("Instituição:", instituicao_opcoes,
                                     index=0,
                                     help="Selecione a Instituição que estuda ou deseja estudar.")

região_metropolina_ue = st.radio("A unidade de ensino está localizada em região metropolitana?", [
    "SIM", "NÃO"], help="Informe essa a Instituição que estuda ou deseja estudar fica em região metropolitana da cidade.")

# Dados Pessoais
st.subheader("Dados Pessoais")
sexo = st.selectbox("Informe seu Gênero:", [
    "Masculino", "Feminino"], placeholder="Escolha uma opção.")
idade = st.slider("Informe sua Idade:", min_value=14,
                  max_value=100, value=14, step=1)
cor_raca = st.selectbox("Informe sua Cor/Raça:", ["Branca", "Preta", "Parda", "Amarela",
                                                  "Indígena", "Não declarada"], placeholder="Escolha uma opção.", help="Informe sua cor/raça")
renda_familiar = st.selectbox("Informe sua Renda Familiar Per capita:", [
                              "0<RFP<=0,5", "0,5<RFP<=1", "1<RFP<=1,5", "1,5<RFP<=2,5", "2,5<RFP<=3,5", "RFP>3,5", "Não declarada"], placeholder="Escolha uma opção.", help="Informe a renda familiar por pessoa.")

# Dados do Curso
st.subheader("Dados do Curso")


# # Definição de eixos tecnologicos
mapeamento_eixos = {
    "Ambiente e Saúde": "Ambiente e Saúde",
    "Controle e Processos Industriais": "Controle e Processos Industriais",
    "Desenvolvimento Educacional e Social": "Desenvolvimento Educacional e Social",
    "Gestão e Negócios": "Gestão e Negócios",
    "Informação e Comunicação": "Informação e Comunicação",
    "Infraestrutura": "Infraestrutura",
    "Produção Alimentícia": "Produção Alimentícia",
    "Produção Cultural e Design": "Produção Cultural e Design",
    "Produção Industrial": "Produção Industrial",
    "Recursos Naturais": "Recursos Naturais",
    "Segurança": "Segurança",
    "Militar": "Militar",
    "Turismo, Hospitalidade e Lazer": "Turismo, Hospitalidade e Lazer"
}

# Carregar os dados


def carregar_dados():
    # '../artifacts/cnct2025.xlsx' ou cnct2025_base_eficiencia.xlsx
    file_path = 'artifacts/cnct2025v1.xlsx'
    df = pd.read_excel(file_path, sheet_name="Plan1", engine="openpyxl")
    return df


df = carregar_dados()


# Aplicar o mapeamento no DataFrame
df["Eixo_Tecnologico_Mapeado"] = df["eixo_tecnologico"].map(mapeamento_eixos)

# Obter Eixos Tecnológicos únicos (mapeados)
eixos_mapeados = sorted(df["Eixo_Tecnologico_Mapeado"].dropna().unique())

# Selecionar Eixo Tecnológico (com opção fixa "Selecione um Eixo Tecnológico")
eixo_opcoes = ["Selecione um Eixo Tecnológico"] + eixos_mapeados
eixo_tecnologico_escolhido = st.selectbox(
    "Informe o Eixo Tecnológico:",
    eixo_opcoes,
    index=0,  # Mantém "Selecione um Eixo Tecnológico" como padrão
    help="Selecione o Eixo Tecnológico do Curso Técnico que estuda ou deseja cursar."
)


# Se o usuário não escolher um eixo válido, exibir mensagem de erro
if eixo_tecnologico_escolhido == "Selecione um Eixo Tecnológico":
    st.markdown(
        """
    <div style="
        border-radius: 5px; 
        color: red; 
        background-color: white;
        display: inline-block;">
        *selecione primeiro um Eixo Tecnológico.
        <p>
    </div>
    """,
        unsafe_allow_html=True
    )

# Inicializa lista de cursos
cursos = ["Selecione um Curso Técnico"]

# Filtrar cursos apenas se um eixo válido for escolhido
if eixo_tecnologico_escolhido != "Selecione um Eixo Tecnológico":
    df_filtrado = df[df["Eixo_Tecnologico_Mapeado"]
                     == eixo_tecnologico_escolhido]
    cursos += sorted(df_filtrado["nome_de_curso"].unique())

# Selecionar Curso Técnico (com opção fixa "Selecione um Curso Técnico")
nome_de_curso = st.selectbox(
    "Nome do curso técnico:",
    cursos,
    index=0,  # Mantém "Selecione um Curso Técnico" como padrão
    help="Selecione o Curso Técnico que estuda ou deseja cursar."
)

# Inicializa a carga horária mínima
carga_horaria_minima = 0

# Exibir carga horária apenas se um curso válido for selecionado
if nome_de_curso != "Selecione um Curso Técnico":
    carga_horaria_minima = df_filtrado[df_filtrado["nome_de_curso"]
                                       == nome_de_curso]["carga_horaria_minima"].values[0]

# Exibir carga horária mínima (desabilitado)
st.text_input("Carga Horária", carga_horaria_minima, disabled=True,
              help="A Carga horária do Curso técnico é baseada na carga mínima do CNCT.")

modalidade_de_ensino = st.selectbox("Modalidade de ensino:", [
    "Educação a Distância", "Educação Presencial"], placeholder="Escolha uma opção.", help="Informe se o curso técnico de que estuda ou deseja cursar é Presencial ao EaD.")
tipo_de_oferta = st.selectbox("Tipo de oferta:", ["Concomitante", "Integrado", "Subsequente", "PROEJA - Concomitante", "PROEJA - Integrado", "PROEJA - Subsequente"], placeholder="Escolha uma opção.",
                              help="Informe se o curso técnico de que estuda ou deseja cursar é Subsequente ao ensino médio, será cursado junto com o Ensino médio ou Integrado ao ensino médio.")
turno = st.selectbox("Turno do curso:", ["Integral", "Matutino", "Vespertino", "Noturno", "Não se aplica"], placeholder="Escolha uma opção.",
                     help="Informe se o curso técnico de que estuda ou deseja cursar é/será realizado no turno Matutino, Vespertino, Noturno ou Integrado.")


# Botão para submeter
submit = st.button("🔎 Prever Evasão")

# **Validação Completa Antes de Processar**
if submit:
    erros = []

    if regiao_escolhida == "Selecione uma região":
        erros.append("⚠️ Por favor, selecione uma **Região**.")
    if estado_escolhido == "Selecione um Estado":
        erros.append("⚠️ Por favor, selecione um **Estado**.")
    if instituicao_escolhida == "Selecione uma Instituição":
        erros.append("⚠️ Por favor, selecione uma **Instituição**.")
    if eixo_tecnologico_escolhido == "Selecione um Eixo Tecnológico":
        erros.append("⚠️ Por favor, selecione um **Eixo Tecnológico**.")
    if nome_de_curso == "Selecione um Curso Técnico":
        erros.append("⚠️ Por favor, selecione um **Curso Técnico**.")
    if carga_horaria_minima == 0:
        erros.append(
            "⚠️ A **Carga Horária** deve ser maior que 0. Por favor, selecione um valor válido.")
    if modalidade_de_ensino == "Selecione":
        erros.append("⚠️ Por favor, selecione a **Modalidade de Ensino**.")
    if tipo_de_oferta == "Selecione":
        erros.append("⚠️ Por favor, selecione o **Tipo de Oferta**.")
    if turno == "Selecione":
        erros.append("⚠️ Por favor, selecione o **Turno do Curso**.")

    if erros:
        for erro in erros:
            st.error(erro)
    else:
        # # Se não houver erros, realiza o processamento dos dados
        # Criando o DataFrame de entrada
        input_data = pd.DataFrame({
            "cor_raca": ["AmarelaBranca" if cor_raca in ["Amarela", "Branca"] else cor_raca],
            "idade": [int(idade)],
            "sexo": (sexo),
            "renda_familiar": (renda_familiar),
            "modalidade_de_ensino": (modalidade_de_ensino),
            "tipo_de_oferta": (tipo_de_oferta),
            "turno": (turno),
            "nome_de_curso": (nome_de_curso),
            "eixo_tecnologico": (eixo_tecnologico_escolhido),
            "carga_horaria_minima": [int(carga_horaria_minima)],
            "uf": (estado_escolhido),
            "regiao": (regiao_escolhida),
            "instituicao": (instituicao_escolhida),
            "região_metropolina_ue": (região_metropolina_ue)
        })
        # # Criando o DataFrame de entrada

        st.subheader("📋 Simulações Realizadas")
        if "input_data" in st.session_state:
            st.session_state.input_data = pd.concat(
                [st.session_state.input_data, input_data], ignore_index=True)
        else:
            st.session_state.input_data = input_data

        st.write(st.session_state.input_data)

        # Exibe as colunas do modelo e as colunas do input_data
        print("Colunas do modelo:", model.feature_names_)
        print("Colunas do input_data:", input_data.columns.tolist())

        # Botão para limpar as simulações
        if st.button("Limpar Simulações"):
            # Limpa os dados de 'input_data' no session_state
            st.session_state.input_data = pd.DataFrame()  # Reseta para um DataFrame vazio
            st.write("Simulações limpas com sucesso!")

        # Código para realizar a previsão aqui, se não houver erros
        # st.success("Processando a previsão de evasão...")

        # --- Mensagem temporária ---
        placeholder_mensagem = st.empty()  # Cria um placeholder vazio
        placeholder_mensagem.success("Processando a previsão de evasão...")  # Exibe a mensagem

        # Predição
        probabilidades = model.predict_proba(input_data)[0]
        prob_nao_evasao = probabilidades[0]  # Probabilidade de NÃO EVADIR
        prob_evasao = probabilidades[1]  # Probabilidade de EVADIR

        import plotly.graph_objects as go
        import time

        valor_final = round(prob_evasao * 100, 2)
        # Criar espaço para o gráfico
        chart_placeholder = st.empty()

        # Animação do ponteiro do velocímetro
        for valor_final in range(0, int(round(valor_final * 1, 2,)) + 1, 1):  # Atualiza a cada 5%
            # Convertendo para float com 2 casas decimais
            valor_final_float = valor_final
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=valor_final_float,
                number={'valueformat': '.f', 'suffix': "%",
                        'font': {'size': 45, 'color': '#2C3E50'}},
                title={'text': "Probabilidade de Evasão (%)", 'font': {
                    'size': 20, 'color': '#2C3E50'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': "#7f8c8d"},
                    'bar': {'color': "#2C3E50"},  # Cor do ponteiro
                    'steps': [
                        # Verde moderno
                        {'range': [0, 40], 'color': "#27AE60"},
                        # Amarelo vibrante
                        {'range': [40, 70], 'color': "#F1C40F"},
                        # Vermelho marcante
                        {'range': [70, 100], 'color': "#E74C3C"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.85,
                        'value': valor_final_float
                    }
                }
            ))

            # Layout moderno
            fig.update_layout(
                margin=dict(l=20, r=40, t=10, b=20),
                paper_bgcolor="#f2f4f5",
                font=dict(color="#2c3e50", family="Arial")
            )

            # Atualiza o gráfico na tela
            chart_placeholder.plotly_chart(fig)

            # Pausa para criar o efeito de transição
            time.sleep(0.1)  # Ajuste esse tempo para controlar a velocidade

        # --- Remover a mensagem inicial após a animação ---
        placeholder_mensagem.empty()  # Faz a mensagem desaparecer

        # Definir categorias de risco com base na probabilidade de evasão
        if prob_evasao < 0.50:
            st.success(
                f"✅ Baixa probabilidade de evasão. (Não evade: {prob_nao_evasao:.2%})")
            imagem = Image.open("templates/n_evade.jpg")
            legenda = "Estudante aliviado por não evadir"

        elif 0.51 <= prob_evasao <= 0.60:
            st.warning(
                f"⚠️ Moderada chance de evasão. (Evade: {prob_evasao:.2%})")
            # Trocar por outra imagem
            imagem = Image.open("templates/moderada1.jpg")
            legenda = "Estudante com dúvidas sobre continuar o curso"

        elif 0.61 <= prob_evasao <= 0.70:
            st.warning(
                f"⚠️ Considerável probabilidade de evasão. (Evade: {prob_evasao:.2%})")
            imagem = Image.open("templates/evade1.jpg")
            legenda = "Estudante em risco moderado de evasão"

        elif 0.71 <= prob_evasao <= 0.90:
            st.error(f"⚠️ Alta chance de evasão! (Evade: {prob_evasao:.2%})")
            imagem = Image.open("templates/alta.jpg")
            legenda = "Estudante preocupado com a evasão"

        else:  # 0.91 a 1.00
            st.error(
                f"🚨 Muito alta chance de evasão! (Evade: {prob_evasao:.2%})")
            imagem = Image.open("templates/evade.jpg")
            legenda = "Estudante com grande risco de abandonar o curso"

        # Exibir os resultados
        st.subheader("📊 Resultados da Predição")
        st.write(f"🔵 Probabilidade de **NÃO EVADIR**: {prob_nao_evasao:.2%}")
        st.write(f"🔴 Probabilidade de **EVADIR**: {prob_evasao:.2%}")
        
        # Exibir a imagem correspondente
        st.image(imagem, caption=legenda, width=450)  # use_container_width=True


        # Exibir a imagem correspondente (centralizada e com largura 450px)
        col1, col2, col3 = st.columns([1, 1, 1])  # colunas: esquerda, centro, direita
        with col2:
            st.image(imagem, caption=legenda, width=450)

        # Centralizar e redimensionar a imagem (400px)
        st.markdown(
            f"""
            <div style='display: flex; justify-content: center;'>
                <img src='{imagem}' alt='{legenda}'>
            </div>
            
            <p style='text-align:center; font-style: italic;'>{legenda}</p>
            """,
            unsafe_allow_html=True
        )       










##########################################################################################################################################################




elif st.session_state.current_page == "simular":
    st.title("Simulador de Evasão")
    st.write("Conteúdo do simulador será implementado aqui...")

elif st.session_state.current_page == "indicadores":
    st.title("Indicadores de Evasão")
    st.write("Conteúdo dos indicadores será implementado aqui...")

elif st.session_state.current_page == "gestor":
    st.title("Módulo Gestor")
    st.write("Conteúdo do módulo gestor será implementado aqui...")

elif st.session_state.current_page == "sobre":
    st.title("Sobre o PrevIA")
    st.write("Informações sobre o projeto...")
























# # Função para converter imagem local em Base64
# def get_base64_of_image(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode()

# # Converter a imagem local
# img_base64 = get_base64_of_image("templates/simulador.jpg")
# st.set_page_config(
#     page_title="Plataforma PrevIA",
#     page_icon="images/previa_azulmenor.png",
#     initial_sidebar_state="collapsed"
# )
# # Ocultar barra streamlit
# hide_st_style = """
#     <style>:
#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
#     header {visibility: hidden;}
#     </style>
#     """  
# st.markdown(hide_st_style, unsafe_allow_html=True)
# # 🔹 CSS para definir a imagem de fundo
# st.markdown(
#     f"""
#     <style>
#     .stApp {{
#         background-image: url("data:image/jpg;base64,{img_base64}");
#         background-size: cover;  # Cobrir toda a tela sem repetição
#         background-repeat: no-repeat;
#         background-position: center center;
#         background-attachment: fixed;
#     }}
#     </style>
#     """,
#     unsafe_allow_html=True
# )



# st.markdown("<hr style='border: 1px solid black;'>", unsafe_allow_html=True)
# st.markdown("<p style='color: black;'>Versão 0.0.1 - Brasília - 2025. Universidade Federal do Tocantins - UFT.</p>", unsafe_allow_html=True)
