#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

print("\n" + "="*70)
print("PROCURAR ATAS NOS GAPS DOS DCLs")
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

# Atas faltantes
faltantes_ordinarias = [5, 8, 9, 22, 37, 39, 41, 50, 57, 60, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 97, 99, 112, 113, 114, 115, 116, 117]
faltantes_extraordinarias = [1, 4, 11, 12, 15, 19, 20, 26, 31, 32, 33, 34, 35, 36, 37, 38]

print(f"\nProcurando atas faltantes nos gaps dos DCLs...\n")

gaps_encontrados = []

for dcl in sorted(dcls.keys()):
    atas_dcl = sorted(dcls[dcl], key=lambda x: x['pag_inicio'])
    
    # Verificar gaps entre páginas
    for i in range(len(atas_dcl) - 1):
        ata_atual = atas_dcl[i]
        ata_proxima = atas_dcl[i + 1]
        
        gap = ata_proxima['pag_inicio'] - ata_atual['pag_fim']
        if gap > 1:
            gap_info = {
                'dcl': dcl,
                'pag_inicio': ata_atual['pag_fim'] + 1,
                'pag_fim': ata_proxima['pag_inicio'] - 1,
                'ata_anterior': ata_atual['sessao_num'],
                'ata_proxima': ata_proxima['sessao_num'],
                'gap_size': gap
            }
            gaps_encontrados.append(gap_info)
            
            print(f"GAP encontrado em {dcl}:")
            print(f"  Páginas: {gap_info['pag_inicio']}-{gap_info['pag_fim']} (tamanho: {gap_info['gap_size']})")
            print(f"  Entre ata {ata_atual['sessao_num']} e {ata_proxima['sessao_num']}")
            print()

print(f"\n{'='*70}")
print(f"Total de gaps encontrados: {len(gaps_encontrados)}")
print(f"{'='*70}\n")

# Salvar relatório
with open(Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/gaps_encontrados.txt"), 'w', encoding='utf-8') as f:
    f.write("GAPS ENCONTRADOS NOS DCLs\n")
    f.write("="*70 + "\n\n")
    for gap in gaps_encontrados:
        f.write(f"DCL: {gap['dcl']}\n")
        f.write(f"  Páginas: {gap['pag_inicio']}-{gap['pag_fim']} (tamanho: {gap['gap_size']})\n")
        f.write(f"  Entre ata {gap['ata_anterior']} e {gap['ata_proxima']}\n\n")

print("Relatório salvo em: gaps_encontrados.txt")

