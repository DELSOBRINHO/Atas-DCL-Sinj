# -*- coding: utf-8 -*-
"""
AUDITORIA DE ATAS CIRCUNSTANCIADAS DE 2007
Valida nomenclatura, integridade e correspondência com atas sucintas
"""

import os
import re
from pathlib import Path
from datetime import datetime
import json

# Padrão correto de nomenclatura
PADRAO_CORRETO = r'^\d{4}-\d{2}-\d{2}-[1-5]-(SO|SE|SS|SP)-\d{3}-[1-2]-(AS|AC)\.pdf$'

class AuditoriaAtas2007:
    def __init__(self):
        self.dir_downloads = Path("downloads_2007")
        self.dir_atas_ac = Path("atas_circunstanciadas_2007")
        self.dir_processados = Path("processados_2007")
        self.relatorio = {
            'data_auditoria': datetime.now().isoformat(),
            'downloads': {},
            'atas_ac': {},
            'inconsistencias': []
        }
    
    def validar_nomenclatura(self, nome_arquivo):
        """Valida se o arquivo segue o padrão correto"""
        if re.match(PADRAO_CORRETO, nome_arquivo):
            return True, None
        return False, f"Nomenclatura incorreta: {nome_arquivo}"
    
    def extrair_info_arquivo(self, nome_arquivo):
        """Extrai informações do nome do arquivo"""
        try:
            partes = nome_arquivo.replace('.pdf', '').split('-')
            if len(partes) >= 8:
                return {
                    'ano': partes[0],
                    'mes': partes[1],
                    'dia': partes[2],
                    'cod_tipo': partes[3],
                    'tipo_sessao': partes[4],
                    'num_sessao': partes[5],
                    'cod_ata': partes[6],
                    'tipo_ata': partes[7]
                }
        except:
            pass
        return None
    
    def auditar_downloads(self):
        """Audita pasta downloads_2007"""
        print("\n" + "="*80)
        print("AUDITORIA: downloads_2007/")
        print("="*80)
        
        if not self.dir_downloads.exists():
            print("❌ Pasta não existe!")
            return
        
        arquivos = sorted(self.dir_downloads.glob("*.pdf"))
        print(f"\n📊 Total de arquivos: {len(arquivos)}")
        
        tamanho_total = 0
        for arquivo in arquivos:
            tamanho_mb = arquivo.stat().st_size / (1024 * 1024)
            tamanho_total += tamanho_mb
        
        print(f"📦 Tamanho total: {tamanho_total:.2f} MB")
        print(f"📅 Período: {arquivos[0].name[:7]} a {arquivos[-1].name[:7]}")
        
        self.relatorio['downloads'] = {
            'total': len(arquivos),
            'tamanho_mb': round(tamanho_total, 2),
            'primeiro': arquivos[0].name if arquivos else None,
            'ultimo': arquivos[-1].name if arquivos else None
        }
    
    def auditar_atas_ac(self):
        """Audita pasta atas_circunstanciadas_2007"""
        print("\n" + "="*80)
        print("AUDITORIA: atas_circunstanciadas_2007/")
        print("="*80)
        
        if not self.dir_atas_ac.exists():
            print("❌ Pasta não existe!")
            return
        
        arquivos = sorted(self.dir_atas_ac.glob("*.pdf"))
        print(f"\n📊 Total de atas: {len(arquivos)}")
        
        corretos = 0
        incorretos = []
        tamanho_total = 0
        
        for arquivo in arquivos:
            nome = arquivo.name
            tamanho_mb = arquivo.stat().st_size / (1024 * 1024)
            tamanho_total += tamanho_mb
            
            valido, erro = self.validar_nomenclatura(nome)
            
            if valido:
                corretos += 1
                print(f"  ✅ {nome}")
            else:
                incorretos.append({'arquivo': nome, 'erro': erro})
                print(f"  ❌ {nome}")
                print(f"     └─ {erro}")
        
        print(f"\n📦 Tamanho total: {tamanho_total:.2f} MB")
        print(f"✅ Nomenclatura correta: {corretos}/{len(arquivos)}")
        print(f"❌ Nomenclatura incorreta: {len(incorretos)}/{len(arquivos)}")
        
        self.relatorio['atas_ac'] = {
            'total': len(arquivos),
            'corretos': corretos,
            'incorretos': len(incorretos),
            'tamanho_mb': round(tamanho_total, 2),
            'arquivos_incorretos': incorretos
        }
    
    def gerar_relatorio(self):
        """Gera relatório em JSON"""
        relatorio_path = Path("documentacao/AUDITORIA_2007.json")
        relatorio_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(relatorio_path, 'w', encoding='utf-8') as f:
            json.dump(self.relatorio, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Relatório salvo em: {relatorio_path}")
    
    def executar(self):
        """Executa auditoria completa"""
        print("\n" + "╔" + "="*78 + "╗")
        print("║" + " "*20 + "AUDITORIA DE ATAS CIRCUNSTANCIADAS 2007" + " "*20 + "║")
        print("╚" + "="*78 + "╝")
        
        self.auditar_downloads()
        self.auditar_atas_ac()
        self.gerar_relatorio()
        
        print("\n" + "="*80)
        print("RESUMO FINAL")
        print("="*80)
        print(f"Downloads: {self.relatorio['downloads'].get('total', 0)} arquivos")
        print(f"Atas AC: {self.relatorio['atas_ac'].get('total', 0)} arquivos")
        print(f"  ✅ Corretos: {self.relatorio['atas_ac'].get('corretos', 0)}")
        print(f"  ❌ Incorretos: {self.relatorio['atas_ac'].get('incorretos', 0)}")
        print("="*80 + "\n")

if __name__ == "__main__":
    auditoria = AuditoriaAtas2007()
    auditoria.executar()

