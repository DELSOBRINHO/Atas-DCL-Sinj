#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para analisar o sumário do PDF e identificar todas as atas
"""

import pdfplumber
import re

pdf_path = 'DCL nº 218 de 01 de dezembro de 2008 - Suplemento.pdf'

with pdfplumber.open(pdf_path) as pdf:
    total_paginas = len(pdf.pages)
    print(f'Total de páginas: {total_paginas}\n')
    
    # Extrai texto da primeira página
    primeira_pagina = pdf.pages[0]
    texto_sumario = primeira_pagina.extract_text()
    
    # Mostra o sumário completo
    print('SUMÁRIO COMPLETO:')
    print('='*70)
    print(texto_sumario)
    print('='*70)
    print('\n\nANALISANDO ATAS:\n')
    
    # Padrão para identificar atas
    padrao = r'Ata\s*Circ\.?\s*da\s*(\d+)a?\s*Sessão\s*(Ordinária|Extraordinária)\s*(\d+)'
    
    matches = list(re.finditer(padrao, texto_sumario, re.IGNORECASE))
    
    print(f'Total de atas encontradas: {len(matches)}\n')
    
    for i, match in enumerate(matches):
        numero_sessao = match.group(1)
        tipo_sessao = match.group(2)
        pagina_inicio = int(match.group(3))
        
        print(f'{i+1}. Ata {numero_sessao}ª {tipo_sessao}')
        print(f'   Página inicial: {pagina_inicio}')
        print(f'   Match: {match.group(0)}')
        print()
    
    # Procura por "35" no texto
    print('\n\nPROCURANDO POR "35" NO SUMÁRIO:\n')
    linhas = texto_sumario.split('\n')
    for i, linha in enumerate(linhas):
        if '35' in linha:
            print(f'Linha {i}: {linha}')

