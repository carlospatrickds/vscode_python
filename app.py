import streamlit as st

# Título da página
st.title("🧾 Ficha de Cliente")

# Coletando dados com interface amigável
nome = st.text_input("Digite o nome do cliente")
idade = st.number_input("Digite a idade do cliente", min_value=0, step=1)
renda = st.number_input("Digite a renda mensal do cliente (R$)", min_value=0.0, step=100.0, format="%.2f")
profissao = st.text_input("Digite a profissão do cliente")

# Quando o botão for pressionado
if st.button("📋 Analisar Cliente"):
    st.subheader("📄 Ficha do Cliente")
    st.write(f"**Nome:** {nome}")
    st.write(f"**Idade:** {idade} anos")
    st.write(f"**Renda:** R$ {renda}")
    st.write(f"**Profissão:** {profissao}")

    st.subheader("🔍 Análise de Perfil")

    # Regra 1 – Benefício por renda
    if renda < 2000:
        st.success("✅ Pode ter direito ao benefício por baixa renda.")
    else:
        st.warning("❌ Não se enquadra no critério de renda.")

    # Regra 2 – Idoso
    if idade >= 60:
        st.info("👵 Cliente é considerado idoso.")
    else:
        st.info("🧒 Cliente não é idoso.")

    # Regra 3 – Situação crítica
    if profissao.lower() == "desempregado":
        st.error("🚨 Situação crítica detectada!")
    else:
        st.success("🧑 Cliente possui emprego.")
