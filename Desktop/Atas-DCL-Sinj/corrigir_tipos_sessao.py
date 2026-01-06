#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

print("CORRIGIR TIPOS DE SESSÃO")

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

# Mapeamento de correções de tipo
correcoes_tipo = {
    '008': 'EXTRAORDINÁRIA',
    '018': 'EXTRAORDINÁRIA',
    '022': 'EXTRAORDINÁRIA',
}

corrigidas = 0

for sessao_num, tipo_correto in correcoes_tipo.items():
    for ata in atas:
        if ata['sessao_num'] == sessao_num:
            if ata['tipo_sessao'] != tipo_correto:
                print(f"\n{sessao_num}: {ata['tipo_sessao']} -> {tipo_correto}")
                ata['tipo_sessao'] = tipo_correto
                
                # Atualizar nomenclatura também
                codigo_tipo = '2' if tipo_correto == 'EXTRAORDINÁRIA' else '1'
                abrev_tipo = 'SE' if tipo_correto == 'EXTRAORDINÁRIA' else 'SO'
                
                # Extrair data da nomenclatura
                nomen = ata['nomenclatura']
                partes = nomen.split('-')
                if len(partes) >= 3:
                    ano, mes, dia = partes[0], partes[1], partes[2]
                    nomenclatura_correta = f"{ano}-{mes}-{dia}-{codigo_tipo}-{abrev_tipo}-{sessao_num}-2-AC.pdf"
                    print(f"  Nomenclatura: {nomen} -> {nomenclatura_correta}")
                    ata['nomenclatura'] = nomenclatura_correta
                    corrigidas += 1
            break

# Ordenar por sessão_num
atas_sorted = sorted(atas, key=lambda x: int(x['sessao_num']))

# Salvar JSON
with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
    json.dump(atas_sorted, f, ensure_ascii=False, indent=2)

print(f"\nTotal corrigidas: {corrigidas}")
print(f"Total de atas: {len(atas_sorted)}")

