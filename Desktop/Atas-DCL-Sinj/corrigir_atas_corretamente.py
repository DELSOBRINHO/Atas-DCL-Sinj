#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

print("\n" + "="*70)
print("CORRIGIR ATAS - VERSÃO CORRETA")
print("="*70)

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print(f"\nTotal de atas antes: {len(atas)}")

# Correções específicas baseadas nas informações do usuário
# 1. ATA 101: página final deve ser 8 (não 22)
# 2. ATA 104: página final deve ser 42 (próxima é 105 na página 43)
# 3. ATA 105: página final deve ser 54 (próxima é 106 na página 54)
# 4. ATA 106: página final deve ser 54 (última do DCL)
# 5. ATA 107: deve ir de página 1 até 6 do DCL_2007-01-236.pdf
# 6. ATA 110: deve ir de página 23 até 30 do DCL_2007-01-236.pdf
# 7. ATA 111: deve ir até página 34
# 8. ATA 16 EXTRAORDINÁRIA: deve ir até página 22
# 9. ATA 17 EXTRAORDINÁRIA: deve ir até página 24
# 10. ATA 68 (21/08/2007): é a correta, remover as outras
# 11. ATA 68 (20/11/2007): remover (duplicada)
# 12. ATA 68 (02/10/2007): remover (é na verdade a 86ª)

correcoes = [
    # (sessao_num, tipo, data, pag_inicio, pag_fim, dcl)
    ("101", "ORDINÁRIA", "06/11/2007", 2, 8, "DCL_2007-01-235.pdf"),
    ("104", "ORDINÁRIA", "13/11/2007", 37, 42, "DCL_2007-01-235.pdf"),
    ("105", "ORDINÁRIA", "14/11/2007", 43, 54, "DCL_2007-01-235.pdf"),
    ("106", "ORDINÁRIA", "20/11/2007", 54, 54, "DCL_2007-01-235.pdf"),
    ("107", "ORDINÁRIA", "21/10/2007", 1, 6, "DCL_2007-01-236.pdf"),
    ("110", "ORDINÁRIA", "28/11/2007", 23, 30, "DCL_2007-01-236.pdf"),
    ("111", "ORDINÁRIA", "29/11/2007", 31, 34, "DCL_2007-01-236.pdf"),
    ("016", "EXTRAORDINÁRIA", "12/09/2007", 20, 22, "DCL_2007-10-1766369225.pdf"),
    ("017", "EXTRAORDINÁRIA", "13/09/2007", 22, 24, "DCL_2007-10-1766369225.pdf"),
]

# Remover atas duplicadas/incorretas
atas_para_remover = []
for i, ata in enumerate(atas):
    # Remover 68ª ordinária (20/11/2007) - duplicada
    if (ata['sessao_num'] == '068' and ata['tipo_sessao'] == 'ORDINÁRIA' and 
        ata['data_real'] == '20/11/2007'):
        atas_para_remover.append(i)
    # Remover 68ª ordinária (02/10/2007) - é na verdade a 86ª
    elif (ata['sessao_num'] == '068' and ata['tipo_sessao'] == 'ORDINÁRIA' and 
          ata['data_real'] == '02/10/2007'):
        atas_para_remover.append(i)

# Remover em ordem reversa
for i in sorted(atas_para_remover, reverse=True):
    print(f"\n🗑️  Removida ATA {atas[i]['sessao_num']} {atas[i]['tipo_sessao']} ({atas[i]['data_real']})")
    atas.pop(i)

# Aplicar correções
corrigidas = 0
for sessao_num, tipo, data, pag_inicio, pag_fim, dcl in correcoes:
    # Encontrar e atualizar
    encontrada = False
    for ata in atas:
        if ata['sessao_num'] == sessao_num and ata['tipo_sessao'] == tipo:
            if ata['data_real'] == data:
                if (ata['pag_inicio'] != pag_inicio or ata['pag_fim'] != pag_fim or 
                    ata['dcl_original'] != dcl):
                    print(f"\n✏️  Corrigida ATA {sessao_num} {tipo} ({data})")
                    print(f"   Páginas: {ata['pag_inicio']}-{ata['pag_fim']} → {pag_inicio}-{pag_fim}")
                    print(f"   DCL: {ata['dcl_original']} → {dcl}")
                    ata['pag_inicio'] = pag_inicio
                    ata['pag_fim'] = pag_fim
                    ata['dcl_original'] = dcl
                    corrigidas += 1
                encontrada = True
                break
    
    if not encontrada:
        print(f"\n⚠️  ATA {sessao_num} {tipo} ({data}) não encontrada!")

# Salvar JSON
with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
    json.dump(atas, f, ensure_ascii=False, indent=2)

print(f"\n{'='*70}")
print(f"Total de atas removidas: {len(atas_para_remover)}")
print(f"Total de atas corrigidas: {corrigidas}")
print(f"Total de atas depois: {len(atas)}")
print(f"{'='*70}\n")

