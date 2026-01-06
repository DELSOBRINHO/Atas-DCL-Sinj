"""
Script para buscar DCLs no SINJ-DF usando requests + BeautifulSoup
Mais confiável que Selenium
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote
from extrair_data_melhorado import extrair_data_melhorado

# Configuração
SINJ_BASE_URL = "https://www.sinj.df.gov.br/sinj/Consulta/Diario.html"
SINJ_SEARCH_URL = "https://www.sinj.df.gov.br/sinj/Consulta/Diario.html"
DOWNLOADS_DIR = "downloads_2007_novos"
ATAS_DIR = "atas_circunstanciadas_2007_validadas"
RELATORIO_FILE = "relatorio_busca_sinj_requests.json"

Path(DOWNLOADS_DIR).mkdir(exist_ok=True)
Path(ATAS_DIR).mkdir(exist_ok=True)

MESES = {
    "Janeiro": "01", "Fevereiro": "02", "Março": "03", "Abril": "04",
    "Maio": "05", "Junho": "06", "Julho": "07", "Agosto": "08",
    "Setembro": "09", "Outubro": "10", "Novembro": "11", "Dezembro": "12"
}

relatorio = {
    "data_execucao": datetime.now().isoformat(),
    "dcls_baixados": 0,
    "atas_encontradas": 0,
    "erros": []
}

def buscar_dcls_requests(mes_nome, ano):
    """Busca DCLs usando requests"""
    try:
        # Parâmetros da busca
        params = {
            "tipoDiario": "DCL",
            "ano": str(ano),
            "mes": mes_nome
        }

        print(f"  🔍 Buscando DCLs em {mes_nome}/{ano}...")

        # Fazer requisição (desabilitar verificação SSL)
        response = requests.get(SINJ_SEARCH_URL, params=params, timeout=30, verify=False)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(f"  ⚠️  Status {response.status_code}")
            return []
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Procurar por links de download
        links = []
        for link in soup.find_all('a'):
            href = link.get('href', '')
            if 'download' in href.lower():
                full_url = urljoin(SINJ_BASE_URL, href)
                links.append(full_url)
        
        print(f"  ✅ Encontrados {len(links)} DCLs")
        return links
    
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        relatorio["erros"].append(f"Busca {mes_nome}: {str(e)}")
        return []

def baixar_dcl(url, mes, ano):
    """Baixa um DCL"""
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            # Extrair nome do arquivo
            filename = unquote(url.split('/')[-1])
            if not filename.endswith('.pdf'):
                filename = f"DCL_{ano}_{mes}_{int(time.time())}.pdf"
            
            filepath = os.path.join(DOWNLOADS_DIR, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            relatorio["dcls_baixados"] += 1
            return filepath
    except Exception as e:
        print(f"    ⚠️  Erro ao baixar: {e}")
        relatorio["erros"].append(f"Download: {str(e)}")
    
    return None

def processar_dcl(pdf_path):
    """Processa um DCL"""
    try:
        data_real = extrair_data_melhorado(pdf_path, verbose=False)
        
        if not data_real:
            print(f"    ⚠️  Data não encontrada")
            return False
        
        print(f"    ✅ Data: {data_real}")
        relatorio["atas_encontradas"] += 1
        return True
    
    except Exception as e:
        print(f"    ❌ Erro: {e}")
        relatorio["erros"].append(f"Processamento: {str(e)}")
        return False

# Executar busca
print("🔍 Iniciando busca de DCLs no SINJ-DF (usando requests)...")
print(f"Período: Janeiro a Dezembro de 2007\n")

for mes_nome, mes_num in list(MESES.items())[:3]:  # Testar com 3 meses
    print(f"\n📅 {mes_nome}/2007")
    
    try:
        # Buscar DCLs
        links = buscar_dcls_requests(mes_nome, 2007)
        
        # Baixar e processar cada DCL
        for i, link in enumerate(links[:2], 1):  # Limitar a 2 por mês
            print(f"  [{i}/{min(2, len(links))}] Baixando...")
            pdf_path = baixar_dcl(link, mes_num, 2007)
            
            if pdf_path:
                processar_dcl(pdf_path)
        
        time.sleep(1)
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        relatorio["erros"].append(f"Mês {mes_nome}: {str(e)}")

# Salvar relatório
with open(RELATORIO_FILE, 'w', encoding='utf-8') as f:
    json.dump(relatorio, f, indent=2, ensure_ascii=False)

print(f"\n✅ Busca concluída!")
print(f"   DCLs baixados: {relatorio['dcls_baixados']}")
print(f"   Atas encontradas: {relatorio['atas_encontradas']}")
print(f"   Relatório: {RELATORIO_FILE}")

