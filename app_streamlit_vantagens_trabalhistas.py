import streamlit as st
from num2words import num2words

st.title("📊 Sistema de Cálculo de Adicionais Trabalhistas")
st.write("Preencha os dados abaixo para calcular os adicionais:")

# Entrada de salário base
salario_base = st.number_input("Salário Base (R$)", min_value=0.0, step=100.0, format="%.2f")

# Entrada percentual de insalubridade (em vez de fixo)
percentual_insalubridade = st.number_input("Percentual de Insalubridade (%)", min_value=0.0, max_value=40.0, value=0.0, step=10.0)

# Checkbox para periculosidade e entrada do percentual
recebe_periculosidade = st.checkbox("Recebe Periculosidade?")
percentual_periculosidade = 0.0
if recebe_periculosidade:
    percentual_periculosidade = st.number_input("Percentual de Periculosidade (%)", min_value=0.0, max_value=50.0, value=30.0, step=5.0)

# Horas trabalhadas
horas_noturnas = st.number_input("Horas Noturnas Eventuais", min_value=0.0, step=1.0)
horas_50 = st.number_input("Horas Extras 50%", min_value=0.0, step=1.0)
horas_100 = st.number_input("Horas Extras 100%", min_value=0.0, step=1.0)

# Botão calcular
if st.button("Calcular", key="btn_calcular"):
    adicional_insalubridade = salario_base * (percentual_insalubridade / 100)
    adicional_periculosidade = salario_base * (percentual_periculosidade / 100)
    valor_hora = salario_base / 220  # Jornada mensal de referência

    adicional_noturno = horas_noturnas * valor_hora * 0.2
    adicional_50 = horas_50 * valor_hora * 0.5
    adicional_100 = horas_100 * valor_hora * 1.0

    total_adicionais = (
        adicional_insalubridade +
        adicional_periculosidade +
        adicional_noturno +
        adicional_50 +
        adicional_100
    )

    st.subheader("📝 Dados informados:")
    st.write(f"🔹 Salário Base: R$ {salario_base:,.2f} ({num2words(salario_base, lang='pt_BR', to='currency')})")
    st.write(f"🔹 Percentual de Insalubridade: {percentual_insalubridade:.0f}% ({num2words(percentual_insalubridade, lang='pt_BR')} por cento)")
    if recebe_periculosidade:
        st.write(f"🔹 Percentual de Periculosidade: {percentual_periculosidade:.0f}% ({num2words(percentual_periculosidade, lang='pt_BR')} por cento)")
    st.write(f"🌙 Horas Noturnas: {horas_noturnas:.0f} ({num2words(horas_noturnas, lang='pt_BR')} horas)")
    st.write(f"⏱️ Horas Extras 50%: {horas_50:.0f} ({num2words(horas_50, lang='pt_BR')} horas)")
    st.write(f"⏱️ Horas Extras 100%: {horas_100:.0f} ({num2words(horas_100, lang='pt_BR')} horas)")

    st.subheader("💰 Resultado:")
    st.write(f"🔹 Adicional de Insalubridade: R$ {adicional_insalubridade:.2f}")
    st.write(f"🔹 Adicional de Periculosidade: R$ {adicional_periculosidade:.2f}")
    st.write(f"🌙 Adicional Noturno: R$ {adicional_noturno:.2f}")
    st.write(f"⏱️ Horas Extras 50%: R$ {adicional_50:.2f}")
    st.write(f"⏱️ Horas Extras 100%: R$ {adicional_100:.2f}")
    st.success(f"💰 Total de Adicionais: R$ {total_adicionais:.2f}")
