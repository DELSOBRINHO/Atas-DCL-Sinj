#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
REMOVER DUPLICATAS - downloads_2007
===================================

Remove arquivos duplicados da pasta downloads_2007

Uso:
    python remover_duplicatas_2007_2008.py

Autor: Sistema de Automação CLDF
Data: 2025-12-22
"""

import hashlib
from pathlib import Path
from collections import defaultdict

# ======================================================================
# CONFIGURAÇÕES
# ======================================================================

USUARIO = "omega"
DIR_DOWNLOADS = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/downloads_2007")

# ======================================================================
# FUNÇÕES PRINCIPAIS
# ======================================================================

def calcular_hash_arquivo(caminho_arquivo, tamanho_bloco=65536):
    """Calcula hash MD5 de um arquivo"""
    hash_md5 = hashlib.md5()
    
    try:
        with open(caminho_arquivo, 'rb') as f:
            for bloco in iter(lambda: f.read(tamanho_bloco), b''):
                hash_md5.update(bloco)
        return hash_md5.hexdigest()
    except Exception as e:
        return None

def encontrar_duplicatas():
    """Encontra arquivos duplicados por hash"""
    print("\n" + "="*70)
    print("REMOVER DUPLICATAS - downloads_2007")
    print("="*70)
    
    # Listar todos os PDFs
    print("\n📁 LISTANDO ARQUIVOS")
    todos_pdfs = sorted(DIR_DOWNLOADS.glob('*.pdf'))
    print(f"✅ {len(todos_pdfs)} arquivos encontrados")
    
    if not todos_pdfs:
        print("❌ Nenhum arquivo PDF encontrado")
        return
    
    # Calcular hashes
    print("\n🔍 CALCULANDO HASHES (pode levar alguns minutos)...")
    print("="*70 + "\n")
    
    hashes = defaultdict(list)
    
    for i, arquivo in enumerate(todos_pdfs, 1):
        hash_arquivo = calcular_hash_arquivo(arquivo)
        
        if hash_arquivo:
            hashes[hash_arquivo].append(arquivo)
            
            if i % 50 == 0:
                print(f"[{i:3d}/{len(todos_pdfs)}] ✅ Processados")
    
    print(f"[{len(todos_pdfs):3d}/{len(todos_pdfs)}] ✅ Processados")
    
    # Encontrar duplicatas
    print("\n📊 ANALISANDO DUPLICATAS")
    print("="*70 + "\n")
    
    duplicatas = {h: arquivos for h, arquivos in hashes.items() if len(arquivos) > 1}
    
    if not duplicatas:
        print("✅ Nenhuma duplicata encontrada!")
        print(f"   Total de arquivos únicos: {len(todos_pdfs)}")
        return
    
    # Mostrar duplicatas
    print(f"⚠️  {len(duplicatas)} grupo(s) de duplicata(s) encontrado(s)\n")
    
    total_duplicatas = 0
    
    for i, (hash_arquivo, arquivos) in enumerate(duplicatas.items(), 1):
        print(f"Grupo {i}: {len(arquivos)} arquivo(s) idêntico(s)")
        
        for j, arquivo in enumerate(arquivos, 1):
            tamanho_mb = arquivo.stat().st_size / (1024 * 1024)
            print(f"  {j}. {arquivo.name} ({tamanho_mb:.1f} MB)")
        
        total_duplicatas += len(arquivos) - 1
        print()
    
    # Remover duplicatas (manter o primeiro de cada grupo)
    print("🗑️  REMOVENDO DUPLICATAS")
    print("="*70 + "\n")
    
    arquivos_removidos = 0
    tamanho_liberado_mb = 0
    
    for hash_arquivo, arquivos in duplicatas.items():
        # Manter o primeiro, remover os demais
        for arquivo in arquivos[1:]:
            try:
                tamanho_mb = arquivo.stat().st_size / (1024 * 1024)
                arquivo.unlink()
                
                print(f"✅ Removido: {arquivo.name} ({tamanho_mb:.1f} MB)")
                
                arquivos_removidos += 1
                tamanho_liberado_mb += tamanho_mb
            
            except Exception as e:
                print(f"❌ Erro ao remover {arquivo.name}: {e}")
    
    # Estatísticas finais
    print("\n📊 ESTATÍSTICAS FINAIS")
    print("="*70)
    
    arquivos_restantes = len(todos_pdfs) - arquivos_removidos
    
    print(f"   Arquivos originais:    {len(todos_pdfs)}")
    print(f"   Arquivos removidos:    {arquivos_removidos}")
    print(f"   Arquivos restantes:    {arquivos_restantes}")
    print(f"   Espaço liberado:       {tamanho_liberado_mb:.1f} MB")
    
    print(f"\n✅ LIMPEZA CONCLUÍDA!")

if __name__ == "__main__":
    encontrar_duplicatas()

