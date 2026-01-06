"""
FASE 3: EXTRAÇÃO E RENOMEAÇÃO
Extrai páginas específicas de cada ata do DCL
Renomeia com padrão: YYYY-MM-DD-C-TT-NNN-T-TA.pdf
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
import pdfplumber
from PyPDF2 import PdfReader, PdfWriter
from extrair_data_melhorado import extrair_data_melhorado

DOWNLOADS_DIR = "downloads_2007"
DADOS_JSON = "dados_dcls_2007_enriquecidos.json"
ATAS_SAIDA = "atas_circunstanciadas_2007_fase3"
RELATORIO_EXTRACAO = "relatorio_extracao_fase3.json"

Path(ATAS_SAIDA).mkdir(exist_ok=True)

relatorio = {
    "data_execucao": datetime.now().isoformat(),
    "dcls_processados": 0,
    "atas_extraidas": 0,
    "atas_renomeadas": 0,
    "erros": [],
    "atas": []
}

def extrair_atas_do_dcl(pdf_path, metadados):
    """Extrai atas individuais de um DCL"""
    
    atas_extraidas = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Procurar por padrões de ata em cada página
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                if not text:
                    continue
                
                # Procurar por padrões de número de ata
                # Exemplo: "ATA Nº 001", "SESSÃO Nº 001", etc.
                pattern = r'(?:ATA|SESSÃO)\s+(?:Nº|N°|N)\s*(\d+)'
                matches = re.findall(pattern, text, re.IGNORECASE)
                
                for match in matches:
                    atas_extraidas.append({
                        "numero": match,
                        "pagina_inicio": page_num + 1,
                        "metadados": metadados
                    })
    
    except Exception as e:
        print(f"⚠️  Erro ao processar {os.path.basename(pdf_path)}: {e}")
    
    return atas_extraidas

def criar_nome_ata(data_sessao, tipo_sessao, numero_sessao, tipo_ata):
    """Cria nome de ata com padrão YYYY-MM-DD-C-TT-NNN-T-TA.pdf"""
    
    # Padrão: YYYY-MM-DD-C-TT-NNN-T-TA.pdf
    # C: Código tipo sessão (1=Ordinária, 2=Extraordinária, etc.)
    # TT: Tipo sessão (SO, SE, SS, SP)
    # NNN: Número sessão (001-999)
    # T: Código tipo ata (1=Sucinta, 2=Circunstanciada)
    # TA: Tipo ata (AS, AC)
    
    if not data_sessao:
        return None
    
    # Extrair ano, mês, dia
    partes = data_sessao.split('-')
    if len(partes) != 3:
        return None
    
    ano, mes, dia = partes
    
    # Determinar código tipo sessão
    codigo_tipo = "1"  # Padrão: Ordinária
    tipo_sessao_abrev = "SO"
    
    if tipo_sessao:
        if "Extraordinária" in tipo_sessao:
            codigo_tipo = "2"
            tipo_sessao_abrev = "SE"
        elif "Solene" in tipo_sessao:
            codigo_tipo = "3"
            tipo_sessao_abrev = "SS"
    
    # Número sessão com 3 dígitos
    numero_sessao_fmt = str(numero_sessao).zfill(3) if numero_sessao else "001"
    
    # Determinar código tipo ata
    codigo_ata = "2"  # Padrão: Circunstanciada
    tipo_ata_abrev = "AC"
    
    if tipo_ata:
        if "Sucinta" in tipo_ata:
            codigo_ata = "1"
            tipo_ata_abrev = "AS"
    
    nome = f"{ano}-{mes}-{dia}-{codigo_tipo}-{tipo_sessao_abrev}-{numero_sessao_fmt}-{codigo_ata}-{tipo_ata_abrev}.pdf"
    return nome

def processar_dcls():
    """Processa todos os DCLs"""

    print(f"📊 Processando DCLs para extração de atas...\n", flush=True)

    # Carregar dados enriquecidos
    if not os.path.exists(DADOS_JSON):
        print(f"❌ Arquivo {DADOS_JSON} não encontrado", flush=True)
        return
    
    with open(DADOS_JSON, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    for idx, item in enumerate(dados, 1):
        filename = item['filename']
        metadados = item['metadados']
        
        pdf_path = os.path.join(DOWNLOADS_DIR, filename)
        
        print(f"[{idx}/{len(dados)}] {filename}...", end=" ")
        
        # Extrair atas
        atas = extrair_atas_do_dcl(pdf_path, metadados)
        
        if atas:
            print(f"✅ ({len(atas)} atas)")
            relatorio["atas_extraidas"] += len(atas)
            
            # Registrar atas
            for ata in atas:
                relatorio["atas"].append({
                    "dcl": filename,
                    "numero": ata["numero"],
                    "data_sessao": metadados.get("data_sessao"),
                    "tipo_sessao": metadados.get("tipo_sessao"),
                    "tipo_ata": metadados.get("tipo_ata")
                })
        else:
            print("⚠️  Nenhuma ata encontrada")
        
        relatorio["dcls_processados"] += 1
    
    # Salvar relatório
    with open(RELATORIO_EXTRACAO, 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Processamento concluído!")
    print(f"   DCLs processados: {relatorio['dcls_processados']}")
    print(f"   Atas extraídas: {relatorio['atas_extraidas']}")
    print(f"   Relatório: {RELATORIO_EXTRACAO}")

if __name__ == "__main__":
    processar_dcls()

