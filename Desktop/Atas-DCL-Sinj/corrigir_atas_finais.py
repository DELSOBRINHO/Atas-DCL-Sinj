#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

print("\n" + "="*70)
print("CORRIGIR ATAS FINAIS")
print("="*70)

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print(f"\nTotal de atas antes: {len(atas)}")

# Remover a 68ª ordinária duplicada (2/10/2007) com páginas invertidas
atas_para_remover = []
for i, ata in enumerate(atas):
    if (ata['sessao_num'] == '068' and ata['tipo_sessao'] == 'ORDINÁRIA' and 
        ata['data_real'] == '2/10/2007'):
        atas_para_remover.append(i)
        print(f"\n🗑️  Removida ATA 68ª ORDINÁRIA (2/10/2007) - páginas invertidas")

# Remover em ordem reversa
for i in sorted(atas_para_remover, reverse=True):
    atas.pop(i)

# Agrupar atas por DCL e ordenar por página inicial
dcls = {}
for ata in atas:
    dcl = ata['dcl_original']
    if dcl not in dcls:
        dcls[dcl] = []
    dcls[dcl].append(ata)

for dcl in dcls:
    dcls[dcl] = sorted(dcls[dcl], key=lambda x: x['pag_inicio'])

# Corrigir páginas finais das atas 61-70, 104, 108-109
atas_para_corrigir = [61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 104, 108, 109]

corrigidas = 0
for ata in atas:
    sessao_num = int(ata['sessao_num'])
    if sessao_num in atas_para_corrigir and ata['tipo_sessao'] == 'ORDINÁRIA':
        dcl = ata['dcl_original']
        atas_dcl = dcls[dcl]
        
        try:
            idx = atas_dcl.index(ata)
            if idx + 1 < len(atas_dcl):
                proxima_ata = atas_dcl[idx + 1]
                pag_fim_novo = proxima_ata['pag_inicio'] - 1
                
                if pag_fim_novo != ata['pag_fim']:
                    print(f"\n✏️  Corrigida ATA {sessao_num:3d} ORDINÁRIA")
                    print(f"   Página final: {ata['pag_fim']} → {pag_fim_novo}")
                    ata['pag_fim'] = pag_fim_novo
                    corrigidas += 1
        except ValueError:
            pass

# Salvar JSON
with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
    json.dump(atas, f, ensure_ascii=False, indent=2)

print(f"\n{'='*70}")
print(f"Total de atas removidas: {len(atas_para_remover)}")
print(f"Total de atas corrigidas: {corrigidas}")
print(f"Total de atas depois: {len(atas)}")
print(f"{'='*70}\n")

