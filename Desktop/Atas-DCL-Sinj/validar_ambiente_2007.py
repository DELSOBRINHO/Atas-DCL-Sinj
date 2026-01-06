# -*- coding: utf-8 -*-
"""
VALIDADOR DE AMBIENTE - Extração de Atas 2007
==============================================

Verifica se o ambiente está configurado corretamente para executar
o script de extração de atas circunstanciadas.

Uso:
    python validar_ambiente_2007.py
"""

import sys
import os
from pathlib import Path

print("="*70)
print("VALIDADOR DE AMBIENTE - EXTRAÇÃO DE ATAS 2007")
print("="*70)

# Configurações
USUARIO = "omega"
ONEDRIVE_NAME = "OneDrive - Câmara Legislativa do Distrito Federal - CLDF"
BASE_PATH = Path(f"C:/Users/{USUARIO}/{ONEDRIVE_NAME}")
PASTA_BASE = 'Cadernos_Anais_CLDF'

erros = []
avisos = []
sucessos = []

# 1. Verificar Python
print("\n1️⃣  Verificando Python...")
try:
    versao = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"   ✅ Python {versao}")
    sucessos.append(f"Python {versao}")
except Exception as e:
    erros.append(f"Erro ao verificar Python: {e}")

# 2. Verificar dependências
print("\n2️⃣  Verificando dependências Python...")
dependencias = {
    'requests': 'Requisições HTTP',
    'bs4': 'BeautifulSoup4 (parsing HTML)',
    'pdfplumber': 'Extração de texto de PDFs',
    'PyPDF2': 'Manipulação de PDFs',
}

for modulo, descricao in dependencias.items():
    try:
        __import__(modulo)
        print(f"   ✅ {modulo}: {descricao}")
        sucessos.append(f"Módulo {modulo}")
    except ImportError:
        msg = f"Módulo {modulo} não instalado: {descricao}"
        print(f"   ❌ {msg}")
        erros.append(msg)

# 3. Verificar OneDrive
print("\n3️⃣  Verificando OneDrive...")
if BASE_PATH.exists():
    print(f"   ✅ OneDrive encontrado: {BASE_PATH}")
    sucessos.append("OneDrive")
else:
    msg = f"OneDrive não encontrado em: {BASE_PATH}"
    print(f"   ❌ {msg}")
    erros.append(msg)

# 4. Verificar estrutura de pastas
print("\n4️⃣  Verificando estrutura de pastas...")
pasta_estrutura = BASE_PATH / PASTA_BASE / "05_Legislatura_2007-2010" / "Cadernos_PDF" / "PDFs_Individuais" / "2007"

if pasta_estrutura.exists():
    print(f"   ✅ Estrutura de pastas criada")
    sucessos.append("Estrutura de pastas")
else:
    msg = f"Estrutura de pastas não encontrada. Execute: python cria_estrutura_pastas_local.py"
    print(f"   ⚠️  {msg}")
    avisos.append(msg)

# 5. Verificar diretórios de trabalho
print("\n5️⃣  Verificando diretórios de trabalho...")
dir_downloads = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/downloads_2007")
dir_processados = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/processados_2007")

for diretorio, nome in [(dir_downloads, "downloads_2007"), (dir_processados, "processados_2007")]:
    if diretorio.exists():
        print(f"   ✅ {nome} existe")
        sucessos.append(f"Diretório {nome}")
    else:
        print(f"   ℹ️  {nome} será criado automaticamente")
        avisos.append(f"Diretório {nome} será criado na primeira execução")

# 6. Verificar conectividade
print("\n6️⃣  Verificando conectividade...")
try:
    import requests
    response = requests.head("https://www.sinj.df.gov.br", timeout=5)
    if response.status_code < 500:
        print(f"   ✅ SINJ-DF acessível")
        sucessos.append("Conectividade SINJ-DF")
    else:
        msg = f"SINJ-DF retornou status {response.status_code}"
        print(f"   ⚠️  {msg}")
        avisos.append(msg)
except Exception as e:
    msg = f"Erro ao acessar SINJ-DF: {e}"
    print(f"   ❌ {msg}")
    erros.append(msg)

# 7. Verificar espaço em disco
print("\n7️⃣  Verificando espaço em disco...")
try:
    import shutil
    disco = shutil.disk_usage(Path.home())
    livre_gb = disco.free / (1024**3)
    if livre_gb > 5:
        print(f"   ✅ Espaço disponível: {livre_gb:.1f} GB")
        sucessos.append("Espaço em disco")
    else:
        msg = f"Espaço em disco baixo: {livre_gb:.1f} GB (mínimo 5 GB recomendado)"
        print(f"   ⚠️  {msg}")
        avisos.append(msg)
except Exception as e:
    print(f"   ⚠️  Não foi possível verificar espaço: {e}")

# Resumo
print("\n" + "="*70)
print("RESUMO DA VALIDAÇÃO")
print("="*70)

print(f"\n✅ Sucessos: {len(sucessos)}")
for sucesso in sucessos:
    print(f"   • {sucesso}")

if avisos:
    print(f"\n⚠️  Avisos: {len(avisos)}")
    for aviso in avisos:
        print(f"   • {aviso}")

if erros:
    print(f"\n❌ Erros: {len(erros)}")
    for erro in erros:
        print(f"   • {erro}")
    print("\n❌ AMBIENTE NÃO ESTÁ PRONTO")
    print("\nResolva os erros acima antes de executar o script principal.")
    sys.exit(1)
else:
    print("\n✅ AMBIENTE VALIDADO COM SUCESSO!")
    print("\nVocê pode executar: python 01_extrair_atas_sinj_2007.py")
    sys.exit(0)

