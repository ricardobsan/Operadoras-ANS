from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

df = pd.read_csv("Relatorio_cadop.csv", delimiter=";", encoding="utf-8", low_memory=False)

@app.get("/operadoras")
def buscar_operadoras(
    nome: str = Query(None, description="Nome da operadora"),
    cnpj: str = Query(None, description="CNPJ da operadora"),
    registro_ans: str = Query(None, description="Registro ANS"),
    cidade: str = Query(None, description="Cidade da operadora"),
    uf: str = Query(None, description="Estado (UF) da operadora"),
    limite: int = Query(100, description="Número máximo de resultados retornados")
):
    resultado = df.copy()
    
    if nome:
        resultado = resultado[resultado["Razao_Social"].fillna("").str.contains(nome, case=False, na=False)]
    if cnpj:
        resultado = resultado[resultado["CNPJ"].astype(str).str.strip() == cnpj.strip()]
    if registro_ans:
        resultado = resultado[resultado["Registro_ANS"].astype(str).str.strip() == registro_ans.strip()]
    if cidade:
        resultado = resultado[resultado["Cidade"].fillna("").str.contains(cidade, case=False, na=False)]
    if uf and len(uf) == 2:
        resultado = resultado[resultado["UF"].fillna("").str.upper() == uf.upper()]

    colunas_essenciais = ["Razao_Social", "CNPJ", "Registro_ANS", "Cidade", "UF"]
    resultado = resultado[colunas_essenciais]
    
    resultado = resultado.head(limite)

    return resultado.fillna("").to_dict(orient="records")
