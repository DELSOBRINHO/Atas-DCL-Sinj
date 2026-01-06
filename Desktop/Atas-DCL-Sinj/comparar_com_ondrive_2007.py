# -*- coding: utf-8 -*-
"""
Script para comparar atas circunstanciadas com atas sucintas do OneDrive
"""

import re
import json
from pathlib import Path
from datetime import datetime

class ComparadorAtas2007:
    def __init__(self):
        self.dir_atas_ac = Path("atas_circunstanciadas_2007")
        self.dir_ondrive = Path("C:/Users/omega/OneDrive - Câmara Legislativa do Distrito Federal - CLDF/Cadernos_Anais_CLDF/05_Legislatura_2007-2010/Cadernos_PDF/PDFs_Individuais/2007")
        self.atas_ac = {}
        self.atas_as = {}
        self.correspondencias = []
        self.sem_correspondencia = []
    
    def extrair_numero_sessao(self, nome_arquivo):
        """Extrai número de sessão do nome do arquivo"""
        # Padrão: YYYY-MM-DD-C-TT-NNN-T-TA.pdf
        match = re.search(r'-SO-(\d+)-', nome_arquivo)
        if match:
            return int(match.group(1))
        return None
    
    def extrair_data(self, nome_arquivo):
        """Extrai data do nome do arquivo"""
        # Padrão: YYYY-MM-DD-C-TT-NNN-T-TA.pdf
        match = re.match(r'(\d{4})-(\d{2})-(\d{2})', nome_arquivo)
        if match:
            return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
        return None
    
    def carregar_atas_ac(self):
        """Carrega atas circunstanciadas"""
        if not self.dir_atas_ac.exists():
            print("❌ Pasta de atas circunstanciadas não existe!")
            return
        
        for arquivo in self.dir_atas_ac.glob("*.pdf"):
            numero_sessao = self.extrair_numero_sessao(arquivo.name)
            data = self.extrair_data(arquivo.name)
            
            if numero_sessao:
                self.atas_ac[numero_sessao] = {
                    'arquivo': arquivo.name,
                    'data': data
                }
    
    def carregar_atas_as(self):
        """Carrega atas sucintas do OneDrive"""
        if not self.dir_ondrive.exists():
            print("❌ Pasta do OneDrive não existe!")
            return
        
        for arquivo in self.dir_ondrive.glob("*.pdf"):
            numero_sessao = self.extrair_numero_sessao(arquivo.name)
            data = self.extrair_data(arquivo.name)
            
            if numero_sessao:
                self.atas_as[numero_sessao] = {
                    'arquivo': arquivo.name,
                    'data': data
                }
    
    def comparar(self):
        """Compara atas circunstanciadas com atas sucintas"""
        print("\n" + "="*80)
        print("COMPARAÇÃO DE ATAS CIRCUNSTANCIADAS COM ATAS SUCINTAS")
        print("="*80 + "\n")
        
        self.carregar_atas_ac()
        self.carregar_atas_as()
        
        print(f"📊 Atas Circunstanciadas: {len(self.atas_ac)}")
        print(f"📊 Atas Sucintas (OneDrive): {len(self.atas_as)}\n")
        
        # Procura correspondências
        for numero_sessao, ata_as in self.atas_as.items():
            if numero_sessao in self.atas_ac:
                ata_ac = self.atas_ac[numero_sessao]
                self.correspondencias.append({
                    'numero_sessao': numero_sessao,
                    'ata_sucinta': ata_as['arquivo'],
                    'ata_circunstanciada': ata_ac['arquivo'],
                    'data_sucinta': ata_as['data'],
                    'data_circunstanciada': ata_ac['data'],
                    'status': 'encontrada'
                })
            else:
                self.sem_correspondencia.append({
                    'numero_sessao': numero_sessao,
                    'ata_sucinta': ata_as['arquivo'],
                    'data': ata_as['data'],
                    'status': 'sem_correspondencia'
                })
        
        # Exibe resultados
        print(f"✅ COM CORRESPONDÊNCIA: {len(self.correspondencias)}")
        for item in self.correspondencias[:10]:
            print(f"  Sessão {item['numero_sessao']:3d}: {item['ata_sucinta'][:40]}")
        if len(self.correspondencias) > 10:
            print(f"  ... e mais {len(self.correspondencias) - 10}")
        
        print(f"\n❌ SEM CORRESPONDÊNCIA: {len(self.sem_correspondencia)}")
        for item in self.sem_correspondencia[:10]:
            print(f"  Sessão {item['numero_sessao']:3d}: {item['ata_sucinta'][:40]}")
        if len(self.sem_correspondencia) > 10:
            print(f"  ... e mais {len(self.sem_correspondencia) - 10}")
        
        # Salva relatório
        self.salvar_relatorio()
    
    def salvar_relatorio(self):
        """Salva relatório de comparação"""
        relatorio = {
            'data': datetime.now().isoformat(),
            'atas_circunstanciadas_total': len(self.atas_ac),
            'atas_sucintas_total': len(self.atas_as),
            'com_correspondencia': len(self.correspondencias),
            'sem_correspondencia': len(self.sem_correspondencia),
            'percentual_correspondencia': 100 * len(self.correspondencias) // len(self.atas_as) if self.atas_as else 0,
            'correspondencias': self.correspondencias,
            'sem_correspondencia': self.sem_correspondencia
        }
        
        caminho = Path("documentacao/COMPARACAO_ONDRIVE_2007.json")
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Relatório salvo em: {caminho}")
        print(f"\n📊 RESUMO:")
        print(f"  Com correspondência: {len(self.correspondencias)}/{len(self.atas_as)} ({relatorio['percentual_correspondencia']}%)")
        print(f"  Sem correspondência: {len(self.sem_correspondencia)}/{len(self.atas_as)}")

if __name__ == "__main__":
    comparador = ComparadorAtas2007()
    comparador.comparar()

