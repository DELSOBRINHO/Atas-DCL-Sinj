# -*- coding: utf-8 -*-
"""
Script para buscar atas faltantes no SINJ-DF
Identifica as 100 atas sucintas sem correspondente circunstanciada
"""

import json
import re
from pathlib import Path
from datetime import datetime

class BuscadorAtasFaltantes2007:
    def __init__(self):
        self.arquivo_comparacao = Path("documentacao/COMPARACAO_ONDRIVE_2007.json")
        self.atas_faltantes = []
        self.atas_encontradas = []
    
    def carregar_comparacao(self):
        """Carrega dados de comparação"""
        if not self.arquivo_comparacao.exists():
            print("❌ Arquivo de comparação não existe!")
            return False
        
        with open(self.arquivo_comparacao, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            self.atas_encontradas = dados.get('correspondencias', [])
            self.atas_faltantes = dados.get('sem_correspondencia', [])
        
        return True
    
    def gerar_lista_busca(self):
        """Gera lista de atas para buscar no SINJ-DF"""
        print("\n" + "="*80)
        print("ATAS FALTANTES - LISTA PARA BUSCA NO SINJ-DF")
        print("="*80 + "\n")
        
        if not self.carregar_comparacao():
            return
        
        print(f"📊 Total de atas faltantes: {len(self.atas_faltantes)}\n")
        
        # Agrupa por mês
        por_mes = {}
        for ata in self.atas_faltantes:
            data = ata['data']
            mes = data.split('-')[1]
            if mes not in por_mes:
                por_mes[mes] = []
            por_mes[mes].append(ata)
        
        # Exibe por mês
        meses_nomes = {
            '01': 'Janeiro', '02': 'Fevereiro', '03': 'Março', '04': 'Abril',
            '05': 'Maio', '06': 'Junho', '07': 'Julho', '08': 'Agosto',
            '09': 'Setembro', '10': 'Outubro', '11': 'Novembro', '12': 'Dezembro'
        }
        
        for mes in sorted(por_mes.keys()):
            atas = por_mes[mes]
            print(f"📅 {meses_nomes[mes]} ({len(atas)} atas):")
            for ata in atas[:5]:
                numero = ata['numero_sessao']
                print(f"  • Sessão {numero:3d}: {ata['ata_sucinta']}")
            if len(atas) > 5:
                print(f"  ... e mais {len(atas) - 5}")
            print()
        
        # Salva lista estruturada
        self.salvar_lista_busca()
    
    def salvar_lista_busca(self):
        """Salva lista de atas para buscar"""
        lista = {
            'data': datetime.now().isoformat(),
            'total_faltantes': len(self.atas_faltantes),
            'atas_faltantes': self.atas_faltantes,
            'instrucoes': [
                '1. Acessar SINJ-DF: https://www.sinj.df.gov.br',
                '2. Buscar por "Diário da Câmara Legislativa" (DCL)',
                '3. Filtrar por ano 2007',
                '4. Para cada ata faltante, procurar por número de sessão',
                '5. Verificar se existe ata circunstanciada',
                '6. Se existir, baixar e adicionar à pasta atas_circunstanciadas_2007'
            ]
        }
        
        caminho = Path("documentacao/ATAS_FALTANTES_LISTA_BUSCA_2007.json")
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(lista, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Lista de busca salva em: {caminho}")
        
        # Resumo
        print(f"\n📊 RESUMO:")
        print(f"  Total de atas faltantes: {len(self.atas_faltantes)}")
        print(f"  Total de atas encontradas: {len(self.atas_encontradas)}")
        print(f"  Taxa de cobertura: {100*len(self.atas_encontradas)//(len(self.atas_encontradas)+len(self.atas_faltantes))}%")

if __name__ == "__main__":
    buscador = BuscadorAtasFaltantes2007()
    buscador.gerar_lista_busca()

