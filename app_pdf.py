import streamlit as st
import fitz  # PyMuPDF
import re
import pandas as pd

st.set_page_config(page_title="Extrair Salários e Vínculos", layout="centered")
st.title("📄 Extração de Competências, Salários e Código do Empregador")

uploaded_file = st.file_uploader("Envie um PDF com vínculos e salários:", type="pdf")

if uploaded_file is not None:
    texto_pdf = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            texto_pdf += page.get_text("text")

    blocos = re.split(r"(?=Seq\.\s+\d+)", texto_pdf)

    dados = []

    for bloco in blocos:
        match_seq = re.search(r"Seq\.\s+(\d+)", bloco)
        if not match_seq:
            continue
        seq = match_seq.group(1)

        match_codigo_emp = re.search(r"C[oó]digo Emp\. Origem do V[ií]nculo:\s*(\d+)", bloco)
        codigo_emp = match_codigo_emp.group(1) if match_codigo_emp else ""

        matches = re.findall(r"(\d{2}/\d{4})\s+([\d\.]+,[\d]{2})", bloco)
        for competencia, remuneracao in matches:
            try:
                remuneracao_float = float(remuneracao.replace(".", "").replace(",", "."))
                dados.append([seq, codigo_emp, competencia, remuneracao_float])
            except ValueError:
                continue

    if dados:
        df = pd.DataFrame(dados, columns=["Seq.", "Código Emp.", "Competência", "Remuneração (R$)"])
        st.success("✅ Competências, salários e códigos extraídos com sucesso!")
        st.dataframe(df)

        csv = df.to_csv(index=False, sep=";", decimal=",", encoding="utf-8-sig")
        st.download_button("📥 Baixar CSV", data=csv, file_name="salarios_extraidos.csv")
    else:
        st.warning("⚠️ Nenhuma competência ou salário foi encontrado no texto do PDF.")
