
import subprocess

scripts = [
    "scripts/01_extrair_usuarios_sp.py",
    "scripts/02_extrair_definicoes.py",
    "scripts/03_match_atributos.py",
    "scripts/04_aplicar_atributos.py"
]

print("Iniciando pipeline \n")

for script in scripts:
    print(f"\n[+] Executando: {script}")
    subprocess.run(["python", script], check=True)

print("\n Pipeline concluída com sucesso.")
