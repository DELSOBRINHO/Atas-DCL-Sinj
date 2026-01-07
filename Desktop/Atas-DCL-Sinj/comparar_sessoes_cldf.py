#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compara as sessões do site da CLDF com as atas do JSON.
Identifica quais atas estão faltando.
"""

import json

# Lista oficial da CLDF (extraída do print do usuário)
# Formato: (data, numero_sessao, tipo)
SESSOES_CLDF = [
    # Extraordinárias
    ("15/12/2007", 38, "EXTRAORDINÁRIA"), ("14/12/2007", 37, "EXTRAORDINÁRIA"), ("14/12/2007", 36, "EXTRAORDINÁRIA"),
    ("13/12/2007", 35, "EXTRAORDINÁRIA"), ("12/12/2007", 34, "EXTRAORDINÁRIA"), ("11/12/2007", 33, "EXTRAORDINÁRIA"),
    ("05/12/2007", 32, "EXTRAORDINÁRIA"), ("04/12/2007", 31, "EXTRAORDINÁRIA"), ("29/11/2007", 30, "EXTRAORDINÁRIA"),
    ("28/11/2007", 29, "EXTRAORDINÁRIA"), ("27/11/2007", 28, "EXTRAORDINÁRIA"), ("13/11/2007", 27, "EXTRAORDINÁRIA"),
    ("31/10/2007", 26, "EXTRAORDINÁRIA"), ("25/10/2007", 25, "EXTRAORDINÁRIA"), ("23/10/2007", 24, "EXTRAORDINÁRIA"),
    ("18/10/2007", 23, "EXTRAORDINÁRIA"), ("17/10/2007", 22, "EXTRAORDINÁRIA"), ("02/10/2007", 21, "EXTRAORDINÁRIA"),
    ("27/09/2007", 20, "EXTRAORDINÁRIA"), ("19/09/2007", 19, "EXTRAORDINÁRIA"), ("18/09/2007", 18, "EXTRAORDINÁRIA"),
    ("13/09/2007", 17, "EXTRAORDINÁRIA"), ("12/09/2007", 16, "EXTRAORDINÁRIA"), ("11/09/2007", 15, "EXTRAORDINÁRIA"),
    ("29/06/2007", 14, "EXTRAORDINÁRIA"), ("29/06/2007", 13, "EXTRAORDINÁRIA"), ("27/06/2007", 12, "EXTRAORDINÁRIA"),
    ("19/06/2007", 11, "EXTRAORDINÁRIA"), ("13/06/2007", 10, "EXTRAORDINÁRIA"), ("06/06/2007", 9, "EXTRAORDINÁRIA"),
    ("16/05/2007", 8, "EXTRAORDINÁRIA"), ("16/05/2007", 7, "EXTRAORDINÁRIA"), ("10/05/2007", 6, "EXTRAORDINÁRIA"),
    ("09/05/2007", 5, "EXTRAORDINÁRIA"), ("03/05/2007", 4, "EXTRAORDINÁRIA"), ("02/05/2007", 3, "EXTRAORDINÁRIA"),
    ("02/05/2007", 2, "EXTRAORDINÁRIA"), ("04/04/2007", 1, "EXTRAORDINÁRIA"),
    # Ordinárias
    ("13/12/2007", 117, "ORDINÁRIA"), ("12/12/2007", 116, "ORDINÁRIA"), ("11/12/2007", 115, "ORDINÁRIA"),
    ("06/12/2007", 114, "ORDINÁRIA"), ("05/12/2007", 113, "ORDINÁRIA"), ("04/12/2007", 112, "ORDINÁRIA"),
    ("29/11/2007", 111, "ORDINÁRIA"), ("28/11/2007", 110, "ORDINÁRIA"), ("27/11/2007", 109, "ORDINÁRIA"),
    ("22/11/2007", 108, "ORDINÁRIA"), ("21/11/2007", 107, "ORDINÁRIA"), ("20/11/2007", 106, "ORDINÁRIA"),
    ("14/11/2007", 105, "ORDINÁRIA"), ("13/11/2007", 104, "ORDINÁRIA"), ("08/11/2007", 103, "ORDINÁRIA"),
    ("07/11/2007", 102, "ORDINÁRIA"), ("06/11/2007", 101, "ORDINÁRIA"), ("01/11/2007", 100, "ORDINÁRIA"),
    ("31/10/2007", 99, "ORDINÁRIA"), ("30/10/2007", 98, "ORDINÁRIA"), ("25/10/2007", 97, "ORDINÁRIA"),
    ("24/10/2007", 96, "ORDINÁRIA"), ("23/10/2007", 95, "ORDINÁRIA"), ("18/10/2007", 94, "ORDINÁRIA"),
    ("17/10/2007", 93, "ORDINÁRIA"), ("16/10/2007", 92, "ORDINÁRIA"), ("11/10/2007", 91, "ORDINÁRIA"),
    ("10/10/2007", 90, "ORDINÁRIA"), ("09/10/2007", 89, "ORDINÁRIA"), ("04/10/2007", 88, "ORDINÁRIA"),
    ("03/10/2007", 87, "ORDINÁRIA"), ("02/10/2007", 86, "ORDINÁRIA"), ("27/09/2007", 85, "ORDINÁRIA"),
    ("26/09/2007", 84, "ORDINÁRIA"), ("25/09/2007", 83, "ORDINÁRIA"), ("20/09/2007", 82, "ORDINÁRIA"),
    ("19/09/2007", 81, "ORDINÁRIA"), ("18/09/2007", 80, "ORDINÁRIA"), ("13/09/2007", 79, "ORDINÁRIA"),
    ("12/09/2007", 78, "ORDINÁRIA"), ("11/09/2007", 77, "ORDINÁRIA"), ("06/09/2007", 76, "ORDINÁRIA"),
    ("05/09/2007", 75, "ORDINÁRIA"), ("04/09/2007", 74, "ORDINÁRIA"), ("30/08/2007", 73, "ORDINÁRIA"),
    ("29/08/2007", 72, "ORDINÁRIA"), ("28/08/2007", 71, "ORDINÁRIA"), ("23/08/2007", 70, "ORDINÁRIA"),
    ("22/08/2007", 69, "ORDINÁRIA"), ("21/08/2007", 68, "ORDINÁRIA"), ("16/08/2007", 67, "ORDINÁRIA"),
    ("15/08/2007", 66, "ORDINÁRIA"), ("14/08/2007", 65, "ORDINÁRIA"), ("09/08/2007", 64, "ORDINÁRIA"),
    ("08/08/2007", 63, "ORDINÁRIA"), ("07/08/2007", 62, "ORDINÁRIA"), ("02/08/2007", 61, "ORDINÁRIA"),
    ("01/08/2007", 60, "ORDINÁRIA"), ("28/06/2007", 59, "ORDINÁRIA"), ("27/06/2007", 58, "ORDINÁRIA"),
    ("26/06/2007", 57, "ORDINÁRIA"), ("21/06/2007", 56, "ORDINÁRIA"), ("20/06/2007", 55, "ORDINÁRIA"),
    ("19/06/2007", 54, "ORDINÁRIA"), ("14/06/2007", 53, "ORDINÁRIA"), ("13/06/2007", 52, "ORDINÁRIA"),
    ("12/06/2007", 51, "ORDINÁRIA"), ("06/06/2007", 50, "ORDINÁRIA"), ("05/06/2007", 49, "ORDINÁRIA"),
    ("31/05/2007", 48, "ORDINÁRIA"), ("30/05/2007", 47, "ORDINÁRIA"), ("29/05/2007", 46, "ORDINÁRIA"),
    ("24/05/2007", 45, "ORDINÁRIA"), ("23/05/2007", 44, "ORDINÁRIA"), ("22/05/2007", 43, "ORDINÁRIA"),
    ("17/05/2007", 42, "ORDINÁRIA"), ("16/05/2007", 41, "ORDINÁRIA"), ("15/05/2007", 40, "ORDINÁRIA"),
    ("10/05/2007", 39, "ORDINÁRIA"), ("09/05/2007", 38, "ORDINÁRIA"), ("08/05/2007", 37, "ORDINÁRIA"),
    ("03/05/2007", 36, "ORDINÁRIA"), ("02/05/2007", 35, "ORDINÁRIA"), ("26/04/2007", 34, "ORDINÁRIA"),
    ("25/04/2007", 33, "ORDINÁRIA"), ("24/04/2007", 32, "ORDINÁRIA"), ("19/04/2007", 31, "ORDINÁRIA"),
    ("18/04/2007", 30, "ORDINÁRIA"), ("17/04/2007", 29, "ORDINÁRIA"), ("12/04/2007", 28, "ORDINÁRIA"),
    ("11/04/2007", 27, "ORDINÁRIA"), ("10/04/2007", 26, "ORDINÁRIA"), ("04/04/2007", 25, "ORDINÁRIA"),
    ("03/04/2007", 24, "ORDINÁRIA"), ("29/03/2007", 23, "ORDINÁRIA"), ("28/03/2007", 22, "ORDINÁRIA"),
    ("27/03/2007", 21, "ORDINÁRIA"), ("22/03/2007", 20, "ORDINÁRIA"), ("21/03/2007", 19, "ORDINÁRIA"),
    ("20/03/2007", 18, "ORDINÁRIA"), ("15/03/2007", 17, "ORDINÁRIA"), ("14/03/2007", 16, "ORDINÁRIA"),
    ("13/03/2007", 15, "ORDINÁRIA"), ("08/03/2007", 14, "ORDINÁRIA"), ("07/03/2007", 13, "ORDINÁRIA"),
    ("06/03/2007", 12, "ORDINÁRIA"), ("01/03/2007", 11, "ORDINÁRIA"), ("28/02/2007", 10, "ORDINÁRIA"),
    ("27/02/2007", 9, "ORDINÁRIA"), ("22/02/2007", 8, "ORDINÁRIA"), ("15/02/2007", 7, "ORDINÁRIA"),
    ("14/02/2007", 6, "ORDINÁRIA"), ("13/02/2007", 5, "ORDINÁRIA"), ("08/02/2007", 4, "ORDINÁRIA"),
    ("07/02/2007", 3, "ORDINÁRIA"), ("06/02/2007", 2, "ORDINÁRIA"), ("01/02/2007", 1, "ORDINÁRIA"),
]

# Carregar JSON atual
with open('fase2_atas_2007_final.json', 'r', encoding='utf-8') as f:
    atas = json.load(f)

# Criar set das atas existentes (numero, tipo)
atas_existentes = set()
for ata in atas:
    num = int(str(ata['sessao_num']))
    tipo = ata['tipo_sessao']
    atas_existentes.add((num, tipo))

print("=" * 80)
print("COMPARAÇÃO: CLDF vs JSON ATUAL")
print("=" * 80)

# Estatísticas
total_cldf = len(SESSOES_CLDF)
ord_cldf = len([s for s in SESSOES_CLDF if s[2] == "ORDINÁRIA"])
ext_cldf = len([s for s in SESSOES_CLDF if s[2] == "EXTRAORDINÁRIA"])

print(f"\n📊 CLDF (site oficial):")
print(f"   - Total: {total_cldf} sessões")
print(f"   - Ordinárias: {ord_cldf}")
print(f"   - Extraordinárias: {ext_cldf}")

ord_json = len([a for a in atas if a['tipo_sessao'] == 'ORDINÁRIA'])
ext_json = len([a for a in atas if 'EXTRA' in a['tipo_sessao']])
print(f"\n📊 JSON atual:")
print(f"   - Total: {len(atas)} atas")
print(f"   - Ordinárias: {ord_json}")
print(f"   - Extraordinárias: {ext_json}")

# Encontrar faltantes
faltantes = []
for data, num, tipo in SESSOES_CLDF:
    if (num, tipo) not in atas_existentes:
        faltantes.append((data, num, tipo))

print(f"\n❌ ATAS FALTANTES: {len(faltantes)}")
print("-" * 80)
for data, num, tipo in sorted(faltantes, key=lambda x: (x[2], x[1])):
    sigla = "ORD" if tipo == "ORDINÁRIA" else "EXT"
    print(f"   {num:03d} {sigla} - {data}")

print("\n" + "=" * 80)

