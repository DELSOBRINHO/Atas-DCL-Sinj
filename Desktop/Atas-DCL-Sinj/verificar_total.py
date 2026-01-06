#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print(f"Total de atas: {len(atas)}")
print(f"Primeira ata: {atas[0]['sessao_num']}")
print(f"Ultima ata: {atas[-1]['sessao_num']}")

# Verificar se há 111 atas
if len(atas) == 111:
    print("✅ Arquivo tem 111 atas")
elif len(atas) == 106:
    print("❌ Arquivo foi revertido para 106 atas")
else:
    print(f"⚠️ Arquivo tem {len(atas)} atas")

