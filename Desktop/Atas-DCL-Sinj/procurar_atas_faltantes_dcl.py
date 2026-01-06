#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

print("\n" + "="*70)
print("PROCURAR ATAS FALTANTES NOS DCLs")
print("="*70)

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

# Extrair DCLs únicos
dcls = {}
for ata in atas:
    dcl = ata['dcl_original']
    if dcl not in dcls:
        dcls[dcl] = []
    dcls[dcl].append({
        'sessao_num': int(ata['sessao_num']),
        'tipo': ata['tipo_sessao'],
        'data': ata['data_real'],
        'pag_inicio': ata['pag_inicio'],
        'pag_fim': ata['pag_fim']
    })

print(f"\nTotal de DCLs: {len(dcls)}")
print(f"Total de atas: {len(atas)}")

# Atas faltantes
faltantes_ordinarias = [5, 8, 9, 22, 37, 39, 41, 50, 57, 60, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 97, 99, 112, 113, 114, 115, 116, 117]
faltantes_extraordinarias = [1, 4, 11, 12, 15, 19, 20, 26, 31, 32, 33, 34, 35, 36, 37, 38]

print(f"\nAtas ordinárias faltando: {len(faltantes_ordinarias)}")
print(f"Atas extraordinárias faltando: {len(faltantes_extraordinarias)}")

# Analisar DCLs para encontrar gaps
print(f"\n{'='*70}")
print("ANÁLISE DE GAPS NOS DCLs:")
print(f"{'='*70}\n")

for dcl in sorted(dcls.keys()):
    atas_dcl = sorted(dcls[dcl], key=lambda x: x['pag_inicio'])
    print(f"\n{dcl}:")
    print(f"  Total de atas: {len(atas_dcl)}")
    
    # Verificar gaps entre páginas
    for i in range(len(atas_dcl) - 1):
        ata_atual = atas_dcl[i]
        ata_proxima = atas_dcl[i + 1]
        
        gap = ata_proxima['pag_inicio'] - ata_atual['pag_fim']
        if gap > 1:
            print(f"  ⚠️  GAP entre pág {ata_atual['pag_fim']} e {ata_proxima['pag_inicio']} (gap: {gap})")
            print(f"      Ata {ata_atual['sessao_num']:3d} ({ata_atual['tipo'][:3]}) termina em {ata_atual['pag_fim']}")
            print(f"      Ata {ata_proxima['sessao_num']:3d} ({ata_proxima['tipo'][:3]}) começa em {ata_proxima['pag_inicio']}")

print(f"\n{'='*70}\n")

