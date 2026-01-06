#!/usr/bin/env python3
import json
from pathlib import Path
import re

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

print("CORRIGIR TODAS AS NOMENCLATURAS")

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print(f"Total de atas: {len(atas)}")

corrigidas = 0

for ata in atas:
    sessao_num = ata['sessao_num']
    tipo_sessao = ata['tipo_sessao']
    data_real = ata['data_real']
    nomenclatura = ata['nomenclatura']
    
    # Determinar código de tipo (1=Ordinária, 2=Extraordinária)
    codigo_tipo = '1' if tipo_sessao == 'ORDINÁRIA' else '2'
    
    # Determinar abreviação (SO=Ordinária, SE=Extraordinária)
    abrev_tipo = 'SO' if tipo_sessao == 'ORDINÁRIA' else 'SE'
    
    # Extrair data da nomenclatura
    match = re.match(r'(\d{4})-(\d{2})-(\d{2})', nomenclatura)
    if match:
        ano, mes, dia = match.groups()
        
        # Construir nomenclatura correta
        nomenclatura_correta = f"{ano}-{mes}-{dia}-{codigo_tipo}-{abrev_tipo}-{sessao_num}-2-AC.pdf"
        
        # Se diferente, corrigir
        if nomenclatura != nomenclatura_correta:
            print(f"\n{sessao_num}: {nomenclatura} -> {nomenclatura_correta}")
            ata['nomenclatura'] = nomenclatura_correta
            corrigidas += 1

# Ordenar por sessão_num
atas_sorted = sorted(atas, key=lambda x: int(x['sessao_num']))

# Salvar JSON
with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
    json.dump(atas_sorted, f, ensure_ascii=False, indent=2)

print(f"\nTotal corrigidas: {corrigidas}")
print(f"Total de atas: {len(atas_sorted)}")

