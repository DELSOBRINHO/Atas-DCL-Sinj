# -*- coding: utf-8 -*-
"""
Script final para renomear todas as atas com nomenclatura correta
Usa dados de INVESTIGACAO_ATAS_SEM_DATA.json
"""

import re
import json
from pathlib import Path
from datetime import datetime

class RenomeadorFinal2007:
    def __init__(self):
        self.dir_atas = Path("atas_circunstanciadas_2007")
        self.arquivo_investigacao = Path("documentacao/INVESTIGACAO_ATAS_SEM_DATA.json")
        self.investigacoes = {}
        self.renomeacoes = []
        
        self.meses = {
            'janeiro': '01', 'fevereiro': '02', 'março': '03', 'abril': '04',
            'maio': '05', 'junho': '06', 'julho': '07', 'agosto': '08',
            'setembro': '09', 'outubro': '10', 'novembro': '11', 'dezembro': '12'
        }
    
    def carregar_investigacoes(self):
        """Carrega investigações do JSON"""
        if self.arquivo_investigacao.exists():
            with open(self.arquivo_investigacao, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                for item in dados:
                    self.investigacoes[item['arquivo']] = item
    
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
        match = re.search(r'-SO-(\d+)-', nome_arquivo)
        if match:
            return match.group(1).zfill(3)
        return None
    
    def criar_novo_nome(self, arquivo_original, data_extraida):
        """Cria novo nome seguindo padrão YYYY-MM-DD-C-TT-NNN-T-TA.pdf"""
        if not data_extraida:
            return None
        
        ano, mes, dia = data_extraida.split('-')
        numero_sessao = self.extrair_numero_sessao(arquivo_original)
        
        if not numero_sessao:
            return None
        
        novo_nome = f"{ano}-{mes}-{dia}-1-SO-{numero_sessao}-2-AC.pdf"
        return novo_nome
    
    def executar(self):
        """Executa renomeação final"""
        print("\n" + "="*80)
        print("RENOMEAÇÃO FINAL - ATAS CIRCUNSTANCIADAS 2007")
        print("="*80 + "\n")
        
        self.carregar_investigacoes()
        
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
            
            # Obtém data da investigação
            investigacao = self.investigacoes.get(nome_arquivo, {})
            data_str = investigacao.get('data')
            
            if not data_str:
                print(f"  ⚠️  Sem data - PULANDO")
                falha += 1
                continue
            
            # Extrai data
            data_extraida = self.extrair_data(data_str)
            
            if not data_extraida:
                print(f"  ⚠️  Não conseguiu extrair data: {data_str}")
                falha += 1
                continue
            
            # Cria novo nome
            novo_nome = self.criar_novo_nome(nome_arquivo, data_extraida)
            
            if not novo_nome:
                print(f"  ⚠️  Não conseguiu criar novo nome")
                falha += 1
                continue
            
            # Se já está correto, pula
            if nome_arquivo == novo_nome:
                print(f"  ✅ Já está correto")
                sucesso += 1
                continue
            
            # Renomeia
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
                sucesso += 1
            except Exception as e:
                print(f"  ❌ Erro: {str(e)}")
                falha += 1
        
        print(f"\n📊 RESUMO:")
        print(f"  Sucesso: {sucesso}/{len(arquivos)}")
        print(f"  Falha: {falha}/{len(arquivos)}")

if __name__ == "__main__":
    renomeador = RenomeadorFinal2007()
    renomeador.executar()

