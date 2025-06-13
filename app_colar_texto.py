import streamlit as st
import re
import pandas as pd

st.set_page_config(page_title="Extrair dados do texto do PDF", layout="centered")
st.title("📋 Extração de Competências, Salários e Vínculos")

st.write("Cole abaixo o texto copiado do PDF (ex: CNIS):")

texto_pdf = st.text_area("📝 Cole aqui o conteúdo do PDF:", height=400)

if texto_pdf:
    blocos = re.split(r"(?=Seq\.\s+\d+)", texto_pdf)  # Quebra por "Seq. 1", "Seq. 2", etc.
    dados = []

    for bloco in blocos:
        # Extrair número da sequência (Seq.)
        match_seq = re.search(r"Seq\.\s+(\d+)", bloco)
        seq = match_seq.group(1) if match_seq else ""

        # Extrair código do empregador (origem do vínculo)
        match_cod_emp = re.search(r"C[oó]digo Emp\. Origem do V[ií]nculo:\s*(\d+)", bloco)
        cod_emp = match_cod_emp.group(1) if match_cod_emp else ""

        # Extrair competências e salários
        matches = re.findall(r"(\d{2}/\d{4})\s+([\d\.]+,[\d]{2})", bloco)
        for competencia, remuneracao in matches:
            try:
                remun = float(remuneracao.replace(".", "").replace(",", "."))
                dados.append([competencia, remun, seq, cod_emp])
            except ValueError:
                continue

    if dados:
        df = pd.DataFrame(dados, columns=["Competência", "Remuneração (R$)", "Seq.", "Código Emp."])

        st.success("✅ Dados extraídos com sucesso!")
        st.dataframe(df)

        csv = df.to_csv(index=False, sep=";", decimal=",", encoding="utf-8-sig")
        st.download_button("📥 Baixar CSV", data=csv, file_name="salarios_extraidos.csv")
    else:
        st.warning("⚠️ Nenhum dado encontrado. Verifique o texto colado.")
