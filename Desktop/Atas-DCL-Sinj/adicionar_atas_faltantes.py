#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adiciona as atas faltantes identificadas ao JSON.
"""

import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir, 'fase2_atas_2007_final.json')

# Carregar JSON atual
with open(json_path, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print(f"📋 Atas atuais: {len(atas)}")

# Atas encontradas para adicionar
# Formato: (num, tipo, data_sessao, dcl, pag_inicio, pag_fim, data_pub)
NOVAS_ATAS = [
    (5, "ORDINÁRIA", "13/02/2007", "DCL_2007-03-049.pdf", 11, 22, "15/03/2007"),
    (9, "ORDINÁRIA", "27/02/2007", "DCL_2007-03-047.pdf", 50, 50, "14/03/2007"),
    (4, "EXTRAORDINÁRIA", "03/05/2007", "DCL_2007-05-094.pdf", 5, 5, "23/05/2007"),
    (37, "ORDINÁRIA", "08/05/2007", "DCL_2007-05-094.pdf", 6, 6, "23/05/2007"),
    (41, "ORDINÁRIA", "16/05/2007", "DCL_2007-05-099.pdf", 1, 1, "28/05/2007"),
    (50, "ORDINÁRIA", "06/06/2007", "DCL_2007-06-1766369018.pdf", 1, 1, "01/06/2007"),
    # Novas encontradas
    (30, "ORDINÁRIA", "18/04/2007", "DCL_2007-05-1766368939.pdf", 16, 16, "01/05/2007"),
    (39, "ORDINÁRIA", "10/05/2007", "DCL_2007-06-109.pdf", 1, 1, "01/06/2007"),
    (57, "ORDINÁRIA", "26/06/2007", "DCL_2007-08-144.pdf", 1, 1, "03/08/2007"),
    (11, "EXTRAORDINÁRIA", "19/06/2007", "DCL_2007-07-124.pdf", 1, 1, "01/07/2007"),
    (12, "EXTRAORDINÁRIA", "27/06/2007", "DCL_2007-07-124.pdf", 2, 2, "01/07/2007"),
    # Atas de setembro
    (71, "ORDINÁRIA", "28/08/2007", "DCL_2007-09-166.pdf", 1, 1, "01/09/2007"),
    (72, "ORDINÁRIA", "29/08/2007", "DCL_2007-09-170.pdf", 1, 1, "01/09/2007"),
    (73, "ORDINÁRIA", "30/08/2007", "DCL_2007-09-170.pdf", 48, 48, "01/09/2007"),
    (74, "ORDINÁRIA", "04/09/2007", "DCL_2007-09-171.pdf", 1, 1, "01/09/2007"),
    (75, "ORDINÁRIA", "05/09/2007", "DCL_2007-09-172.pdf", 1, 1, "01/09/2007"),
    (76, "ORDINÁRIA", "06/09/2007", "DCL_2007-09-172.pdf", 3, 3, "01/09/2007"),
    (77, "ORDINÁRIA", "11/09/2007", "DCL_2007-09-1766369161.pdf", 1, 1, "01/09/2007"),
    (15, "EXTRAORDINÁRIA", "11/09/2007", "DCL_2007-09-175.pdf", 1, 1, "01/09/2007"),
    # Mais atas de setembro/outubro
    (78, "ORDINÁRIA", "12/09/2007", "DCL_2007-09-1766369157.pdf", 1, 1, "01/09/2007"),
    (79, "ORDINÁRIA", "13/09/2007", "DCL_2007-09-1766369157.pdf", 28, 28, "01/09/2007"),
    (80, "ORDINÁRIA", "18/09/2007", "DCL_2007-09-1766369146.pdf", 3, 3, "01/09/2007"),
    (81, "ORDINÁRIA", "19/09/2007", "DCL_2007-09-1766369149.pdf", 60, 60, "01/09/2007"),
    (82, "ORDINÁRIA", "20/09/2007", "DCL_2007-09-1766369146.pdf", 2, 2, "01/09/2007"),
    (99, "ORDINÁRIA", "31/10/2007", "DCL_2007-12-1766369304.pdf", 13, 13, "01/12/2007"),
    # Atas de dezembro 2007 (publicadas em 2008)
    (113, "ORDINÁRIA", "05/12/2007", "DCL_2008-02-1766369371.pdf", 17, 17, "01/02/2008"),
    (114, "ORDINÁRIA", "06/12/2007", "DCL_2008-02-1766369371.pdf", 33, 33, "01/02/2008"),
    (31, "EXTRAORDINÁRIA", "04/12/2007", "DCL_2008-02-1766369379.pdf", 1, 1, "01/02/2008"),
    (32, "EXTRAORDINÁRIA", "05/12/2007", "DCL_2008-02-1766369379.pdf", 2, 2, "01/02/2008"),
    (33, "EXTRAORDINÁRIA", "11/12/2007", "DCL_2008-02-1766369363.pdf", 35, 35, "01/02/2008"),
    (34, "EXTRAORDINÁRIA", "12/12/2007", "DCL_2008-02-1766369363.pdf", 38, 38, "01/02/2008"),
]

# Criar set das atas existentes
existentes = set()
for ata in atas:
    num = int(str(ata['sessao_num']))
    tipo = ata['tipo_sessao']
    existentes.add((num, tipo))

adicionadas = 0
for num, tipo, data_sessao, dcl, pag_inicio, pag_fim, data_pub in NOVAS_ATAS:
    if (num, tipo) not in existentes:
        # Gerar nomenclatura
        dia, mes, ano = data_sessao.split('/')
        codigo_tipo = "2" if "EXTRA" in tipo else "1"
        sigla_tipo = "SE" if "EXTRA" in tipo else "SO"
        nomenclatura = f"{ano}-{mes}-{dia.zfill(2)}-{codigo_tipo}-{sigla_tipo}-{str(num).zfill(3)}-2-AC.pdf"
        
        nova_ata = {
            'dcl_original': dcl,
            'pag_inicio': pag_inicio,
            'pag_fim': pag_fim,
            'sessao_num': str(num).zfill(3),
            'tipo_sessao': tipo,
            'data_real': data_sessao,
            'data_publicacao_ata': data_pub,
            'nomenclatura': nomenclatura
        }
        atas.append(nova_ata)
        adicionadas += 1
        sigla = "EXT" if "EXTRA" in tipo else "ORD"
        print(f"✅ {str(num).zfill(3)} {sigla} - {data_sessao} → {dcl} p.{pag_inicio}")
    else:
        sigla = "EXT" if "EXTRA" in tipo else "ORD"
        print(f"⏭️  {str(num).zfill(3)} {sigla} já existe")

# Salvar JSON atualizado
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(atas, f, ensure_ascii=False, indent=2)

print(f"\n📊 Resultado:")
print(f"   Adicionadas: {adicionadas}")
print(f"   Total atual: {len(atas)}")

