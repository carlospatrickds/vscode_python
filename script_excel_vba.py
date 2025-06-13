import os
import zipfile
import shutil

def desbloquear_vba(path_arquivo_xlsm, destino):
    if not zipfile.is_zipfile(path_arquivo_xlsm):
        print("❌ O arquivo não parece ser um .xlsm válido.")
        return

    # Criar uma cópia temporária
    temp_dir = "xlsm_temp"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    with zipfile.ZipFile(path_arquivo_xlsm, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    vba_path = os.path.join(temp_dir, "xl", "vbaProject.bin")
    if not os.path.exists(vba_path):
        print("❌ Nenhum projeto VBA encontrado no arquivo.")
        return

    # Lê o conteúdo binário
    with open(vba_path, "rb") as file:
        content = file.read()

    # Remove os bytes típicos da proteção de senha
    patched = content.replace(b'DPB=', b'DPx=')

    # Salva o conteúdo editado
    with open(vba_path, "wb") as file:
        file.write(patched)

    # Cria novo arquivo desbloqueado
    novo_arquivo = os.path.join(destino, "arquivo_desbloqueado.xlsm")
    with zipfile.ZipFile(novo_arquivo, 'w', zipfile.ZIP_DEFLATED) as new_zip:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zip_name = os.path.relpath(file_path, temp_dir)
                new_zip.write(file_path, zip_name)

    # Limpeza
    shutil.rmtree(temp_dir)
    print(f"✅ Projeto VBA desbloqueado com sucesso! Salvo como: {novo_arquivo}")

# Caminho do arquivo original e pasta de destino
arquivo = "protegido.xlsm"
destino_saida = "."

desbloquear_vba(arquivo, destino_saida)
