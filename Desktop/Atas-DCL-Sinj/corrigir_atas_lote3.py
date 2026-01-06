#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

print("\n" + "="*70)
print("CORRIGIR ATAS - LOTE 3")
print("="*70)

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print(f"\nTotal de atas antes: {len(atas)}")

# Criar dicionário para acesso rápido
atas_dict = {(a['sessao_num'], a['tipo_sessao']): a for a in atas}

# Correções a fazer
correcoes = [
    # (sessao_num, tipo, pag_fim_novo)
    ("101", "ORDINÁRIA", 8),
    ("104", "ORDINÁRIA", 42),
    ("105", "ORDINÁRIA", 43),
    ("106", "ORDINÁRIA", 54),
    ("107", "ORDINÁRIA", 6),
    ("110", "ORDINÁRIA", 30),
    ("111", "ORDINÁRIA", 34),
    ("016", "EXTRAORDINÁRIA", 22),
    ("017", "EXTRAORDINÁRIA", 24),
    # Atas ordinárias que precisam de correção de página final
    ("061", "ORDINÁRIA", None),  # Será corrigido pela próxima
    ("062", "ORDINÁRIA", None),
    ("063", "ORDINÁRIA", None),
    ("064", "ORDINÁRIA", None),
    ("065", "ORDINÁRIA", None),
    ("066", "ORDINÁRIA", None),
    ("067", "ORDINÁRIA", None),
    ("068", "ORDINÁRIA", None),
    ("069", "ORDINÁRIA", None),
    ("070", "ORDINÁRIA", None),
    ("108", "ORDINÁRIA", None),
    ("109", "ORDINÁRIA", None),
]

# Remover a 68ª ordinária duplicada (20/11/2007)
atas_para_remover = []
for i, ata in enumerate(atas):
    if (ata['sessao_num'] == '068' and ata['tipo_sessao'] == 'ORDINÁRIA' and 
        ata['data_real'] == '20/11/2007'):
        atas_para_remover.append(i)

# Remover em ordem reversa para não afetar índices
for i in sorted(atas_para_remover, reverse=True):
    print(f"\n🗑️  Removida ATA 68ª ORDINÁRIA (20/11/2007)")
    atas.pop(i)

# Aplicar correções
corrigidas = 0
for sessao_num, tipo, pag_fim_novo in correcoes:
    chave = (sessao_num, tipo)
    if chave in atas_dict:
        ata = atas_dict[chave]
        if pag_fim_novo is not None:
            ata['pag_fim'] = pag_fim_novo
            print(f"\n✏️  Corrigida ATA {sessao_num} {tipo}")
            print(f"   Página final: {pag_fim_novo}")
            corrigidas += 1

# Ordenar por sessão_num
atas_sorted = sorted(atas, key=lambda x: int(x['sessao_num']))

# Salvar JSON
with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
    json.dump(atas_sorted, f, ensure_ascii=False, indent=2)

print(f"\n{'='*70}")
print(f"Total de atas corrigidas: {corrigidas}")
print(f"Total de atas removidas: {len(atas_para_remover)}")
print(f"Total de atas depois: {len(atas_sorted)}")
print(f"{'='*70}\n")

