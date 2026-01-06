# -*- coding: utf-8 -*-
"""
Script para corrigir nomenclatura de atas circunstanciadas de 2007
Padrão: YYYY-MM-DD-C-TT-NNN-T-TA.pdf
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

class CorrigirNomenclatura2007:
    def __init__(self):
        self.dir_atas = Path("atas_circunstanciadas_2007")
        self.arquivo_analise = Path("documentacao/ANALISE_PDFS_2007.json")
        self.analises = {}
        self.correcoes = []
        
        # Meses em português para número
        self.meses = {
            'janeiro': '01', 'fevereiro': '02', 'março': '03', 'abril': '04',
            'maio': '05', 'junho': '06', 'julho': '07', 'agosto': '08',
            'setembro': '09', 'outubro': '10', 'novembro': '11', 'dezembro': '12'
        }
    
    def carregar_analises(self):
        """Carrega análises de PDFs do JSON"""
        if self.arquivo_analise.exists():
            with open(self.arquivo_analise, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                for item in dados:
                    self.analises[item['arquivo_original']] = item
    
    def extrair_data(self, data_str):
        """Extrai data em formato YYYY-MM-DD"""
        if not data_str:
            return None
        
        # Padrão: "13 de março de 2007"
        padrao1 = r'(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})'
        match = re.search(padrao1, data_str, re.IGNORECASE)
        if match:
            dia = match.group(1).zfill(2)
            mes_nome = match.group(2).lower()
            ano = match.group(3)
            mes = self.meses.get(mes_nome)
            if mes:
                return f"{ano}-{mes}-{dia}"
        
        # Padrão: "06/03/2007"
        padrao2 = r'(\d{1,2})/(\d{1,2})/(\d{4})'
        match = re.search(padrao2, data_str)
        if match:
            dia = match.group(1).zfill(2)
            mes = match.group(2).zfill(2)
            ano = match.group(3)
            return f"{ano}-{mes}-{dia}"
        
        return None
    
    def extrair_numero_sessao(self, nome_arquivo):
        """Extrai número de sessão do nome do arquivo"""
        # Padrão: 2007-03-060-SO-013-AC.pdf ou 2007-03-30-1-SO-013-2-AC.pdf
        match = re.search(r'-SO-(\d+)-', nome_arquivo)
        if match:
            return match.group(1).zfill(3)
        return None
    
    def criar_novo_nome(self, arquivo_original, data_extraida):
        """Cria novo nome seguindo padrão YYYY-MM-DD-C-TT-NNN-T-TA.pdf"""
        if not data_extraida:
            return None
        
        # Extrai componentes
        ano, mes, dia = data_extraida.split('-')
        numero_sessao = self.extrair_numero_sessao(arquivo_original)
        
        if not numero_sessao:
            return None
        
        # Padrão: YYYY-MM-DD-C-TT-NNN-T-TA.pdf
        # C=1 (Ordinária), TT=SO, T=2 (Circunstanciada), TA=AC
        novo_nome = f"{ano}-{mes}-{dia}-1-SO-{numero_sessao}-2-AC.pdf"
        
        return novo_nome
    
    def obter_arquivo_original(self, arquivo_atual):
        """Obtém arquivo original a partir do arquivo atual"""
        # Se já está parcialmente renomeado, procura no JSON
        for orig, analise in self.analises.items():
            if analise.get('data_extraida'):
                data_extraida = self.extrair_data(analise['data_extraida'])
                if data_extraida:
                    novo_nome = self.criar_novo_nome(orig, data_extraida)
                    if novo_nome == arquivo_atual:
                        return orig
        
        return arquivo_atual
    
    def executar(self):
        """Executa correção de nomenclatura"""
        print("\n" + "="*80)
        print("CORREÇÃO DE NOMENCLATURA - ATAS CIRCUNSTANCIADAS 2007")
        print("="*80 + "\n")
        
        self.carregar_analises()
        
        if not self.dir_atas.exists():
            print("❌ Pasta não existe!")
            return
        
        arquivos = sorted(self.dir_atas.glob("*.pdf"))
        print(f"📊 Processando {len(arquivos)} arquivos...\n")
        
        sucesso = 0
        falha = 0
        
        for i, arquivo in enumerate(arquivos, 1):
            nome_arquivo = arquivo.name
            print(f"[{i}/{len(arquivos)}] {nome_arquivo}")
            
            # Obtém arquivo original
            arquivo_original = self.obter_arquivo_original(nome_arquivo)
            
            # Obtém data extraída
            analise = self.analises.get(arquivo_original, {})
            data_extraida_str = analise.get('data_extraida')
            
            if not data_extraida_str:
                print(f"  ⚠️  Sem data extraída - PULANDO")
                falha += 1
                continue
            
            # Extrai data em formato YYYY-MM-DD
            data_extraida = self.extrair_data(data_extraida_str)
            
            if not data_extraida:
                print(f"  ⚠️  Não conseguiu extrair data: {data_extraida_str}")
                falha += 1
                continue
            
            # Cria novo nome
            novo_nome = self.criar_novo_nome(arquivo_original, data_extraida)
            
            if not novo_nome:
                print(f"  ⚠️  Não conseguiu criar novo nome")
                falha += 1
                continue
            
            # Se já está com o nome correto, pula
            if nome_arquivo == novo_nome:
                print(f"  ✅ Já está correto: {novo_nome}")
                sucesso += 1
                continue
            
            # Renomeia arquivo
            caminho_original = self.dir_atas / nome_arquivo
            caminho_novo = self.dir_atas / novo_nome
            
            if not caminho_original.exists():
                print(f"  ❌ Arquivo não encontrado")
                falha += 1
                continue
            
            if caminho_novo.exists():
                print(f"  ⚠️  Arquivo de destino já existe")
                falha += 1
                continue
            
            try:
                caminho_original.rename(caminho_novo)
                print(f"  ✅ {novo_nome}")
                self.correcoes.append({
                    'original': nome_arquivo,
                    'novo': novo_nome,
                    'data': data_extraida,
                    'status': 'sucesso'
                })
                sucesso += 1
            except Exception as e:
                print(f"  ❌ Erro: {str(e)}")
                self.correcoes.append({
                    'original': nome_arquivo,
                    'novo': novo_nome,
                    'data': data_extraida,
                    'status': 'falha',
                    'erro': str(e)
                })
                falha += 1
        
        # Salva relatório
        self.salvar_relatorio(sucesso, falha)
        
        print(f"\n📊 RESUMO:")
        print(f"  Sucesso: {sucesso}/{len(arquivos)}")
        print(f"  Falha: {falha}/{len(arquivos)}")
    
    def salvar_relatorio(self, sucesso, falha):
        """Salva relatório de correção"""
        relatorio = {
            'data': datetime.now().isoformat(),
            'total': len(self.correcoes),
            'sucesso': sucesso,
            'falha': falha,
            'correcoes': self.correcoes
        }
        
        caminho = Path("documentacao/CORRECAO_NOMENCLATURA_2007.json")
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Relatório salvo em: {caminho}")

if __name__ == "__main__":
    corretor = CorrigirNomenclatura2007()
    corretor.executar()

