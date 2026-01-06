# -*- coding: utf-8 -*-
"""
Script para investigar atas sem data extraível
Tenta extrair data de múltiplas páginas do PDF
"""

import re
from pathlib import Path
import pdfplumber
import json

class InvestigadorAtas:
    def __init__(self):
        self.dir_atas = Path("atas_circunstanciadas_2007")
        self.atas_sem_data = [
            "2007-01-009-SO-034-AC.pdf",
            "2007-01-009-SO-035-AC.pdf",
            "2007-05-101-SO-002-AC.pdf",
            "2007-05-SO-002-AC.pdf",
            "2007-06-114-SO-393-AC.pdf",
            "2007-07-128-SO-046-AC.pdf",
            "2007-07-130-SO-051-AC.pdf",
            "2007-08-142-SO-003-AC.pdf",
            "2007-09-167-SO-069-AC.pdf",
            "2007-03-SO-013-AC.pdf",
            "2007-12-231-SO-092-AC.pdf"
        ]
        
        self.meses = {
            'janeiro': '01', 'fevereiro': '02', 'março': '03', 'abril': '04',
            'maio': '05', 'junho': '06', 'julho': '07', 'agosto': '08',
            'setembro': '09', 'outubro': '10', 'novembro': '11', 'dezembro': '12'
        }
        
        self.investigacoes = []
    
    def extrair_data_de_paginas(self, caminho_pdf):
        """Tenta extrair data de múltiplas páginas"""
        try:
            with pdfplumber.open(caminho_pdf) as pdf:
                # Tenta primeiras 5 páginas
                for num_pagina in range(min(5, len(pdf.pages))):
                    pagina = pdf.pages[num_pagina]
                    texto = pagina.extract_text()
                    
                    # Procura por padrões de data
                    padroes = [
                        r'(\d{1,2})\s+de\s+(janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)\s+de\s+(\d{4})',
                        r'(\d{1,2})/(\d{1,2})/(\d{4})',
                        r'(\d{4})-(\d{1,2})-(\d{1,2})',
                        r'Brasília,\s+\w+,\s+(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})',
                    ]
                    
                    for padrao in padroes:
                        match = re.search(padrao, texto, re.IGNORECASE)
                        if match:
                            return match.group(0), num_pagina, texto[:300]
                
                return None, None, None
        except Exception as e:
            return None, None, str(e)
    
    def executar(self):
        """Executa investigação"""
        print("\n" + "="*80)
        print("INVESTIGAÇÃO DE ATAS SEM DATA")
        print("="*80 + "\n")
        
        for i, nome_arquivo in enumerate(self.atas_sem_data, 1):
            caminho = self.dir_atas / nome_arquivo
            
            if not caminho.exists():
                print(f"[{i}/{len(self.atas_sem_data)}] {nome_arquivo}")
                print(f"  ❌ Arquivo não encontrado\n")
                continue
            
            print(f"[{i}/{len(self.atas_sem_data)}] {nome_arquivo}")
            
            data, pagina, amostra = self.extrair_data_de_paginas(caminho)
            
            if data:
                print(f"  ✅ Data encontrada: {data}")
                print(f"  📄 Página: {pagina}")
                print(f"  📝 Amostra: {amostra[:100]}...")
                self.investigacoes.append({
                    'arquivo': nome_arquivo,
                    'data': data,
                    'pagina': pagina,
                    'status': 'encontrada'
                })
            else:
                print(f"  ⚠️  Data não encontrada")
                print(f"  📝 Amostra: {amostra[:100] if amostra else 'N/A'}...")
                self.investigacoes.append({
                    'arquivo': nome_arquivo,
                    'data': None,
                    'pagina': None,
                    'status': 'nao_encontrada'
                })
            
            print()
        
        # Salva investigações
        caminho = Path("documentacao/INVESTIGACAO_ATAS_SEM_DATA.json")
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(self.investigacoes, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Investigações salvas em: {caminho}")
        
        # Resumo
        encontradas = sum(1 for i in self.investigacoes if i['status'] == 'encontrada')
        print(f"\n📊 RESUMO:")
        print(f"  Datas encontradas: {encontradas}/{len(self.atas_sem_data)}")
        print(f"  Datas não encontradas: {len(self.atas_sem_data) - encontradas}/{len(self.atas_sem_data)}")

if __name__ == "__main__":
    investigador = InvestigadorAtas()
    investigador.executar()

