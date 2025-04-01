import pdfplumber
import pandas as pd
import zipfile
import os

pdf_path = "Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf" 
csv_path = "rol_procedimentos.csv"
zip_path = "Teste_Ricardo.zip"

substituicoes = {
    "OD": "Seg. Odontológica",
    "AMB": "Seg. Ambulatorial"
}

def extrair_tabela_do_pdf(pdf_path):
    dados = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tabelas = page.extract_tables()
            for tabela in tabelas:
                for linha in tabela:
                    dados.append(linha)
    
    return dados

dados = extrair_tabela_do_pdf(pdf_path)


df = pd.DataFrame(dados)

df.columns = df.iloc[0]
df = df[1:] 


df.replace(substituicoes, inplace=True)


df.to_csv(csv_path, index=False, encoding="utf-8")

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(csv_path)

os.remove(csv_path)

print(f"Processo concluído! O arquivo compactado foi salvo como: {zip_path}")
