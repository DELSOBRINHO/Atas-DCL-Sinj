#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

# Agrupar por DCL
dcls = {}
for ata in atas:
    dcl = ata['dcl_original']
    if dcl not in dcls:
        dcls[dcl] = []
    dcls[dcl].append(ata)

# Atas faltantes
faltantes_ordinarias = [37, 39, 41, 50, 57, 60, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 97, 99, 112, 113, 114, 115, 116, 117]

print("\n" + "="*70)
print("PROCURA DE ATAS FALTANTES POR DCL")
print("="*70 + "\n")

# Para cada DCL, mostrar as atas ordinárias
for dcl in sorted(dcls.keys()):
    atas_dcl = sorted([a for a in dcls[dcl] if a['tipo_sessao'] == 'ORDINÁRIA'], key=lambda x: int(x['sessao_num']))
    
    if atas_dcl:
        atas_neste_dcl = [int(a['sessao_num']) for a in atas_dcl]
        
        # Verificar se há atas faltantes neste intervalo
        if len(atas_neste_dcl) > 1:
            min_ata = min(atas_neste_dcl)
            max_ata = max(atas_neste_dcl)
            faltantes_neste_dcl = [n for n in faltantes_ordinarias if n >= min_ata and n <= max_ata]
            
            if faltantes_neste_dcl:
                print(f"{dcl}:")
                print(f"  Atas ordinárias: {atas_neste_dcl}")
                print(f"  ⚠️  Atas faltantes neste intervalo: {faltantes_neste_dcl}")
                print()

print(f"{'='*70}\n")

