import tkinter as tk
from tkinter import messagebox

def analisar_cliente():
    nome = entry_nome.get()
    idade = int(entry_idade.get())
    renda = float(entry_renda.get())
    profissao = entry_profissao.get().lower()

    resultado = f"\n📄 Ficha do Cliente\nNome: {nome}\nIdade: {idade} anos\nRenda: R$ {renda:.2f}\nProfissão: {profissao.capitalize()}\n\n🔎 Análise:\n"

    # Regra 1 – Benefício por renda
    if renda < 2000:
        resultado += "✅ Pode ter direito ao benefício por baixa renda.\n"
    else:
        resultado += "❌ Não se enquadra no critério de renda.\n"

    # Regra 2 – Idoso
    if idade >= 60:
        resultado += "👵 Cliente é considerado idoso.\n"
    else:
        resultado += "🧒 Cliente não é idoso.\n"

    # Regra 3 – Situação crítica
    if profissao == "desempregado":
        resultado += "🚨 Situação crítica detectada!\n"
    else:
        resultado += "🧑 Cliente possui emprego.\n"

    messagebox.showinfo("Resultado da Análise", resultado)

# Criar janela
janela = tk.Tk()
janela.title("Analisador de Cliente")

# Labels e entradas
tk.Label(janela, text="Nome do cliente:").grid(row=0, column=0, sticky="w")
entry_nome = tk.Entry(janela, width=30)
entry_nome.grid(row=0, column=1)

tk.Label(janela, text="Idade:").grid(row=1, column=0, sticky="w")
entry_idade = tk.Entry(janela)
entry_idade.grid(row=1, column=1)

tk.Label(janela, text="Renda mensal (R$):").grid(row=2, column=0, sticky="w")
entry_renda = tk.Entry(janela)
entry_renda.grid(row=2, column=1)

tk.Label(janela, text="Profissão:").grid(row=3, column=0, sticky="w")
entry_profissao = tk.Entry(janela)
entry_profissao.grid(row=3, column=1)

# Botão
btn_analisar = tk.Button(janela, text="Analisar", command=analisar_cliente)
btn_analisar.grid(row=4, column=0, columnspan=2, pady=10)

# Rodar
janela.mainloop()
