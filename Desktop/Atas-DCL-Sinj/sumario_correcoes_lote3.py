#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print("\n" + "="*70)
print("SUMÁRIO FINAL - LOTE 3 (CORREÇÕES)")
print("="*70)

print(f"\n📊 TOTAL DE ATAS NO JSON: {len(atas)}")

# Contar ordinárias e extraordinárias
ordinárias = [a for a in atas if a['tipo_sessao'] == 'ORDINÁRIA']
extraordinárias = [a for a in atas if a['tipo_sessao'] == 'EXTRAORDINÁRIA']

print(f"\n   Atas Ordinárias: {len(ordinárias)}")
print(f"   Atas Extraordinárias: {len(extraordinárias)}")

# Verificar atas faltando
atas_ord_nums = set(int(a['sessao_num']) for a in ordinárias)
atas_ext_nums = set(int(a['sessao_num']) for a in extraordinárias)

print(f"\n✅ CORREÇÕES REALIZADAS:")
print(f"   • Removida ATA 68ª ORDINÁRIA (2/10/2007) - páginas invertidas")
print(f"   • Removida ATA 011 ORDINÁRIA (28/11/2007) - duplicada")
print(f"   • Corrigida ATA 101ª ORDINÁRIA - página final: 22 → 8")
print(f"   • Corrigida ATA 104ª ORDINÁRIA - página final: 42 (confirmada)")
print(f"   • Corrigida ATA 105ª ORDINÁRIA - página final: 43 → 54")
print(f"   • Corrigida ATA 106ª ORDINÁRIA - página final: 54 (confirmada)")
print(f"   • Corrigida ATA 107ª ORDINÁRIA - página final: 6 (confirmada)")
print(f"   • Corrigida ATA 110ª ORDINÁRIA - página final: 30 (confirmada)")
print(f"   • Corrigida ATA 111ª ORDINÁRIA - página final: 34 (confirmada)")
print(f"   • Corrigida ATA 016ª EXTRAORDINÁRIA - página final: 22 (confirmada)")
print(f"   • Corrigida ATA 017ª EXTRAORDINÁRIA - página final: 24 (confirmada)")

print(f"\n{'='*70}\n")

