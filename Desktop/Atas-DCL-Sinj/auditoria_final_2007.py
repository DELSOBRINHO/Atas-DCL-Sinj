# -*- coding: utf-8 -*-
"""
Auditoria final de nomenclatura de atas circunstanciadas 2007
"""

import re
import json
from pathlib import Path
from datetime import datetime

class AuditoriaFinal2007:
    def __init__(self):
        self.dir_atas = Path("atas_circunstanciadas_2007")
        self.padroes_corretos = []
        self.padroes_incorretos = []
        
        # Regex para validar padrão correto
        self.regex_correto = r'^\d{4}-\d{2}-\d{2}-[1-5]-(SO|SE|SS|SP)-\d{3}-[1-2]-(AS|AC)\.pdf$'
    
    def validar_nomenclatura(self, nome_arquivo):
        """Valida se o arquivo segue o padrão correto"""
        return bool(re.match(self.regex_correto, nome_arquivo))
    
    def extrair_componentes(self, nome_arquivo):
        """Extrai componentes do nome do arquivo"""
        match = re.match(r'(\d{4})-(\d{2})-(\d{2})-([1-5])-(SO|SE|SS|SP)-(\d{3})-([1-2])-(AS|AC)', nome_arquivo)
        if match:
            return {
                'ano': match.group(1),
                'mes': match.group(2),
                'dia': match.group(3),
                'codigo_tipo_sessao': match.group(4),
                'tipo_sessao': match.group(5),
                'numero_sessao': match.group(6),
                'codigo_tipo_ata': match.group(7),
                'tipo_ata': match.group(8)
            }
        return None
    
    def executar(self):
        """Executa auditoria final"""
        print("\n" + "="*80)
        print("AUDITORIA FINAL - ATAS CIRCUNSTANCIADAS 2007")
        print("="*80 + "\n")
        
        if not self.dir_atas.exists():
            print("❌ Pasta não existe!")
            return
        
        arquivos = sorted(self.dir_atas.glob("*.pdf"))
        print(f"📊 Auditando {len(arquivos)} arquivos...\n")
        
        for i, arquivo in enumerate(arquivos, 1):
            nome_arquivo = arquivo.name
            
            if self.validar_nomenclatura(nome_arquivo):
                componentes = self.extrair_componentes(nome_arquivo)
                self.padroes_corretos.append({
                    'arquivo': nome_arquivo,
                    'componentes': componentes
                })
                print(f"[{i}/{len(arquivos)}] ✅ {nome_arquivo}")
            else:
                self.padroes_incorretos.append({
                    'arquivo': nome_arquivo
                })
                print(f"[{i}/{len(arquivos)}] ❌ {nome_arquivo}")
        
        # Salva relatório
        self.salvar_relatorio(len(arquivos))
        
        # Resumo
        print(f"\n📊 RESUMO FINAL:")
        print(f"  Nomenclatura correta: {len(self.padroes_corretos)}/{len(arquivos)} ({100*len(self.padroes_corretos)//len(arquivos)}%)")
        print(f"  Nomenclatura incorreta: {len(self.padroes_incorretos)}/{len(arquivos)} ({100*len(self.padroes_incorretos)//len(arquivos)}%)")
        
        if self.padroes_incorretos:
            print(f"\n❌ ATAS COM NOMENCLATURA INCORRETA:")
            for item in self.padroes_incorretos:
                print(f"  • {item['arquivo']}")
    
    def salvar_relatorio(self, total):
        """Salva relatório de auditoria final"""
        relatorio = {
            'data': datetime.now().isoformat(),
            'total': total,
            'corretos': len(self.padroes_corretos),
            'incorretos': len(self.padroes_incorretos),
            'percentual_correto': 100 * len(self.padroes_corretos) // total if total > 0 else 0,
            'padroes_corretos': self.padroes_corretos,
            'padroes_incorretos': self.padroes_incorretos
        }
        
        caminho = Path("documentacao/AUDITORIA_FINAL_2007.json")
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Relatório salvo em: {caminho}")

if __name__ == "__main__":
    auditoria = AuditoriaFinal2007()
    auditoria.executar()

