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
    initial_sidebar_state="expanded"  # Sidebar expandida por padrão
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

# CSS personalizado
st.markdown("""
    <style>
    /* Esconder o termo "Home Profissional" */
    .css-1d391kg, 
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# CSS personalizado - ADICIONE ESTE BLOCO PARA REMOVER O ÍCONE DA SIDEBAR
st.markdown("""
    <style>
    /* REMOVER COMPLETAMENTE o ícone de recolher/expandir sidebar */
    button[data-testid="stBaseButton-headerNoPadding"],
    [data-testid="stIconMaterial"],
    [data-testid="stSidebarCollapseButton"],
    .css-1d391kg {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
        width: 0 !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
    <style>
    [data-testid="stHelpIcon"] svg {
        fill: white !important;  /* muda a cor do ícone */
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Manter visível mas desabilitar interação */
    button[data-testid="baseButton-header"] {
        pointer-events: none !important;
        cursor: not-allowed !important;
    }
    </style>
""", unsafe_allow_html=True)
######################################################################## BARRA AZUL #################################################################################
st.markdown(""" 
<style>
/* 🔹 Barra superior azul */
.nav-container {
    background-color: #152847;
    height: 2cm;
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    padding: 0 2rem;
    margin: 0;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 999;
    border-radius: 0;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2)
}

.nav-logo {
    width: 200px;
    height: 60px;
    background-size: contain;
    background-repeat: no-repeat;
    background-position: left center;
}

.nav-links {
    display: flex;
    gap: 2rem;
}

.nav-link {
    color: #FFFFFF !important;
    font-weight: 600;
    font-size: 1.1rem;
    cursor: pointer;
    text-decoration: none !important;
}
.nav-link:hover {
    color: #FFA500 !important
    transition: color 0.2s;
}

/* Espaço no topo para não sobrepor o conteúdo */
.app-content {
    padding-top: 3.5rem;
}

/* Centralizar conteúdo */
.centered-content {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    text-align: center;
}
            
* Garante que os links não sejam estilizados por padrão do navegador */
a, a:visited, a:active {
    color: #FFFFFF !important;
    text-decoration: none !important;
}

/* Estilo para a sidebar */
.sidebar-content {
    padding: 1rem;
}
        

/* Estilo para os resultados */
.result-section {
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 1.5rem;
    margin: 1rem 0;
    border-left: 4px solid #3b82f6;
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
</style>
""", unsafe_allow_html=True)


# 🔹 Mantém sidebar visível e apenas oculta links indesejados
st.markdown("""
    <style>
    /* Oculta links específicos */
    section[data-testid="stSidebar"] a[href*="Home_Profissional"],
    section[data-testid="stSidebar"] a[href*="Indicadores_Eficiencia"],
    section[data-testid="stSidebar"] a[href*="Simulador_Eficiencia"],
    section[data-testid="stSidebar"] a[href*="Sobre"],
    section[data-testid="stSidebar"] a[href*="Indicadores_Eficiencia_Layout"],
    section[data-testid="stSidebar"] a[href*="Simulador_Eficiencia_Layout"] {
        display: none !important;
    }

    /* Sidebar com transição suave */
    [data-testid="stSidebar"] {
        position: fixed;
        left: 0;
        top: 2cm;
        height: calc(100vh - 2cm);
        min-width: 2rem !important;
        max-width: 26rem !important;
        z-index: 1000;
        box-shadow: 2px 0 12px rgba(0,0,0,0.18);
        background-color: #455f85; d4d4d4 - #455f85
        transform: none !important;
        transition: none !important;
    }
    
    </style>
""", unsafe_allow_html=True)
# Barra de navegação
st.markdown(f"""
<div class="nav-container">
    <div class="nav-logo" style="background-image: url('data:image/jpg;base64,{logo_b64}');"></div>
    <div class="nav-links">
        <a class="nav-link" href="/" target="_self">Início</a>
        <a class="nav-link" href="/Simulador_Eficiencia_Layout" target="_self">Simular</a>
        <a class="nav-link" href="/Indicadores_Eficiencia_Layout" target="_self">Indicadores</a>
        <a class="nav-link" href="/Simulador_Eficiencia_Layout_Gestor" target="_self">Módulo Gestor</a>
        <a class="nav-link" href="/Sobre" target="_self">Sobre</a>
    </div>
</div>
<div class="app-content"></div>
""", unsafe_allow_html=True)

# Estado inicial
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"
if "input_data" not in st.session_state:
    st.session_state.input_data = pd.DataFrame()

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


# Carregar dados
def carregar_dados():
    file_path = 'artifacts/cnct2025v1.xlsx'
    df = pd.read_excel(file_path, sheet_name="Plan1", engine="openpyxl")
    return df

df = carregar_dados()

# =============================================
# CONTEÚDO PRINCIPAL - CENTRALIZADO
# =============================================

# 🔹 Conteúdo das páginas
if st.session_state.current_page == "home":
    st.markdown('<h1 class="main-header">PrevIA - Predição de Evasão na Rede Federal com Inteligência Artificial</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Sistema inteligente de análise e predição de evasão escolar na RFEPCT</p>', unsafe_allow_html=True)
# Linha divisória
st.markdown("<p style='text-align: center; color: #3f3f4f;'> </p>",
            unsafe_allow_html=True)
st.write("---")

# Texto introdutório
st.markdown(
    """
    <p style='text-align: center; color: #3f3f4f; font-size: 16px;'>
        Olá! Faça agora a sua simulação e descubra a probabilidade de evasão em um curso técnico da Rede Federal EPCT.
        Nossa plataforma utiliza um modelo avançado de aprendizado de máquina treinado com dados históricos de matrículas de estudantes
        para analisar padrões e prever a chance de permanência ou evasão no curso.
        Essa ferramenta pode ajudá-lo a tomar decisões mais informadas, seja para o seu próprio percurso acadêmico
        ou para apoiar alguém que está considerando ingressar em um curso técnico. Experimente e veja as possibilidades!
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("<hr style='margin-top: 10px; margin-bottom: 10px;'>", unsafe_allow_html=True)





# Mapeamento de eixos tecnológicos
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

df["Eixo_Tecnologico_Mapeado"] = df["eixo_tecnologico"].map(mapeamento_eixos)

# Dicionário com regiões, UFs e instituições federais
regioes = {
    "Norte": {
        "AC": ["Instituto Federal do Acre"],
        "AM": ["Instituto Federal do Amazonas"],
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

# =============================================
# SIDEBAR - FILTROS
# =============================================

with st.sidebar: 

    # Dados da Instituição
    st.markdown("<h3 style='font-weight: bold; color: #F0F0F0;'>Dados da Instituição</h3>", unsafe_allow_html=True)
    
    
    st.markdown("""
        <style>
        /* Cor do texto do selectbox */
        .stSelectbox label {
            color: #F0F0F0 !important;
            font-weight: 500;
        }
        
        /* Cor do texto das opções no dropdown */
        .stSelectbox div[data-baseweb="select"] {
            color: #F0F0F0 !important;
        }
                
        /* Ícone de help - abordagem direta */
        [data-testid="stTooltipHoverTarget"] svg {
            fill: #F0F0F0 !important;
            stroke: rgb(24, 221, 110); 
        }
        
        /* Hover no ícone */
        [data-testid="stTooltipHoverTarget"]:hover svg {
            stroke: rgb(24, 221, 110); 
        }
        
        /* Tooltip content */
        [data-testid="stTooltip"] {
            color: #E8E8E8 !important;
            background-color: #262730 !important;
            border: 1px solid #666666 !important;
            stroke: rgb(24, 221, 110); 
        }
        
        /* Garantir para todos os tipos de componentes */
        .st-emotion-cache-oj1fi .stTooltipHoverTarget > svg {
            stroke: rgba(50, 62, 55, 0.7);
        }
        </style>
                
      

    """, unsafe_allow_html=True)
    
    regiao_escolhida = st.selectbox("Região", 
                                   ["Selecione uma região"] + list(regioes.keys()),
                                   help="Selecione a Região que estuda ou deseja estudar.")

    if regiao_escolhida != "Selecione uma região":
        estado_opcoes = ["Selecione um Estado"] + list(regioes[regiao_escolhida].keys())
    else:
        estado_opcoes = ["Selecione um Estado"]

    estado_escolhido = st.selectbox("Estado:", estado_opcoes,
                                   help="Selecione o Estado que estuda ou deseja estudar.")

    if estado_escolhido != "Selecione um Estado":
        instituicao_opcoes = ["Selecione uma Instituição"] + regioes[regiao_escolhida][estado_escolhido]
    else:
        instituicao_opcoes = ["Selecione uma Instituição"]

    instituicao_escolhida = st.selectbox("Instituição:", instituicao_opcoes,
                                        help="Selecione a Instituição que estuda ou deseja estudar.")

    st.markdown("""
        <style>
        /* Label da pergunta do radio */
        .stRadio label {
            color: #F0F0F0 !important;
            font-weight: 500;
        }
        
        /* Texto das opções do radio */
        .stRadio div[role="radiogroup"] label {
            color: #E8E8E8 !important;
            font-weight: 400;
        }
        
        /* Opção selecionada */
        .stRadio div[role="radiogroup"] input:checked + label {
            color: #FFFFFF !important;
            font-weight: 500;
        }
        
        /* Hover nas opções */
        .stRadio div[role="radiogroup"] label:hover {
            color: #FFFFFF !important;
        }
        
        /* Selectbox (mantendo seu estilo original) */
        .stSelectbox div[data-baseweb="select"] {
            color: #F0F0F0 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    regiao_metropolitana_ue = st.radio("A unidade de ensino está localizada em região metropolitana?", 
                                  ["SIM", "NÃO"],
                                  help="Informe se a Instituição fica em região metropolitana.")
  
    # Dados Pessoais
    st.markdown("---")
    st.markdown("<h3 style='font-weight: bold;color: #F0F0F0; '>Dados Pessoais</h3>", unsafe_allow_html=True)
    sexo = st.selectbox("Gênero:", 
                                    ["Selecione um Gênero"] + ["Masculino", "Feminino"],
                                    help="Selecione o gênero do estudante")
    
    st.markdown("""
        <style>
        /* Cor do texto do selectbox */
        .stSlider label {
            color: #F0F0F0 !important;
            font-weight: 500;
        }
        
        /* Cor do texto das opções no dropdown */
        .stSelectbox div[data-baseweb="select"] {
            color: #F0F0F0 !important;
        }
        </style>
    """, unsafe_allow_html=True)
    idade = st.slider("Idade:", min_value=14, max_value=100, value=14, step=1)
    cor_raca = st.selectbox("Cor/Raça:", 
                                    ["Selecione uma Cor/Raça"] + ["Branca", "Preta", "Parda", "Amarela", "Indígena", "Não declarada"],
                                    help="Selecione a Cor/Raça")

    renda_familiar = st.selectbox("Renda Familiar Per capita:", 
                                    ["Selecione uma Renda Familiar"] + ["0<RFP<=0,5", "0,5<RFP<=1", "1<RFP<=1,5", "1,5<RFP<=2,5", "2,5<RFP<=3,5", "RFP>3,5", "Não declarada"],
                                    help="Selecione a Renda Familiar")
     # Dados do Curso
    st.markdown("---")
    st.markdown("<h3 style='font-weight: bold; color: #F0F0F0;'>Dados do Curso</h3>", unsafe_allow_html=True)


    
    eixos_mapeados = sorted(df["Eixo_Tecnologico_Mapeado"].dropna().unique())
    eixo_opcoes = ["Selecione um Eixo Tecnológico"] + eixos_mapeados
    eixo_tecnologico_escolhido = st.selectbox(
        "Eixo Tecnológico:",
        eixo_opcoes,
        help="Selecione o Eixo Tecnológico do Curso Técnico."
    )

    # Filtrar cursos baseado no eixo tecnológico
    cursos = ["Selecione um Curso Técnico"]
    carga_horaria_minima = 0

    if eixo_tecnologico_escolhido != "Selecione um Eixo Tecnológico":
        df_filtrado = df[df["Eixo_Tecnologico_Mapeado"] == eixo_tecnologico_escolhido]
        cursos += sorted(df_filtrado["nome_de_curso"].unique())

    nome_de_curso = st.selectbox(
        "Curso Técnico:",
        cursos,
        help="Selecione o Curso Técnico que estuda ou deseja cursar."
    )

    if nome_de_curso != "Selecione um Curso Técnico":
        carga_horaria_minima = df_filtrado[df_filtrado["nome_de_curso"] == nome_de_curso]["carga_horaria_minima"].values[0]


    st.markdown("""
        <style>
        /* Label do text_input */
        .stTextInput label {
            color: #F5F5F5 !important;
            font-weight: bold;
        }
        
        /* Campo de texto desabilitado */
        .stTextInput input:disabled {
            color: #E8E8E8 !important;
            background-color: rgba(255, 255, 255, 0.1);
            border: 1px solid #666666;
            opacity: 0.8;
        }
        
        /* Placeholder se houver */
        .stTextInput input::placeholder {
            color: #BBBBBB !important;
        }
        </style>
    """, unsafe_allow_html=True)
    st.text_input("Carga Horária", carga_horaria_minima, disabled=True,
                 help="Carga horária mínima do curso técnico baseada no CNCT.")

    modalidade_de_ensino = st.selectbox("Modalidade de ensino:", 
                                       ["Educação a Distância", "Educação Presencial"],
                                       help="Informe se o curso é Presencial ou EaD.")
    tipo_de_oferta = st.selectbox("Tipo de oferta:", 
                                 ["Concomitante", "Integrado", "Subsequente", "PROEJA - Concomitante", "PROEJA - Integrado", "PROEJA - Subsequente"],
                                 help="Informe o tipo de oferta do curso.")
    turno = st.selectbox("Turno do curso:", 
                        ["Integral", "Matutino", "Vespertino", "Noturno", "Não se aplica"],
                        help="Informe o turno do curso.")

    st.markdown("---")
    
    # Botão para submeter na sidebar
    submit = st.button("🔎 Prever Evasão", use_container_width=True)


# Processamento quando o botão é clicado
if submit:
    erros = []

    if regiao_escolhida == "Selecione uma região":
        erros.append("⚠️ Por favor, selecione uma **Região**.")
    if estado_escolhido == "Selecione um Estado":
        erros.append("⚠️ Por favor, selecione um **Estado**.")
    if instituicao_escolhida == "Selecione uma Instituição":
        erros.append("⚠️ Por favor, selecione uma **Instituição**.")
    if sexo == "Selecione um Gênero":
        erros.append("⚠️ Por favor, selecione um **Gênero**.")   
    if cor_raca == "Selecione uma Cor/Raça":
        erros.append("⚠️ Por favor, selecione uma **Cor/Raça**.")   
    if renda_familiar == "Selecione uma Renda Familiar":
        erros.append("⚠️ Por favor, selecione uma **Renda Familiar**.")   
    if eixo_tecnologico_escolhido == "Selecione um Eixo Tecnológico":
        erros.append("⚠️ Por favor, selecione um **Eixo Tecnológico**.")
    if nome_de_curso == "Selecione um Curso Técnico":
        erros.append("⚠️ Por favor, selecione um **Curso Técnico**.")
    if carga_horaria_minima == 0:
        erros.append("⚠️ A **Carga Horária** deve ser maior que 0.")
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
        # Criar DataFrame de entrada
        input_data = pd.DataFrame({
            "cor_raca": ["AmarelaBranca" if cor_raca in ["Amarela", "Branca"] else cor_raca],
            "idade": [int(idade)],
            "sexo": sexo,
            "renda_familiar": renda_familiar,
            "modalidade_de_ensino": modalidade_de_ensino,
            "tipo_de_oferta": tipo_de_oferta,
            "turno": turno,
            "nome_de_curso": nome_de_curso,
            "eixo_tecnologico": eixo_tecnologico_escolhido,
            "carga_horaria_minima": [int(carga_horaria_minima)],
            "uf": estado_escolhido,
            "regiao": regiao_escolhida,
            "instituicao": instituicao_escolhida,
            "região_metropolina_ue": regiao_metropolitana_ue
        })

        # Adicionar à sessão
        if "input_data" in st.session_state:
            st.session_state.input_data = pd.concat([st.session_state.input_data, input_data], ignore_index=True)
        else:
            st.session_state.input_data = input_data


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

        # Resultados numéricos
        st.markdown("---")
        st.subheader("💻 Resultados Detalhados")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🟢 Probabilidade de NÃO EVADIR", f"{prob_nao_evasao:.2%}")
        with col2:
            st.metric("🔴 Probabilidade de EVADIR", f"{prob_evasao:.2%}")
        

    

    # =====================================================
        # EXPLAINABLE AI (XAI) - SHAP Waterfall Plot
    # =====================================================
        
        st.markdown("---")
        st.subheader("📝 Explainable Artificial Intelligence (XAI)")
        st.write("Impacto das Variáveis na Predição de Evasão:")
        
        try:
            import shap
            import matplotlib.pyplot as plt
            import numpy as np
            
            plt.title("", fontsize=14, fontweight='bold', loc='center')
            plt.tight_layout()

            # Criar explainer SHAP
            explainer = shap.TreeExplainer(model)
            
            # Preparar dados para SHAP (usando one-hot encoding se necessário)
            # Primeiro, vamos garantir que as colunas estejam na mesma ordem que o modelo espera
            input_data_encoded = input_data.copy()
            
            # Aplicar o mesmo pré-processamento usado no treinamento
            # (você precisará adaptar isso ao seu pré-processamento específico)
            
            # Calcular valores SHAP
            shap_values = explainer.shap_values(input_data_encoded)
            
            # Se for um modelo multiclasse, pegar os valores para a classe de evasão
            if isinstance(shap_values, list):
                shap_values_evasao = shap_values[1]  # Índice 1 para evasão
            else:
                shap_values_evasao = shap_values
            
            # Criar waterfall plot
            fig, ax = plt.subplots(figsize=(20, 12))
            
            # Gerar o waterfall plot
            shap.waterfall_plot(
                shap.Explanation(
                    values=shap_values_evasao[0],
                    base_values=explainer.expected_value[1] if isinstance(explainer.expected_value, list) else explainer.expected_value,
                    data=input_data_encoded.iloc[0],
                    feature_names=input_data_encoded.columns.tolist()
                ),
                max_display=15,  # Mostrar as 15 variáveis mais importantes
                show=False
            )
            
            # Centralizar o gráfico
            col1, col2, col3 = st.columns([1, 3, 1])
            with col2:
                st.pyplot(fig)
                plt.close()
            
            # Explicação adicional
            st.markdown("""
            **Interpretação do gráfico:**
            - **Valores positivos (vermelho)**: Aumentam a probabilidade de evasão
            - **Valores negativos (azul)**: Diminuem a probabilidade de evasão
            - **E[f(X)]**: Valor base (probabilidade média)
            - **f(x)**: Probabilidade final para este caso específico
            """)
            
        except Exception as e:
            st.warning(f"⚠️ Não foi possível gerar a análise de explicabilidade: {str(e)}")
  
##########################################################################################################################################################

  