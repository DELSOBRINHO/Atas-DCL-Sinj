#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Corrige a data de publicação da ata extraindo do cabeçalho do DCL.
A data de publicação é a data do DCL (não a data da sessão).
"""

import json
import re
import os
import fitz  # PyMuPDF

# Mapa de meses
MESES = {
    'janeiro': '01', 'fevereiro': '02', 'março': '03', 'marco': '03',
    'abril': '04', 'maio': '05', 'junho': '06',
    'julho': '07', 'agosto': '08', 'setembro': '09',
    'outubro': '10', 'novembro': '11', 'dezembro': '12'
}

def extrair_data_cabecalho_dcl(pdf_path):
    """
    Extrai a data de publicação do cabeçalho do DCL.
    Procura padrões como: "N°44, Brasília, quinta-feira, 8demarçode2007"
    """
    try:
        doc = fitz.open(pdf_path)
        
        # Verificar apenas as primeiras páginas
        for page_num in range(min(3, doc.page_count)):
            page = doc[page_num]
            texto = page.get_text()
            
            # Padrão 1: "DDdemêsdeAAAA" (sem espaços)
            match = re.search(r'(\d{1,2})de(\w+)de(\d{4})', texto, re.IGNORECASE)
            if match:
                dia = match.group(1).zfill(2)
                mes_nome = match.group(2).lower()
                ano = match.group(3)
                mes = MESES.get(mes_nome)
                if mes:
                    doc.close()
                    return f"{dia}/{mes}/{ano}"
            
            # Padrão 2: "DD de mês de AAAA" (com espaços)
            match = re.search(r'(\d{1,2})\s*de\s*(\w+)\s*de\s*(\d{4})', texto, re.IGNORECASE)
            if match:
                dia = match.group(1).zfill(2)
                mes_nome = match.group(2).lower()
                ano = match.group(3)
                mes = MESES.get(mes_nome)
                if mes:
                    doc.close()
                    return f"{dia}/{mes}/{ano}"
        
        doc.close()
    except Exception as e:
        print(f"  ⚠️ Erro ao ler {os.path.basename(pdf_path)}: {e}")
    
    return None

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'fase2_atas_2007_final.json')
    downloads_dir = os.path.join(script_dir, 'downloads_2007')
    
    print("=" * 70)
    print("CORRIGIR DATA DE PUBLICAÇÃO DA ATA")
    print("=" * 70)
    
    # Carregar JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        atas = json.load(f)
    
    print(f"\n📋 Total de atas: {len(atas)}")
    
    # Identificar DCLs únicos
    dcls_unicos = set(ata['dcl_original'] for ata in atas)
    print(f"📁 DCLs únicos: {len(dcls_unicos)}")
    
    # Extrair data de cada DCL
    datas_dcl = {}
    print("\n🔍 Extraindo datas dos cabeçalhos dos DCLs...")
    
    for dcl in sorted(dcls_unicos):
        pdf_path = os.path.join(downloads_dir, dcl)
        if os.path.exists(pdf_path):
            data = extrair_data_cabecalho_dcl(pdf_path)
            if data:
                datas_dcl[dcl] = data
                print(f"  ✅ {dcl}: {data}")
            else:
                print(f"  ❌ {dcl}: Data não encontrada no cabeçalho")
        else:
            print(f"  ⚠️ {dcl}: Arquivo não encontrado")
    
    # Atualizar atas com datas corretas
    print(f"\n📝 Atualizando {len(atas)} atas...")
    atualizadas = 0
    nao_encontradas = 0
    
    for ata in atas:
        dcl = ata['dcl_original']
        if dcl in datas_dcl:
            ata['data_publicacao_ata'] = datas_dcl[dcl]
            atualizadas += 1
        else:
            ata['data_publicacao_ata'] = 'N/A'
            nao_encontradas += 1
    
    # Salvar JSON atualizado
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(atas, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'=' * 70}")
    print(f"RESULTADO")
    print(f"{'=' * 70}")
    print(f"✅ Atas atualizadas: {atualizadas}")
    print(f"❌ Sem data encontrada: {nao_encontradas}")
    print(f"💾 JSON salvo: fase2_atas_2007_final.json")

if __name__ == "__main__":
    main()

