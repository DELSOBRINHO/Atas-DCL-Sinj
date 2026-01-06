#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print("\n" + "="*70)
print("CORRIGIR 024ª PARA 095ª (23/10/2007)")
print("="*70)

# Procurar e corrigir
encontrada = False
for ata in atas:
    if (ata['sessao_num'] == '024' and 
        ata['data_real'] == '23/10/2007' and
        'DCL_2007-01-231' in ata['dcl_original']):
        
        print(f"\n✅ Encontrada ata para correção:")
        print(f"   Sessão: {ata['sessao_num']}ª")
        print(f"   Data: {ata['data_real']}")
        print(f"   DCL: {ata['dcl_original']}")
        print(f"   Nomenclatura atual: {ata['nomenclatura']}")
        
        # Corrigir
        ata['sessao_num'] = '095'
        ata['nomenclatura'] = '2007-10-23-1-SO-095-2-AC.pdf'
        
        print(f"\n✅ Corrigida para:")
        print(f"   Sessão: {ata['sessao_num']}ª")
        print(f"   Nomenclatura nova: {ata['nomenclatura']}")
        
        encontrada = True
        break

if encontrada:
    # Ordenar por sessão_num
    atas_sorted = sorted(atas, key=lambda x: int(x['sessao_num']))
    
    # Salvar JSON
    with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
        json.dump(atas_sorted, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ JSON atualizado com sucesso!")
else:
    print(f"\n❌ Ata não encontrada para correção")

print(f"\n" + "="*70)

