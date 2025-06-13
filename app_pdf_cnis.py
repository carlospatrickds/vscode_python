import streamlit as st
import pandas as pd
import fitz  # PyMuPDF
import re
import io

st.set_page_config(page_title="Extrator CNIS", layout="wide")
st.title("📄 Extrator de Dados do CNIS")

st.subheader("🔸 Enviar PDF do CNIS")
cnis_file = st.file_uploader("📌 Enviar PDF do CNIS", type=["pdf"])

def extrair_texto(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    texto = "\n".join([page.get_text() for page in doc])
    doc.close()
    return texto

if cnis_file:
    texto = extrair_texto(cnis_file)

    padrao_bloco = r"(Seq\.: \d+[\s\S]+?)(?=Seq\.|$)"
    padrao_seq = r"Seq\.: (\d+)"
    padrao_comp_salario = r"(\d{2}/\d{4})\s+([\d\.]+,[\d]{2})"

    blocos = re.findall(padrao_bloco, texto)
    dados = []

    for bloco in blocos:
        seq_match = re.search(padrao_seq, bloco)
        if not seq_match:
            continue
        seq = seq_match.group(1)

        matches = re.findall(padrao_comp_salario, bloco)
        for comp, sal in matches:
            sal = sal.replace(".", "").replace(",", ".")
            dados.append([seq, comp, float(sal)])

    if dados:
        df_cnis = pd.DataFrame(dados, columns=["SEQ", "Competência", "Salário (R$)"])
        st.success("✅ CNIS processado com sucesso!")
        st.dataframe(df_cnis)

        with io.BytesIO() as buffer:
            with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
                df_cnis.to_excel(writer, sheet_name="CNIS", index=False)
            st.download_button(
                label="📥 Baixar planilha CNIS (.xlsx)",
                data=buffer.getvalue(),
                file_name="cnis_extraido.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.warning("⚠️ Nenhum dado encontrado no CNIS.")