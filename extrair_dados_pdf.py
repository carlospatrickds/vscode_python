import fitz  # PyMuPDF
import re
import pandas as pd

# Caminho do seu PDF
caminho_pdf = "sahhhhhhhhhhhhh.pdf"

# Abre o PDF
doc = fitz.open(caminho_pdf)

# Extrai todo o texto do PDF
texto = ""
for pagina in doc:
    texto += pagina.get_text()
doc.close()

# Define os padrões que queremos buscar com expressões regulares
dados_extraidos = {
    "DIB": re.search(r"DIB[:\s]*([\d]{2}/[\d]{2}/[\d]{4})", texto),
    "DIP": re.search(r"DIP[:\s]*([\d]{2}/[\d]{2}/[\d]{4})", texto),
    "RMI Concedida": re.search(r"RMI Concedida[:\s]*R?\$?\s?([\d\.]+,\d{2})", texto),
    "RMI Devida": re.search(r"RMI Devida[:\s]*R?\$?\s?([\d\.]+,\d{2})", texto),
    "Percentual de Juros": re.search(r"Juros[:\s]*([\d,]+%)", texto),
    "Total Atualizado": re.search(r"Total Atualizado[:\s]*R?\$?\s?([\d\.]+,\d{2})", texto),
}

# Limpa os resultados encontrados
resultado_limpo = {}
for campo, match in dados_extraidos.items():
    if match:
        resultado_limpo[campo] = match.group(1)
    else:
        resultado_limpo[campo] = "NÃO ENCONTRADO"

# Cria um DataFrame do pandas com os dados
df = pd.DataFrame([resultado_limpo])

# Exporta para CSV
df.to_csv("dados_extraidos.csv", index=False, sep=";", encoding="utf-8-sig")

print("✅ Arquivo 'dados_extraidos.csv' criado com sucesso!")
