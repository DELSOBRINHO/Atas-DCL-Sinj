# -*- coding: utf-8 -*-
"""
Analisa PDFs de atas circunstanciadas para extrair data correta
"""

import os
import re
from pathlib import Path
import pdfplumber
import json
from datetime import datetime

class AnalisadorPDFs2007:
    def __init__(self):
        self.dir_atas = Path("atas_circunstanciadas_2007")
        self.analises = []
    
    def extrair_data_pdf(self, caminho_pdf):
        """Extrai data do PDF analisando primeira página"""
        try:
            with pdfplumber.open(caminho_pdf) as pdf:
                primeira_pagina = pdf.pages[0]
                texto = primeira_pagina.extract_text()
                
                # Procura por padrões de data
                # Padrão: "13 de março de 2007" ou "13/03/2007"
                padroes_data = [
                    r'(\d{1,2})\s+de\s+(janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)\s+de\s+(\d{4})',
                    r'(\d{1,2})/(\d{1,2})/(\d{4})',
                    r'(\d{4})-(\d{1,2})-(\d{1,2})',
                ]
                
                for padrao in padroes_data:
                    match = re.search(padrao, texto, re.IGNORECASE)
                    if match:
                        return match.group(0), texto[:500]
                
                return None, texto[:500]
        except Exception as e:
            return None, str(e)
    
    def extrair_sessao_pdf(self, caminho_pdf):
        """Extrai informação de sessão do PDF"""
        try:
            with pdfplumber.open(caminho_pdf) as pdf:
                primeira_pagina = pdf.pages[0]
                texto = primeira_pagina.extract_text()
                
                # Procura por "Nª Sessão Ordinária/Extraordinária"
                padrao = r'(\d+)ª?\s+(?:Sessão|SESSÃO)\s+(Ordinária|Extraordinária|ORDINÁRIA|EXTRAORDINÁRIA)'
                match = re.search(padrao, texto)
                
                if match:
                    return {
                        'numero': match.group(1),
                        'tipo': match.group(2).lower()
                    }
                
                return None
        except Exception as e:
            return None
    
    def analisar_arquivo(self, nome_arquivo, caminho_pdf):
        """Analisa um arquivo e extrai informações"""
        data, texto_amostra = self.extrair_data_pdf(caminho_pdf)
        sessao = self.extrair_sessao_pdf(caminho_pdf)
        
        analise = {
            'arquivo_original': nome_arquivo,
            'caminho': str(caminho_pdf),
            'data_extraida': data,
            'sessao': sessao,
            'texto_amostra': texto_amostra[:200]
        }
        
        self.analises.append(analise)
        return analise
    
    def executar(self):
        """Executa análise de todos os PDFs"""
        print("\n" + "="*80)
        print("ANÁLISE DE PDFs - ATAS CIRCUNSTANCIADAS 2007")
        print("="*80 + "\n")
        
        if not self.dir_atas.exists():
            print("❌ Pasta não existe!")
            return
        
        arquivos = sorted(self.dir_atas.glob("*.pdf"))
        print(f"📊 Analisando {len(arquivos)} arquivos...\n")
        
        for i, arquivo in enumerate(arquivos, 1):
            print(f"[{i}/{len(arquivos)}] Analisando: {arquivo.name}")
            analise = self.analisar_arquivo(arquivo.name, arquivo)
            
            if analise['data_extraida']:
                print(f"  ✅ Data encontrada: {analise['data_extraida']}")
            else:
                print(f"  ⚠️  Data não encontrada")
            
            if analise['sessao']:
                print(f"  ✅ Sessão: {analise['sessao']['numero']}ª {analise['sessao']['tipo']}")
            else:
                print(f"  ⚠️  Sessão não encontrada")
        
        # Salva análises em JSON
        analises_path = Path("documentacao/ANALISE_PDFS_2007.json")
        analises_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(analises_path, 'w', encoding='utf-8') as f:
            json.dump(self.analises, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Análises salvas em: {analises_path}")
        
        # Resumo
        com_data = sum(1 for a in self.analises if a['data_extraida'])
        com_sessao = sum(1 for a in self.analises if a['sessao'])
        
        print(f"\n📊 RESUMO:")
        print(f"  Com data extraída: {com_data}/{len(self.analises)}")
        print(f"  Com sessão extraída: {com_sessao}/{len(self.analises)}")

if __name__ == "__main__":
    analisador = AnalisadorPDFs2007()
    analisador.executar()

