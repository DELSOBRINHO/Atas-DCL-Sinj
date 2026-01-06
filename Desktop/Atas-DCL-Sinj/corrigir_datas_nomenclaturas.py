#!/usr/bin/env python3
import json
from pathlib import Path
import re

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

print("CORRIGIR DATAS NAS NOMENCLATURAS")
print("="*70)

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

corrigidas = 0

for ata in atas:
    sessao_num = ata['sessao_num']
    tipo_sessao = ata['tipo_sessao']
    data_real = ata['data_real']
    nomenclatura = ata['nomenclatura']
    
    # Extrair data_real (formato: D/MM/YYYY ou DD/MM/YYYY)
    match_data = re.match(r'(\d{1,2})/(\d{2})/(\d{4})', data_real)
    if match_data:
        dia, mes, ano = match_data.groups()
        dia = dia.zfill(2)  # Adicionar zero à esquerda se necessário
        
        # Determinar código de tipo
        codigo_tipo = '1' if tipo_sessao == 'ORDINÁRIA' else '2'
        abrev_tipo = 'SO' if tipo_sessao == 'ORDINÁRIA' else 'SE'
        
        # Construir nomenclatura correta
        nomenclatura_correta = f"{ano}-{mes}-{dia}-{codigo_tipo}-{abrev_tipo}-{sessao_num}-2-AC.pdf"
        
        # Se diferente, corrigir
        if nomenclatura != nomenclatura_correta:
            print(f"\n{sessao_num} ({data_real}): {nomenclatura}")
            print(f"  -> {nomenclatura_correta}")
            ata['nomenclatura'] = nomenclatura_correta
            corrigidas += 1

# Ordenar por sessão_num
atas_sorted = sorted(atas, key=lambda x: int(x['sessao_num']))

# Salvar JSON
with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
    json.dump(atas_sorted, f, ensure_ascii=False, indent=2)

print(f"\n{'='*70}")
print(f"Total corrigidas: {corrigidas}")
print(f"Total de atas: {len(atas_sorted)}")
print(f"{'='*70}")

