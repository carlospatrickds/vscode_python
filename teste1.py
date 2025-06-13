import fitz  # PyMuPDF
import re
import pandas as pd

# Abre o PDF
caminho_pdf = "sahhhhhhhhhhhhh.pdf"
doc = fitz.open(caminho_pdf)

# Junta o texto de todas as páginas
texto = ""
for pagina in doc:
    texto += pagina.get_text()
doc.close()

# Expressões regulares para buscar os campos
dados_extraidos = {
    "DIB": re.search(r"DIB[:\s]*([\d]{2}/[\d]{2}/[\d]{4})", texto),
    "DIP": re.search(r"DIP[:\s]*([\d]{2}/[\d]{2}/[\d]{4})", texto),
    "RMI Concedida": re.search(r"RMI Concedida[:\s]*R?\$?\s?([\d\.]+,\d{2})", texto),
    "RMI Devida": re.search(r"RMI Devida[:\s]*R?\$?\s?([\d\.]+,\d{2})", texto),
    "Percentual de Juros": re.search(r"Juros[:\s]*([\d,]+%)", texto),
    "Total Atualizado": re.search(r"Total Atualizado[:\s]*R?\$?\s?([\d\.]+,\d{2})", texto),
}

# Trata resultados para tirar apenas o texto
resultado_limpo = {}
for campo, match in dados_extraidos.items():
    resultado_limpo[campo] = match.group(1) if match else "NÃO ENCONTRADO"

# Cria DataFrame e exporta para CSV
df = pd.DataFrame([resultado_limpo])
df.to_csv("dados_extraidos.csv", index=False, sep=";", encoding="utf-8-sig")

print("✅ Dados extraídos com sucesso para o arquivo: dados_extraidos.csv")
