#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TESTE SIMPLES - Analisar DCL_2007-01-009.pdf
=============================================

Objetivo: Entender por que não está encontrando as atas

Uso:
    python teste_simples_dcl_009.py

Autor: Sistema de Automação CLDF
Data: 2025-12-22
"""

import re
from pathlib import Path

# ======================================================================
# CONFIGURAÇÕES
# ======================================================================

USUARIO = "omega"
DIR_DOWNLOADS = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/downloads_2007")

# Mapeamento de meses
MESES_MAP = {
    'JANEIRO': '01', 'FEVEREIRO': '02', 'MARÇO': '03', 'MARCO': '03', 'ABRIL': '04',
    'MAIO': '05', 'JUNHO': '06', 'JULHO': '07', 'AGOSTO': '08', 'SETEMBRO': '09',
    'OUTUBRO': '10', 'NOVEMBRO': '11', 'DEZEMBRO': '12'
}

# ======================================================================
# FUNÇÕES PRINCIPAIS
# ======================================================================

def instalar_dependencias():
    """Instala dependências necessárias"""
    print("📦 Verificando dependências...")
    
    import subprocess
    
    try:
        __import__("pdfplumber")
        print(f"   ✅ pdfplumber já instalado")
    except ImportError:
        print(f"   ⬇️  Instalando pdfplumber...")
        subprocess.check_call([__import__('sys').executable, "-m", "pip", "install", "pdfplumber", "-q"])
        print(f"   ✅ pdfplumber instalado")

def main():
    """Função principal"""
    print("\n" + "="*70)
    print("TESTE SIMPLES - Analisar DCL_2007-01-009.pdf")
    print("="*70)
    
    # Instalar dependências
    instalar_dependencias()
    
    arquivo = "DCL_2007-01-009.pdf"
    caminho = DIR_DOWNLOADS / arquivo
    
    print(f"\n📄 Analisando: {arquivo}")
    print("="*70)
    
    if not caminho.exists():
        print(f"❌ Arquivo não encontrado: {caminho}")
        return
    
    try:
        import pdfplumber
        
        with pdfplumber.open(caminho) as pdf:
            total_paginas = len(pdf.pages)
            print(f"\n📊 Total de páginas: {total_paginas}")
            
            lista_atas = []
            
            # Procurar por "ATA CIRCUNSTANCIADA" em todo o PDF
            for num_p, pagina in enumerate(pdf.pages, 1):
                texto_raw = (pagina.extract_text() or "").upper()
                # Normaliza espaços
                texto = " ".join(texto_raw.split())
                
                # Procura por "ATACIRCUNSTANCIADA"
                if "ATACIRCUNSTANCIADA" in texto:
                    print(f"\n✅ PÁGINA {num_p}: Encontrou ATACIRCUNSTANCIADA")
                    
                    # Procura por número de sessão
                    match_sessao = re.search(
                        r'(\d+)\s*[ªa°º]?\s*(?:\(.*?\))?\s*SESS[ÃA]O\s+(ORDIN[ÁA]RIA|EXTRAORDIN[ÁA]RIA|SOLENE|PREPARAT[ÓO]RIA|ESPECIAL)',
                        texto
                    )
                    
                    if not match_sessao:
                        match_sessao = re.search(
                            r'(\d+)[ªa°º]?\(?[A-Z]*\)?\s*SESS[ÃA]O\s*(ORDIN[ÁA]RIA|EXTRAORDIN[ÁA]RIA|SOLENE|PREPARAT[ÓO]RIA|ESPECIAL)',
                            texto
                        )
                    
                    # Procura por data
                    match_data = re.search(
                        r'(?:EM|REALIZADA)\s*(\d{1,2})\s*DE\s+(\w+)\s*DE\s+(200\d)',
                        texto
                    )
                    
                    if not match_data:
                        match_data = re.search(
                            r'(?:EM|REALIZADA)\s*(\d{1,2})\s*DE\s*(\w+)\s*DE\s*(200\d)',
                            texto
                        )
                    
                    print(f"   Sessão encontrada: {bool(match_sessao)}")
                    if match_sessao:
                        print(f"      Número: {match_sessao.group(1)}")
                        print(f"      Tipo: {match_sessao.group(2)}")
                    
                    print(f"   Data encontrada: {bool(match_data)}")
                    if match_data:
                        print(f"      Dia: {match_data.group(1)}")
                        print(f"      Mês: {match_data.group(2)}")
                        print(f"      Ano: {match_data.group(3)}")
                    
                    if match_sessao and match_data:
                        num_sessao = match_sessao.group(1).zfill(3)
                        tipo_sessao_txt = match_sessao.group(2)
                        dia, mes_ext, ano = match_data.groups()
                        
                        data_iso = f"{ano}-{MESES_MAP.get(mes_ext, '00')}-{dia.zfill(2)}"
                        
                        lista_atas.append({
                            "pag_inicio": num_p,
                            "sessao_num": num_sessao,
                            "tipo_sessao": tipo_sessao_txt,
                            "data_real": f"{dia}/{MESES_MAP.get(mes_ext, '00')}/{ano}",
                            "data_iso": data_iso
                        })
                        
                        print(f"   ✅ ATA ADICIONADA!")
            
            print(f"\n📊 TOTAL DE ATAS ENCONTRADAS: {len(lista_atas)}")
            
            for i, ata in enumerate(lista_atas, 1):
                print(f"\n   Ata {i}:")
                print(f"      Página: {ata['pag_inicio']}")
                print(f"      Sessão: {ata['sessao_num']}ª {ata['tipo_sessao']}")
                print(f"      Data: {ata['data_real']}")
                print(f"      Data ISO: {ata['data_iso']}")
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

