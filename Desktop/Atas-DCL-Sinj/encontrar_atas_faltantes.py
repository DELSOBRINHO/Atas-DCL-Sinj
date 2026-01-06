#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

print("\n" + "="*80)
print("ENCONTRAR ATAS CIRCUNSTANCIADAS FALTANTES")
print("="*80)

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas_circunstanciadas = json.load(f)

# Lista de todas as atas sucintas do site (extraída manualmente)
atas_sucintas = {
    # EXTRAORDINÁRIAS
    1: "1ª Sessão Extraordinária",
    2: "2ª Sessão Extraordinária",
    3: "3ª Sessão Extraordinária",
    4: "4ª Sessão Extraordinária",
    5: "5ª Sessão Extraordinária",
    6: "6ª Sessão Extraordinária",
    7: "7ª Sessão Extraordinária",
    8: "8ª Sessão Extraordinária",
    9: "9ª Sessão Extraordinária",
    10: "10ª Sessão Extraordinária",
    11: "11ª Sessão Extraordinária",
    12: "12ª Sessão Extraordinária",
    13: "13ª Sessão Extraordinária",
    14: "14ª Sessão Extraordinária",
    15: "15ª Sessão Extraordinária",
    16: "16ª Sessão Extraordinária",
    17: "17ª Sessão Extraordinária",
    18: "18ª Sessão Extraordinária",
    19: "19ª Sessão Extraordinária",
    20: "20ª Sessão Extraordinária",
    21: "21ª Sessão Extraordinária",
    22: "22ª Sessão Extraordinária",
    23: "23ª Sessão Extraordinária",
    24: "24ª Sessão Extraordinária",
    25: "25ª Sessão Extraordinária",
    26: "26ª Sessão Extraordinária",
    27: "27ª Sessão Extraordinária",
    28: "28ª Sessão Extraordinária",
    29: "29ª Sessão Extraordinária",
    30: "30ª Sessão Extraordinária",
    31: "31ª Sessão Extraordinária",
    32: "32ª Sessão Extraordinária",
    33: "33ª Sessão Extraordinária",
    34: "34ª Sessão Extraordinária",
    35: "35ª Sessão Extraordinária",
    36: "36ª Sessão Extraordinária",
    37: "37ª Sessão Extraordinária",
    38: "38ª Sessão Extraordinária",
}

# ORDINÁRIAS (1-117)
for i in range(1, 118):
    atas_sucintas[100 + i] = f"{i}ª Sessão Ordinária"

# Extrair números de atas circunstanciadas que temos
atas_circunstanciadas_nums = set()
for ata in atas_circunstanciadas:
    sessao_num = int(ata['sessao_num'])
    tipo = ata['tipo_sessao']
    
    if tipo == 'EXTRAORDINÁRIA':
        atas_circunstanciadas_nums.add(sessao_num)
    else:  # ORDINÁRIA
        atas_circunstanciadas_nums.add(100 + sessao_num)

# Encontrar faltantes
print(f"\nTotal de atas sucintas: {len(atas_sucintas)}")
print(f"Total de atas circunstanciadas: {len(atas_circunstanciadas)}")

faltantes = []
for num, nome in sorted(atas_sucintas.items()):
    if num not in atas_circunstanciadas_nums:
        faltantes.append((num, nome))

print(f"\n{'='*80}")
print(f"ATAS CIRCUNSTANCIADAS FALTANTES: {len(faltantes)}")
print(f"{'='*80}\n")

for num, nome in faltantes:
    print(f"  • {nome}")

# Salvar em arquivo
with open(Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/atas_faltantes.txt"), 'w', encoding='utf-8') as f:
    f.write("ATAS CIRCUNSTANCIADAS FALTANTES\n")
    f.write("="*80 + "\n\n")
    f.write(f"Total: {len(faltantes)}\n\n")
    for num, nome in faltantes:
        f.write(f"{nome}\n")

print(f"\n{'='*80}")
print(f"Relatório salvo em: atas_faltantes.txt")
print(f"{'='*80}\n")

