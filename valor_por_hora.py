# valor_por_hora.py

# Solicita o valor total recebido
valor_total = float(input("Digite o valor total recebido (ex: 1000.00): R$ "))

# Solicita a carga horária total
carga_horaria = float(input("Digite a carga horária total (ex: 220): "))

# Calcula o valor por hora
valor_hora = valor_total / carga_horaria

# Exibe o resultado
print(f"\nVocê recebe R$ {valor_hora:.2f} por hora trabalhada.")

