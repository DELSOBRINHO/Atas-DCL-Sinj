#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BAIXAR DCLs 2007 + JAN-FEV 2008
================================

Baixa todos os 327 DCLs do SINJ-DF usando os links salvos em dcls_2007.json

Uso:
    python baixar_dcls_2007_2008.py

Autor: Sistema de Automação CLDF
Data: 2025-12-22
"""

import os
import sys
import json
import time
import logging
from pathlib import Path
import requests
import urllib3

# Desabilitar avisos de SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ======================================================================
# CONFIGURAÇÕES
# ======================================================================

USUARIO = "omega"
DIR_LINKS = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/links_2007")
DIR_DOWNLOADS = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/downloads_2007")
ARQUIVO_LINKS = DIR_LINKS / "dcls_2007.json"

# ======================================================================
# LOGGING
# ======================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('baixar_dcls_2007_2008.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ======================================================================
# FUNÇÕES PRINCIPAIS
# ======================================================================

def carregar_links():
    """Carrega links do arquivo JSON"""
    print("\n" + "="*70)
    print("📂 CARREGANDO LINKS")
    print("="*70)
    
    if not ARQUIVO_LINKS.exists():
        print(f"❌ Arquivo não encontrado: {ARQUIVO_LINKS}")
        return []
    
    try:
        with open(ARQUIVO_LINKS, 'r', encoding='utf-8') as f:
            links = json.load(f)
        
        print(f"✅ {len(links)} links carregados")
        return links
    except Exception as e:
        print(f"❌ Erro ao carregar links: {e}")
        return []

def gerar_nome_arquivo(url, ano, mes):
    """Gera nome do arquivo baseado no URL e data"""
    # Extrair número do DCL do URL
    try:
        # Exemplo: DCL%20n%C2%BA%20021%20de%2031%20de%20janeiro%20de%202007.pdf
        if 'DCL' in url:
            # Extrair número do DCL
            partes = url.split('DCL%20n%C2%BA%20')
            if len(partes) > 1:
                numero = partes[1].split('%20')[0]
                return f"DCL_{ano}-{mes:02d}-{numero:03d}.pdf"
    except:
        pass
    
    # Fallback: usar timestamp
    return f"DCL_{ano}-{mes:02d}-{int(time.time())}.pdf"

def baixar_dcl(url, caminho_arquivo, tentativas=3):
    """Baixa um DCL do SINJ-DF usando requests com SSL desabilitado"""
    for tentativa in range(tentativas):
        try:
            # Usar requests com SSL desabilitado
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(url, headers=headers, timeout=30, verify=False)
            response.raise_for_status()

            with open(caminho_arquivo, 'wb') as f:
                f.write(response.content)

            return True

        except Exception as e:
            if tentativa < tentativas - 1:
                print(f"      ⚠️  Tentativa {tentativa + 1} falhou, tentando novamente...")
                time.sleep(2)
            else:
                print(f"      ❌ Erro após {tentativas} tentativas")
                return False

    return False

def baixar_dcls(links):
    """Baixa todos os DCLs"""
    print("\n" + "="*70)
    print("⬇️  BAIXANDO DCLs")
    print("="*70)
    
    # Criar diretório de downloads
    DIR_DOWNLOADS.mkdir(parents=True, exist_ok=True)
    
    total = len(links)
    sucesso = 0
    falha = 0
    ja_existe = 0
    
    print(f"\n📥 Baixando {total} DCLs...\n")
    
    for i, dcl in enumerate(links, 1):
        url = dcl['url']
        ano = dcl['ano']
        mes = dcl['mes']
        
        # Gerar nome do arquivo
        nome_arquivo = gerar_nome_arquivo(url, ano, mes)
        caminho_arquivo = DIR_DOWNLOADS / nome_arquivo
        
        # Verificar se já existe
        if caminho_arquivo.exists():
            print(f"[{i:3d}/{total}] ⏭️  {nome_arquivo} (já existe)")
            ja_existe += 1
            continue
        
        # Baixar arquivo
        print(f"[{i:3d}/{total}] ⬇️  {nome_arquivo}...", end=" ", flush=True)
        
        if baixar_dcl(url, caminho_arquivo):
            tamanho = caminho_arquivo.stat().st_size / 1024  # KB
            print(f"✅ ({tamanho:.0f} KB)")
            sucesso += 1
        else:
            print(f"❌")
            falha += 1
        
        # Respeitar servidor (não sobrecarregar)
        time.sleep(0.5)
    
    print("\n" + "-" * 70)
    print(f"\n📊 RESULTADO")
    print("-" * 70)
    print(f"   ✅ Sucesso:    {sucesso}")
    print(f"   ⏭️  Já existe:  {ja_existe}")
    print(f"   ❌ Falha:      {falha}")
    print(f"   📊 Total:      {total}")
    
    # Calcular tamanho total
    tamanho_total = sum(f.stat().st_size for f in DIR_DOWNLOADS.glob('*.pdf')) / (1024 * 1024)
    print(f"\n💾 Tamanho total: {tamanho_total:.1f} MB")
    
    return sucesso, falha, ja_existe

def main():
    """Função principal"""
    print("\n" + "="*70)
    print("BAIXAR DCLs 2007 + JAN-FEV 2008")
    print("="*70)
    
    # Carregar links
    links = carregar_links()
    
    if not links:
        print("\n❌ Nenhum link para baixar")
        return
    
    # Baixar DCLs
    sucesso, falha, ja_existe = baixar_dcls(links)
    
    # Resumo final
    print("\n" + "="*70)
    if falha == 0:
        print("✅ TODOS OS DCLs FORAM BAIXADOS COM SUCESSO!")
    else:
        print(f"⚠️  {falha} DCL(s) falharam ao baixar")
    print("="*70)
    
    print(f"\n📁 DCLs salvos em: {DIR_DOWNLOADS}")
    print(f"\n🚀 Próximo passo: python processar_ocr_2007_2008.py")

if __name__ == "__main__":
    main()

