# import streamlit as st
# import base64

# # Função para converter imagem local em Base64


# def get_base64_of_image(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode()


# # Converter a imagem local
# # Certifique-se de que o arquivo está no mesmo diretório do código
# img_base64 = get_base64_of_image("templates/dropout1.jpg")

# # Configuração da página
# st.set_page_config(
#     page_title="Plataforma PrevIA",
#     page_icon="previa_azulmenor.png",
#     layout="wide",
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

# # 🔹 Ocultar completamente o sidebar (menu lateral)
# st.markdown(
#     """
#     <style>
#     [data-testid="stSidebar"] {
#         display: none;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )
 
# # 🔹 CSS para definir a imagem de fundo
# st.markdown(
#     f"""
#     <style>
#     .stApp {{
#         background-image: url("data:image/jpg;base64,{img_base64}");
#         background-size: cover;
#         background-position: center;
#         background-attachment: fixed;
#     }}
#     </style>
#     """,
#     unsafe_allow_html=True
# )
# # 🔹 Cabeçalho
# left_co, cent_co, last_co = st.columns([12, 5, 12])
# with cent_co:
#     # use_column_width ------- use_container_width
#     st.image("images/logo_previa.jpg", width=100, use_container_width=True) #images/
# # 🔹 Centraliza o título
# st.markdown("<h2 style='text-align: center; color: white; margin-bottom: 5px;'>PrevIA - Predição de Evasão na Rede Federal com Inteligência Artificial</h2>", unsafe_allow_html=True)
# # 🔹 Texto introdutório centralizado
# st.markdown("<p style='text-align: center; color: white; margin-top: 0px;'>Este projeto tem por objetivo ser uma plataforma para todos aqueles que desejam obter informações do comportamento da evasão na RFEPCT.</p>", unsafe_allow_html=True)

# # 🔹 Criando colunas para centralizar os cards
# col1, col2, col3 = st.columns([1, 3, 1])

# with col2:
#     # 🔹 Card 1 - Indicadores de Evasão
#     st.markdown(
#         """
#         <div style="text-align: center; padding: 16px; border-radius: 10px; 
#                     background-color: rgba(255, 255, 255, 0.8); 
#                     box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
#             <h3>Simulador de Evasão</h3>
#             <p>Simule a probabilidade de evasão de um aluno.</p>
#             <a href="Simulador_Eficiencia" target="_self">
#                 <button style="padding: 4px 15px; border-radius: 7px; 
#                               border: none; background-color: #28A745; 
#                               color: white; font-size: 19px; cursor: pointer;">
#                     Acessar
#                 </button>
#             </a>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )
#     st.markdown("<br>", unsafe_allow_html=True)
#          # 🔹 Card 2 - Simulador de Evasão
#     st.markdown(
#         """
#         <div style="text-align: center; padding: 16px; border-radius: 10px;
#                     background-color: rgba(255, 255, 255, 0.8); 
#                     box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
#             <h3>Indicadores de Evasão</h3>
#             <p>Análises e estatísticas sobre evasão escolar.</p>
#             <a href="Indicadores_Eficiencia" target="_self">
#                 <button style="padding: 4px 15px; border-radius: 7px; 
#                               border: none; background-color: #007BFF; 
#                               color: white; font-size: 19px; cursor: pointer;">
#                     Acessar
#                 </button>
#             </a>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )   

# st.markdown("<hr style='border: 1px solid white;'>", unsafe_allow_html=True)
# st.markdown("<p style='color: white;'>Versão 0.0.1 - Brasília - 2025. Universidade Federal do Tocantins - UFT.</p>", unsafe_allow_html=True)


import streamlit as st
import base64

# Função para converter imagem local em Base64
def get_base64_of_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Carregar imagem de fundo
img_base64 = get_base64_of_image("templates/dropout1_uniform.jpg")  # Substitua pelo caminho da imagem desejada

# Configurar página
st.set_page_config(
    page_title="Plataforma PrevIA",
    page_icon="images/previa_azulmenor.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS global moderno
st.markdown(f"""
    <style>
    #MainMenu, footer, header {{ visibility: hidden; }}
    [data-testid="stSidebar"] {{ display: none; }}

    .stApp {{
        background-image: url("data:image/jpg;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Segoe UI', sans-serif;
    }}

    p {{
        color: #f0f0f0;
        font-size: 18px;
        text-align: left;
        text-shadow: 1px 1px 3px #000;
    }}

    .custom-card {{
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: all 0.3s ease-in-out;
    }}

    .custom-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 12px 48px rgba(31, 38, 135, 0.5);
    }}

    .custom-button {{
        padding: 10px 25px;
        font-size: 18px;
        border: none;
        border-radius: 30px;
        cursor: pointer;
        margin-top: 15px;
        transition: 0.2s;
    }}

    .green-btn {{
        background-color: #00c853;
        color: white;
    }}

    .blue-btn {{
        background-color: #2979ff;
        color: white;
    }}

    .custom-button:hover {{
        filter: brightness(1.1);
    }}

    .footer {{
        color: #ffffff;
        font-size: 13px;
        margin-top: 40px;
        text-align: left;
    }}
    </style>
""", unsafe_allow_html=True)
# Layout centralizado com 3 colunas: esquerda (vazia), centro (conteúdo), direita (vazia)
left_co, cent_co, right_co = st.columns([1, 2, 1])

with cent_co:
    # Logo centralizada com tamanho maior
    st.image("images/logo_previa.jpg", width=280)

    # Título centralizado com fonte branca moderna
    st.markdown("""
        <h2 style='text-align: center; color: white; font-family: "Segoe UI", sans-serif;
        font-weight: 600; margin-bottom: 10px; text-shadow: 2px 2px 4px #000;'>
            PrevIA - Predição de Evasão na Rede Federal com Inteligência Artificial
        </h2>
    """, unsafe_allow_html=True)

    # Parágrafo descritivo também centralizado
    st.markdown("""
        <p style='text-align: center; color: #f0f0f0; font-size: 18px;
        font-family: "Segoe UI", sans-serif; text-shadow: 1px 1px 3px #000;'>
            Este projeto tem por objetivo ser uma plataforma para todos aqueles que desejam obter informações
            sobre o comportamento da evasão na Rede Federal de Educação Profissional, Científica e Tecnológica.
        </p>
    """, unsafe_allow_html=True)

# Layout: cards à esquerda, imagem à direita
# col_left, col_right = st.columns([1.2, 2.5])
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    # Card 1 - Simulador
    st.markdown("""
        <div class="custom-card">
            <h3 style="color:white; text-align:center;">Simulador de Evasão</h3>
            <p style="text-align:center;">Simule a probabilidade de evasão de um aluno.</p>
            <div style="text-align:center;">
                <a href="Simulador_Eficiencia" target="_self">
                    <button class="custom-button green-btn">Acessar</button>
                </a>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Card 2 - Indicadores
    st.markdown("""
        <div class="custom-card">
            <h3 style="color:white; text-align:center;">Indicadores de Evasão</h3>
            <p style="text-align:center;">Análises e estatísticas sobre evasão escolar.</p>
            <div style="text-align:center;">
                <a href="Indicadores_Eficiencia" target="_self">
                    <button class="custom-button blue-btn">Acessar</button>
                </a>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Rodapé
st.markdown("<hr style='border: 1px solid white;'>", unsafe_allow_html=True)
st.markdown("<p class='footer'>Versão 0.0.1 - Brasília - 2025. Universidade Federal do Tocantins - UFT.</p>", unsafe_allow_html=True)
