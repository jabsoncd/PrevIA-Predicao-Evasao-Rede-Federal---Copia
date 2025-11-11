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
        <a class="nav-link" href="/Simulador_Eficiencia_Layout_Gestor_Carga" target="_self">Módulo Carga</a>
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

st.write(" ")
st.write(" ")
st.write(" ")

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
st.markdown("---")
st.subheader("📊 Carga de Dados em Lote")

st.markdown(
    """
    <p style='color: #3f3f4f; margin-bottom: 15px;'>
        Faça a carga de dados em lote utilizando o dicionário de dados disponível no 
        <a href='https://exemplo.com/dicionario-dados' target='_blank'>link para download do template CSV</a>.
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
if uploaded_file is not None:
    try:
        # Ler o arquivo CSV
        df_lote = pd.read_csv(uploaded_file)
        
        # Exibir o dataframe carregado
        st.subheader("📋 Dados Carregados do Arquivo CSV")
        st.write(f"Total de registros: {len(df_lote)}")
        st.dataframe(df_lote)
        
        # Botão para processar a predição em lote
        if st.button("🚀 Prever Evasão em Lote", type="primary"):
            # Mensagem de processamento
            placeholder_mensagem = st.empty()
            placeholder_mensagem.success("🔄 Processando previsão em lote...")
            
            try:
                # Realizar as predições para todos os registros
                probabilidades = model.predict_proba(df_lote)
                
                # Adicionar colunas de resultados
                df_resultado = df_lote.copy()
                df_resultado['Chance de Não Evadir'] = [f"{prob[0]:.2%}" for prob in probabilidades]
                df_resultado['Chance de Evadir'] = [f"{prob[1]:.2%}" for prob in probabilidades]
                df_resultado['Categoria de Risco'] = [categorizar_risco(prob[1]) for prob in probabilidades]
                
                # Remover mensagem de processamento
                placeholder_mensagem.empty()
                
                # Exibir resultados
                st.subheader("📈 Resultados da Predição em Lote")
                st.dataframe(df_resultado)
                
                # Botão para download dos resultados
                csv_resultado = df_resultado.to_csv(index=False)
                st.download_button(
                    label="📥 Download dos Resultados em CSV",
                    data=csv_resultado,
                    file_name="resultados_predicao_evasao.csv",
                    mime="text/csv"
                )
                
                # Estatísticas resumidas
                st.subheader("📊 Estatísticas das Predições")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    alta_evasao = len([prob for prob in probabilidades if prob[1] > 0.7])
                    st.metric("Alto Risco de Evasão", alta_evasao)
                
                with col2:
                    moderada_evasao = len([prob for prob in probabilidades if 0.5 <= prob[1] <= 0.7])
                    st.metric("Risco Moderado", moderada_evasao)
                
                with col3:
                    baixa_evasao = len([prob for prob in probabilidades if prob[1] < 0.5])
                    st.metric("Baixo Risco", baixa_evasao)
                    
            except Exception as e:
                placeholder_mensagem.empty()
                st.error(f"❌ Erro ao processar as predições: {str(e)}")
                
    except Exception as e:
        st.error(f"❌ Erro ao ler o arquivo CSV: {str(e)}")
        st.info("💡 Verifique se o arquivo está no formato correto e contém todas as colunas necessárias.")

# Linha divisória antes do formulário individual
st.markdown("---")

# Container centralizado para o formulário individual
with st.container():
    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        st.subheader("🎯 Simulação Individual")
        st.write("Preencha os dados abaixo para uma simulação individual:")

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

        # Definição de eixos tecnologicos
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
            index=0,
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
            index=0,
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
        submit = st.button("🔎 Prever Evasão - Simulação Individual")

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

                st.subheader("📋 Simulações Realizadas")
                if "input_data" in st.session_state:
                    st.session_state.input_data = pd.concat(
                        [st.session_state.input_data, input_data], ignore_index=True)
                else:
                    st.session_state.input_data = input_data

                st.write(st.session_state.input_data)

                # Botão para limpar as simulações
                if st.button("Limpar Simulações"):
                    st.session_state.input_data = pd.DataFrame()
                    st.write("Simulações limpas com sucesso!")

                # Mensagem temporária
                placeholder_mensagem = st.empty()
                placeholder_mensagem.success("Processando a previsão de evasão...")

                # Predição
                probabilidades = model.predict_proba(input_data)[0]
                prob_nao_evasao = probabilidades[0]
                prob_evasao = probabilidades[1]

                import plotly.graph_objects as go
                import time

                valor_final = round(prob_evasao * 100, 2)
                chart_placeholder = st.empty()

                # Animação do ponteiro do velocímetro
                for valor_atual in range(0, int(valor_final) + 1, 1):
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=valor_atual,
                        number={'valueformat': '.f', 'suffix': "%",
                                'font': {'size': 45, 'color': "#656770"}},
                        gauge={
                            'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': "#7f8c8d"},
                            'bar': {'color': "#2C3E50"},
                            'steps': [
                                {'range': [0, 40], 'color': "#27AE60"},
                                {'range': [40, 70], 'color': "#F1C40F"},
                                {'range': [70, 100], 'color': "#E74C3C"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.85,
                                'value': valor_atual
                            }
                        }
                    ))

                    fig.update_layout(
                        margin=dict(l=20, r=40, t=10, b=20),
                        paper_bgcolor="#f2f4f5",
                        font=dict(color="#2c3e50", family="Arial")
                    )

                    chart_placeholder.plotly_chart(fig)
                    time.sleep(0.1)

                placeholder_mensagem.empty()

                # Definir categorias de risco
                if prob_evasao < 0.50:
                    st.success(
                        f"✅ Baixa probabilidade de evasão. (Não evade: {prob_nao_evasao:.2%})")
                elif 0.51 <= prob_evasao <= 0.60:
                    st.warning(
                        f"⚠️ Moderada chance de evasão. (Evade: {prob_evasao:.2%})")
                elif 0.61 <= prob_evasao <= 0.70:
                    st.warning(
                        f"⚠️ Considerável probabilidade de evasão. (Evade: {prob_evasao:.2%})")
                elif 0.71 <= prob_evasao <= 0.90:
                    st.error(f"⚠️ Alta chance de evasão! (Evade: {prob_evasao:.2%})")
                else:
                    st.error(
                        f"🚨 Muito alta chance de evasão! (Evade: {prob_evasao:.2%})")

                # Exibir os resultados
                st.subheader("💻 Resultados da Predição")
                st.write(f"🟢 Probabilidade de **NÃO EVADIR**: {prob_nao_evasao:.2%}")
                st.write(f"🔴 Probabilidade de **EVADIR**: {prob_evasao:.2%}")