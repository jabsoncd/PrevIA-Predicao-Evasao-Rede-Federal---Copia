from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pandas as pd
import pickle
import numpy as np
from typing import List, Optional
import os

# Configuração da aplicação FastAPI
app = FastAPI(
    title="PrevIA API - Predição de Evasão Estudantil",
    description="API para predição de probabilidade de evasão de estudantes na Rede Federal EPCT",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Modelo Pydantic para validação dos dados de entrada
class EstudanteRequest(BaseModel):
    cor_raca: str = Field(..., description="Cor/Raça do estudante")
    idade: int = Field(..., ge=10, le=80, description="Idade do estudante")
    sexo: str = Field(..., description="Sexo do estudante")
    renda_familiar: str = Field(..., description="Faixa de renda familiar")
    modalidade_de_ensino: str = Field(..., description="Modalidade de ensino")
    tipo_de_oferta: str = Field(..., description="Tipo de oferta do curso")
    turno: str = Field(..., description="Turno do curso")
    nome_de_curso: str = Field(..., description="Nome do curso")
    eixo_tecnologico_escolhido: str = Field(..., description="Eixo tecnológico")
    carga_horaria_minima: int = Field(..., ge=0, description="Carga horária mínima")
    estado_escolhido: str = Field(..., description="Estado da instituição")
    regiao_escolhida: str = Field(..., description="Região da instituição")
    instituicao_escolhida: str = Field(..., description="Nome da instituição")
    regiao_metropolitana_ue: str = Field(..., description="Situação de região metropolitana")

class PredicaoResponse(BaseModel):
    probabilidade_evasao: float = Field(..., description="Probabilidade de evasão (0 a 1)")
    probabilidade_nao_evasao: float = Field(..., description="Probabilidade de não evasão (0 a 1)")
    categoria_risco: str = Field(..., description="Categoria de risco")
    mensagem: str = Field(..., description="Mensagem descritiva")

class BatchPredictionRequest(BaseModel):
    estudantes: List[EstudanteRequest] = Field(..., description="Lista de estudantes para predição em lote")

class BatchPredictionResponse(BaseModel):
    predicoes: List[dict] = Field(..., description="Lista de predições para cada estudante")


# Função para carregar o modelo
def carregar_modelo():
    # modelo_lightgbm_220325.pkl
    # modelo_catboost_categorico_campeao.pkl ou modelo_lightgbm_220325.pkl
    modelo_path = os.path.join(
        "..", "notebooks", "modelo_catboost_categorico_campeao.pkl")  # ../
    with open(modelo_path, "rb") as file:
        modelo = pickle.load(file)
    return modelo
# Carregar o modelo treinado
# modelo = carregar_modelo()
# def carregar_modelo():
#     try:
#         # Ajuste o caminho conforme necessário
#         modelo_path = "modelo_evasao.pkl"
#         with open(modelo_path, 'rb') as f:
#             modelo = pickle.load(f)
#         return modelo
#     except Exception as e:
#         raise RuntimeError(f"Erro ao carregar o modelo: {e}")

# # Carregar o modelo uma vez ao iniciar a aplicação
modelo = carregar_modelo()

# Função para categorizar o risco
def categorizar_risco(prob_evasao: float) -> str:
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

# Endpoint de saúde da API
@app.get("/", tags=["Health Check"])
async def root():
    return {
        "message": "PrevIA API - Predição de Evasão Estudantil",
        "status": "Online",
        "version": "1.0.0"
    }

@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "healthy", "model_loaded": modelo is not None}

