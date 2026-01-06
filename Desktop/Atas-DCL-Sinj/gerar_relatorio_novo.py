#!/usr/bin/env python3
import json
import csv
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")
ARQUIVO_CSV = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/relatorio_112_atas.csv")

print("\n" + "="*70)
print("GERAR RELATÓRIO COM 112 ATAS")
print("="*70)

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print(f"\nTotal de atas: {len(atas)}")

# Gerar CSV com encoding UTF-8-SIG (BOM)
with open(ARQUIVO_CSV, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f, delimiter=';')
    
    # Cabeçalho
    writer.writerow([
        'Sessao',
        'Tipo',
        'Data',
        'Pag_Inicio',
        'Pag_Fim',
        'DCL_Original',
        'Nomenclatura'
    ])
    
    # Dados
    for ata in atas:
        writer.writerow([
            ata['sessao_num'],
            ata['tipo_sessao'],
            ata['data_real'],
            ata['pag_inicio'],
            ata['pag_fim'],
            ata['dcl_original'],
            ata['nomenclatura']
        ])

print(f"✅ Relatório gerado: {ARQUIVO_CSV.name}")
print(f"\n" + "="*70)

