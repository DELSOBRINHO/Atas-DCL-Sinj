#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BUSCAR 22ª E 97ª - Investigação Específica
===========================================

Objetivo: Procurar especificamente pelas sessões 22ª e 97ª

Uso:
    python buscar_22_e_97.py

Autor: Sistema de Automação CLDF
Data: 2025-12-24
"""

import pdfplumber
from pathlib import Path
import re

USUARIO = "omega"
PASTA_DCLS = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/downloads_2007")

# DCLs específicos
DCLS_INVESTIGAR = {
    "DCL_2007-01-231.pdf": 22,      # Procurar 22ª
    "DCL_2007-12-1766369304.pdf": 97 # Procurar 97ª
}

def buscar_sessao(caminho_pdf, num_sessao_alvo):
    """Busca uma sessão específica em um DCL"""
    
    try:
        with pdfplumber.open(caminho_pdf) as pdf:
            print(f"\n📄 Buscando {num_sessao_alvo}ª em: {caminho_pdf.name}")
            print(f"   Total de páginas: {len(pdf.pages)}")
            
            encontrada = False
            
            for num_pag, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                
                # Procurar por padrões que contenham a sessão alvo
                # Padrões: "22ª", "VIGÉSIMA SEGUNDA", "VIGÉSIMA-SEGUNDA", etc.
                
                # Padrão 1: número + ª
                if re.search(rf'{num_sessao_alvo}[ªa°º]', text):
                    print(f"   ✅ Encontrado na página {num_pag}")
                    
                    # Extrair contexto
                    linhas = text.split('\n')
                    for i, linha in enumerate(linhas):
                        if re.search(rf'{num_sessao_alvo}[ªa°º]', linha):
                            contexto = '\n'.join(linhas[max(0, i-2):min(len(linhas), i+3)])
                            print(f"\n   Contexto:")
                            print(f"   {contexto[:300]}")
                            encontrada = True
                            break
                
                # Padrão 2: procurar por "ATACIRCUNSTANCIADA" + número
                if "ATACIRCUNSTANCIADA" in text.replace(" ", ""):
                    linhas = text.split('\n')
                    for i, linha in enumerate(linhas):
                        if "ATACIRCUNSTANCIADA" in linha.replace(" ", ""):
                            contexto = '\n'.join(linhas[max(0, i-1):min(len(linhas), i+6)])
                            
                            # Procurar número neste contexto
                            match = re.search(r'(\d+)[ªa°º]', contexto)
                            if match:
                                num_encontrado = int(match.group(1))
                                if num_encontrado == num_sessao_alvo:
                                    print(f"   ✅ Encontrado na página {num_pag}")
                                    print(f"\n   Contexto:")
                                    print(f"   {contexto[:300]}")
                                    encontrada = True
                                    break
            
            if not encontrada:
                print(f"   ❌ Não encontrada")
    
    except Exception as e:
        print(f"   ❌ Erro: {e}")

def main():
    print("\n" + "="*70)
    print("BUSCAR 22ª E 97ª - Investigação Específica")
    print("="*70)
    
    for dcl_nome, num_sessao in DCLS_INVESTIGAR.items():
        caminho = PASTA_DCLS / dcl_nome
        
        if not caminho.exists():
            print(f"\n❌ Arquivo não encontrado: {caminho}")
            continue
        
        buscar_sessao(caminho, num_sessao)

if __name__ == "__main__":
    main()

