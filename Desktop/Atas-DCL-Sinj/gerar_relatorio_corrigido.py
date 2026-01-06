#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GERAR RELATÓRIO CORRIGIDO
==========================
"""

import json
import pandas as pd
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")
ARQUIVO_EXCEL = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/relatorio_validacao_111_atas_FINAL.xlsx")

print("\n" + "="*70)
print("GERAR RELATÓRIO CORRIGIDO")
print("="*70)

# Carregar JSON
with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print(f"\nTotal de atas: {len(atas)}")

# Criar DataFrame
dados = []
for i, ata in enumerate(atas, 1):
    dados.append({
        'Nº': i,
        'Sessão': f"{ata['sessao_num']}ª {ata['tipo_sessao']}",
        'Tipo Sessão': ata['tipo_sessao'],
        'Data': ata['data_real'],
        'Pág. Inicial': ata['pag_inicio'],
        'Pág. Final': ata['pag_fim'],
        'DCL Original': ata['dcl_original'],
        'Nomenclatura': ata['nomenclatura'],
        'Validado': '',
        'Observações': ''
    })

df = pd.DataFrame(dados)

# Salvar Excel
try:
    df.to_excel(ARQUIVO_EXCEL, index=False, engine='openpyxl')
    print(f"\n✅ Relatório gerado: {ARQUIVO_EXCEL.name}")
except Exception as e:
    print(f"\n❌ Erro ao gerar Excel: {e}")
    # Tentar com CSV
    ARQUIVO_CSV = ARQUIVO_EXCEL.with_suffix('.csv')
    df.to_csv(ARQUIVO_CSV, index=False, encoding='utf-8')
    print(f"✅ Relatório gerado em CSV: {ARQUIVO_CSV.name}")

print("="*70)