# Endpoint para predição individual
@app.post("/predizer-evasao", response_model=PredicaoResponse, tags=["Predição"])
async def predizer_evasao(estudante: EstudanteRequest):
    """
    Realiza a predição de evasão para um único estudante
    
    - **cor_raca**: Cor/Raça do estudante
    - **idade**: Idade do estudante (10-80)
    - **sexo**: Sexo do estudante
    - **renda_familiar**: Faixa de renda familiar
    - **modalidade_de_ensino**: Modalidade de ensino
    - **tipo_de_oferta**: Tipo de oferta do curso
    - **turno**: Turno do curso
    - **nome_de_curso**: Nome do curso
    - **eixo_tecnologico_escolhido**: Eixo tecnológico
    - **carga_horaria_minima**: Carga horária mínima
    - **estado_escolhido**: Estado da instituição
    - **regiao_escolhida**: Região da instituição
    - **instituicao_escolhida**: Nome da instituição
    - **regiao_metropolitana_ue**: Situação de região metropolitana
    """
    try:
        # Criar DataFrame no formato esperado pelo modelo
        input_data = pd.DataFrame({
            'cor_raca': [estudante.cor_raca],
            'idade': [estudante.idade],
            'sexo': [estudante.sexo],
            'renda_familiar': [estudante.renda_familiar],
            'modalidade_de_ensino': [estudante.modalidade_de_ensino],
            'tipo_de_oferta': [estudante.tipo_de_oferta],
            'turno': [estudante.turno],
            'nome_de_curso': [estudante.nome_de_curso],
            'eixo_tecnologico': [estudante.eixo_tecnologico_escolhido],
            'carga_horaria_minima': [estudante.carga_horaria_minima],
            'uf': [estudante.estado_escolhido],
            'regiao': [estudante.regiao_escolhida],
            'instituicao': [estudante.instituicao_escolhida],
            'região_metropolina_ue': [estudante.regiao_metropolitana_ue]
        })
        
        # Fazer a predição
        probabilidades = modelo.predict_proba(input_data)
        
        # Processar probabilidades
        if len(probabilidades.shape) == 2 and probabilidades.shape[1] == 2:
            prob_evasao = probabilidades[0, 1]  # Probabilidade da classe 1 (evasão)
        else:
            prob_evasao = probabilidades[0]
        
        prob_nao_evasao = 1 - prob_evasao
        categoria = categorizar_risco(prob_evasao)
        
        return PredicaoResponse(
            probabilidade_evasao=round(prob_evasao, 4),
            probabilidade_nao_evasao=round(prob_nao_evasao, 4),
            categoria_risco=categoria,
            mensagem=f"Predição realizada com sucesso: {categoria}"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na predição: {str(e)}")

# Endpoint para predição em lote
@app.post("/predizer-evasao-lote", response_model=BatchPredictionResponse, tags=["Predição"])
async def predizer_evasao_lote(request: BatchPredictionRequest):
    """
    Realiza predição de evasão para múltiplos estudantes em lote
    """
    try:
        # Converter lista de estudantes para DataFrame
        dados_estudantes = []
        for estudante in request.estudantes:
            dados_estudantes.append({
                'cor_raca': estudante.cor_raca,
                'idade': estudante.idade,
                'sexo': estudante.sexo,
                'renda_familiar': estudante.renda_familiar,
                'modalidade_de_ensino': estudante.modalidade_de_ensino,
                'tipo_de_oferta': estudante.tipo_de_oferta,
                'turno': estudante.turno,
                'nome_de_curso': estudante.nome_de_curso,
                'eixo_tecnologico': estudante.eixo_tecnologico_escolhido,
                'carga_horaria_minima': estudante.carga_horaria_minima,
                'uf': estudante.estado_escolhido,
                'regiao': estudante.regiao_escolhida,
                'instituicao': estudante.instituicao_escolhida,
                'região_metropolina_ue': estudante.regiao_metropolitana_ue
            })
        
        df_input = pd.DataFrame(dados_estudantes)
        
        # Fazer predições em lote
        probabilidades = modelo.predict_proba(df_input)
        
        # Processar resultados
        predicoes = []
        for i, (_, estudante) in enumerate(df_input.iterrows()):
            if len(probabilidades.shape) == 2 and probabilidades.shape[1] == 2:
                prob_evasao = probabilidades[i, 1]
            else:
                prob_evasao = probabilidades[i]
            
            prob_nao_evasao = 1 - prob_evasao
            categoria = categorizar_risco(prob_evasao)
            
            predicoes.append({
                "indice": i,
                "probabilidade_evasao": round(prob_evasao, 4),
                "probabilidade_nao_evasao": round(prob_nao_evasao, 4),
                "categoria_risco": categoria,
                "estudante": {
                    "cor_raca": estudante['cor_raca'],
                    "idade": int(estudante['idade']),
                    "sexo": estudante['sexo'],
                    "nome_curso": estudante['nome_de_curso']
                }
            })
        
        return BatchPredictionResponse(predicoes=predicoes)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na predição em lote: {str(e)}")

# Endpoint para obter informações do modelo
@app.get("/modelo/info", tags=["Modelo"])
async def obter_info_modelo():
    """Retorna informações sobre o modelo carregado"""
    try:
        info = {
            "tipo_modelo": type(modelo).__name__,
            "features_esperadas": [
                'cor_raca', 'idade', 'sexo', 'renda_familiar', 'modalidade_de_ensino',
                'tipo_de_oferta', 'turno', 'nome_de_curso', 'eixo_tecnologico',
                'carga_horaria_minima', 'uf', 'regiao', 'instituicao', 'região_metropolina_ue'
            ],
            "status": "Carregado com sucesso"
        }
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter informações do modelo: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)