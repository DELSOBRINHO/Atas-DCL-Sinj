#!/usr/bin/env python3
import json
from pathlib import Path
import shutil

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")
ARQUIVO_BACKUP = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final_BACKUP.json")

print("\n" + "="*70)
print("RESTAURAR 111 ATAS")
print("="*70)

# Carregar backup
with open(ARQUIVO_BACKUP, 'r', encoding='utf-8') as f:
    atas_backup = json.load(f)

print(f"\nAtas no backup: {len(atas_backup)}")

# Restaurar
shutil.copy(ARQUIVO_BACKUP, ARQUIVO_JSON)

print(f"✅ Arquivo restaurado com sucesso!")

# Verificar
with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print(f"Atas no arquivo principal: {len(atas)}")

print(f"\n" + "="*70)

