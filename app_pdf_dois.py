import streamlit as st
import pandas as pd
import fitz  # PyMuPDF
import re
import io

st.set_page_config(page_title="Analisador de Benefícios", layout="wide")
st.title("📂 Extração de Dados Previdenciários")

# Upload dos arquivos
st.subheader("🔸 Enviar arquivos PDF")

cnis_file = st.file_uploader("📌 Enviar PDF do CNIS", type=["pdf"], key="cnis")
carta_file = st.file_uploader("📌 Enviar PDF da Carta de Concessão", type=["pdf"], key="carta")
sentenca_file = st.file_uploader("📌 Enviar PDF da Sentença", type=["pdf"], key="sentenca")

sheets = {}

# Função para extrair texto do PDF
def extrair_texto(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    texto = "\n".join([page.get_text() for page in doc])
    doc.close()
    return texto

# --------------------
# Processamento do CNIS
# --------------------
if cnis_file:
    texto = extrair_texto(cnis_file)

    padrao_seq = r"Seq\.:\s*(\d+)"
    padrao_comp_salario = r"(\d{2}/\d{4})\s+([\d\.]+,[\d]{2})"

    blocos = re.split(padrao_seq, texto)
    dados = []

    for i in range(1, len(blocos), 2):
        seq = blocos[i].strip()
        bloco_texto = blocos[i + 1]
        linhas = bloco_texto.splitlines()
        for linha in linhas:
            match = re.search(padrao_comp_salario, linha)
            if match:
                comp, sal = match.groups()
                sal = sal.replace(".", "").replace(",", ".")
                dados.append([seq, comp, float(sal)])

    if dados:
        df_cnis = pd.DataFrame(dados, columns=["SEQ", "Competência", "Salário (R$)"])
        sheets["CNIS"] = df_cnis
        st.success("✅ CNIS processado com sucesso!")
        st.dataframe(df_cnis)
    else:
        st.warning("⚠️ Nenhum dado encontrado no CNIS.")

# -------------------------------
# Processamento da Carta de Concessão
# -------------------------------
if carta_file:
    texto = extrair_texto(carta_file)

    matches = re.findall(r"(\d{2}/\d{4})\s+([\d\.]+,[\d]{2})", texto)
    dados = [[comp, float(valor.replace(".", "").replace(",", "."))] for comp, valor in matches]
    df_salarios = pd.DataFrame(dados, columns=["Competência", "Salário (R$)"])
    sheets["Carta - Salários"] = df_salarios

    def buscar_valor(padrao, texto_base=texto):
        resultado = re.search(padrao, texto_base, re.IGNORECASE)
        return resultado.group(1).strip() if resultado else "Não encontrado"

    nome_match = re.search(r"Nome[:\-]?\s*([A-Z À-Ú]{5,})\s{2,}", texto)
    nome_segurado = nome_match.group(1).strip() if nome_match else "Não encontrado"

    especie_match = re.search(r"\((\d{2})\)", texto)
    especie = especie_match.group(1) if especie_match else "Não encontrado"

    dib_match = re.search(r"vigência a partir de\s*(\d{2}/\d{2}/\d{4})", texto, re.IGNORECASE)
    dib = dib_match.group(1).strip() if dib_match else "Não encontrado"

    rmi_match = re.search(r"R\$\s*([\d\.]+,[\d]{2})", texto, re.IGNORECASE)
    rmi = rmi_match.group(1).replace(".", "").replace(",", ".") if rmi_match else "Não encontrado"

    dados_info = {
        "Nome do Segurado": nome_segurado,
        "Número do Benefício": buscar_valor(r"Número do Benefício:\s*(\d+)", texto),
        "DIB": dib,
        "Espécie": especie,
        "RMI": rmi,
        "Coeficiente": buscar_valor(r"Coeficiente\s*=\s*([\d\.,]+)", texto)
    }
    df_info = pd.DataFrame(dados_info.items(), columns=["Campo", "Valor"])
    sheets["Carta - Dados Gerais"] = df_info

    st.success("✅ Carta de Concessão processada com sucesso!")
    st.dataframe(df_salarios)
    st.dataframe(df_info)

# --------------------
# Processamento da Sentença
# --------------------
if sentenca_file:
    texto = extrair_texto(sentenca_file)

    dispositivo_match = re.search(r"(DISPOSITIVO[\s\S]+?)(?:\n\n|\Z)", texto, re.IGNORECASE)
    dispositivo = dispositivo_match.group(1).strip() if dispositivo_match else "Dispositivo não encontrado."

    dib_match = re.search(r"DIB\s+em\s+(\d{2}/\d{2}/\d{4})", texto, re.IGNORECASE)
    dib_valor = dib_match.group(1) if dib_match else "Não encontrado"

    dip_valor = 0

    df_sentenca = pd.DataFrame({
        "Dispositivo da Sentença": [dispositivo],
        "DIB Extraído": [dib_valor],
        "DIP Extraído": [dip_valor]
    })
    sheets["Sentença"] = df_sentenca

    st.success("✅ Sentença processada com sucesso!")
    st.dataframe(df_sentenca)

# --------------------
# Download do Excel
# --------------------
if sheets:
    with io.BytesIO() as buffer:
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            for nome, df in sheets.items():
                df.to_excel(writer, sheet_name=nome[:31], index=False)
        st.download_button(
            label="📅 Baixar dados extraídos (.xlsx)",
            data=buffer.getvalue(),
            file_name="dados_extraidos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
