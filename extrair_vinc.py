import re
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

st.set_page_config(page_title="Extrair Vínculos", layout="wide")
st.title("📄 Extração de Vínculos com Cálculo de Tempo")

texto = st.text_area("Cole aqui o texto extraído do CNIS", height=400)

aba = st.radio("Escolha a visualização:", ["Todos os Vínculos", "Vínculos Sem Concomitância"])

def calcular_tempo(inicio, fim):
    if not inicio or not fim:
        return (0, 0, 0)
    delta = relativedelta(fim, inicio)
    return delta.years, delta.months, delta.days

def remover_concomitancias(vinculos):
    if not vinculos:
        return []
    vinculos = sorted(vinculos, key=lambda x: x[0])
    resultado = []
    atual_inicio, atual_fim = vinculos[0][0], vinculos[0][1]
    for i in range(1, len(vinculos)):
        inicio, fim = vinculos[i][0], vinculos[i][1]
        if inicio <= atual_fim:
            atual_fim = max(atual_fim, fim)
        else:
            resultado.append((atual_inicio, atual_fim))
            atual_inicio, atual_fim = inicio, fim
    resultado.append((atual_inicio, atual_fim))
    return resultado

def extrair_vinculos(texto):
    # Ignorar tudo antes de "Relações Previdenciárias"
    if "Relações Previdenciárias" in texto:
        texto = texto.split("Relações Previdenciárias", 1)[1]

    blocos = re.split(r"(?=\n?\s*\d+\s+\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})", texto)
    dados = []
    for bloco in blocos:
        match_seq = re.search(r"Seq\.\s*(\d+)", bloco)
        seq = match_seq.group(1) if match_seq else ""

        match_datas = re.findall(r"(\d{2}/\d{2}/\d{4})(?!\s+\d{2}:\d{2}:\d{2})", bloco)
        data_inicio = datetime.strptime(match_datas[0], "%d/%m/%Y").date() if len(match_datas) > 0 else None
        data_fim = datetime.strptime(match_datas[1], "%d/%m/%Y").date() if len(match_datas) > 1 else None

        match_comp = re.findall(r"(\d{2}/\d{4})", bloco)
        ultima_comp = match_comp[-1] if match_comp else ""

        anos, meses, dias = calcular_tempo(data_inicio, data_fim)
        dados.append({
            "Seq.": seq,
            "Início": data_inicio,
            "Término": data_fim,
            "Descrição": ultima_comp,
            "Contagem Anos": anos,
            "Contagem Meses": meses,
            "Contagem Dias": dias,
            "Deficiência": "Comum",
            "Simples": "Sem",
            "Fator": "1,0",
            "Convertido Anos": anos,
            "Convertido Meses": meses,
            "Convertido Dias": dias,
            "Carência": 1 if data_inicio and data_fim else 0
        })
    return dados

def calcular_total(vinculos):
    total_dias = sum((v[1] - v[0]).days + 1 for v in vinculos)
    fim = datetime(2000, 1, 1).date() + timedelta(days=total_dias)
    total = relativedelta(fim, datetime(2000, 1, 1).date())
    return total.years, total.months, total.days

if texto:
    dados = extrair_vinculos(texto)
    df = pd.DataFrame(dados)

    if aba == "Todos os Vínculos":
        st.subheader("🔍 Todos os Vínculos Extraídos")
        st.dataframe(df)

        total_anos = df["Contagem Anos"].sum()
        total_meses = df["Contagem Meses"].sum()
        total_dias = df["Contagem Dias"].sum()
        st.info(f"⏱️ Tempo total: {total_anos} anos, {total_meses} meses e {total_dias} dias")

    elif aba == "Vínculos Sem Concomitância":
        periodos = [(row["Início"], row["Término"]) for _, row in df.iterrows() if row["Início"] and row["Término"]]
        unificados = remover_concomitancias(periodos)

        dados_ajustados = []
        for i, (inicio, fim) in enumerate(unificados, 1):
            anos, meses, dias = calcular_tempo(inicio, fim)
            dados_ajustados.append({
                "Período": f"{inicio} a {fim}",
                "Anos": anos,
                "Meses": meses,
                "Dias": dias
            })

        df2 = pd.DataFrame(dados_ajustados)
        st.subheader("📘 Vínculos Sem Concomitância")
        st.dataframe(df2)

        anos, meses, dias = calcular_total(unificados)
        st.info(f"⏱️ Tempo total ajustado (sem concomitância): {anos} anos, {meses} meses e {dias} dias")
