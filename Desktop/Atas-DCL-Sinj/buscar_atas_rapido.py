#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Busca rápida de atas faltantes nos DCLs - versão otimizada.
"""

import os
import re
import fitz

script_dir = os.path.dirname(os.path.abspath(__file__))
downloads_dir = os.path.join(script_dir, 'downloads_2007')

# Atas faltantes (excluindo 001 EXT que já foi adicionada)
FALTANTES = [
    (4, "EXTRAORDINÁRIA", "03/05/2007"),
    (5, "ORDINÁRIA", "13/02/2007"),
    (9, "ORDINÁRIA", "27/02/2007"),
    (11, "EXTRAORDINÁRIA", "19/06/2007"),
    (12, "EXTRAORDINÁRIA", "27/06/2007"),
    (15, "EXTRAORDINÁRIA", "11/09/2007"),
    (22, "EXTRAORDINÁRIA", "17/10/2007"),
    (26, "EXTRAORDINÁRIA", "31/10/2007"),
    (30, "ORDINÁRIA", "18/04/2007"),
    (37, "ORDINÁRIA", "08/05/2007"),
]

print("=" * 90)
print("BUSCA RÁPIDA DE ATAS FALTANTES")
print("=" * 90)

dcls = sorted([f for f in os.listdir(downloads_dir) if f.endswith('.pdf')])
print(f"📁 Total de DCLs: {len(dcls)}")

# Meses em português
MESES = {
    '01': 'janeiro', '02': 'fevereiro', '03': 'março', '04': 'abril',
    '05': 'maio', '06': 'junho', '07': 'julho', '08': 'agosto',
    '09': 'setembro', '10': 'outubro', '11': 'novembro', '12': 'dezembro'
}

encontradas = []

for num, tipo, data in FALTANTES:
    sigla = "EXT" if "EXTRA" in tipo else "ORD"
    dia, mes, ano = data.split('/')
    dia_int = int(dia)
    mes_nome = MESES[mes]
    
    print(f"\n🔍 {num:03d} {sigla} - {data}...")
    
    # Determinar DCLs candidatos baseado no mês (publicação geralmente 1-2 meses depois)
    mes_int = int(mes)
    meses_busca = [f"2007-{m:02d}" for m in range(mes_int, min(mes_int + 3, 13))]
    
    dcls_candidatos = [d for d in dcls if any(m in d for m in meses_busca)]
    
    for dcl in dcls_candidatos[:30]:  # Limitar busca
        try:
            doc = fitz.open(os.path.join(downloads_dir, dcl))
            for page_num in range(doc.page_count):
                page = doc[page_num]
                texto = page.get_text()
                texto_upper = texto.upper()
                
                # Verificar se contém o número da sessão e o tipo
                tipo_busca = "EXTRAORDIN" if "EXTRA" in tipo else "ORDIN"
                
                if tipo_busca in texto_upper:
                    # Padrão: "ATA DA Xª SESSÃO"
                    padrao = rf'{num}[ªa°]?\s*\(?[A-ZÁÉÍÓÚ]+\)?\s*SESS[ÃA]O\s*{tipo_busca}'
                    match = re.search(padrao, texto_upper)
                    
                    if match:
                        # Verificar data
                        data_padrao = rf'{dia_int}\s*DE\s*{mes_nome}'
                        if re.search(data_padrao, texto, re.IGNORECASE):
                            print(f"   ✅ {dcl} - Página {page_num + 1}")
                            encontradas.append({
                                'num': num, 'tipo': tipo, 'data': data,
                                'dcl': dcl, 'pag': page_num + 1
                            })
                            doc.close()
                            break
            else:
                doc.close()
                continue
            break
        except:
            pass

print(f"\n{'=' * 90}")
print(f"RESULTADO: {len(encontradas)} atas encontradas")
for e in encontradas:
    sigla = "EXT" if "EXTRA" in e['tipo'] else "ORD"
    print(f"  {e['num']:03d} {sigla} - {e['data']} → {e['dcl']} p.{e['pag']}")

