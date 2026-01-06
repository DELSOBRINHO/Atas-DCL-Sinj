#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORRIGIR - Datas problemáticas e sessões > 117
===============================================

Objetivo: 
1. Corrigir datas com mês 00 (extrair data correta do PDF)
2. Remover atas com número de sessão > 117 (não são atas circunstanciadas válidas)
3. Corrigir encoding de "EXTRAORDINARIA" para "EXTRAORDINÁRIA"

Uso:
    python corrigir_datas_e_sessoes.py

Autor: Sistema de Automação CLDF
Data: 2025-12-22
"""

import json
import re
from pathlib import Path

# ======================================================================
# CONFIGURAÇÕES
# ======================================================================

USUARIO = "omega"
DIR_DOWNLOADS = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/downloads_2007")
ARQUIVO_JSON_ENTRADA = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_todas_atas_346_dcls.json")
ARQUIVO_JSON_SAIDA = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_corrigidas_117.json")
ARQUIVO_TXT_SAIDA = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_corrigidas_117.txt")

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
    import subprocess
    try:
        __import__("pdfplumber")
    except ImportError:
        subprocess.check_call([__import__('sys').executable, "-m", "pip", "install", "pdfplumber", "-q"])

def extrair_data_correta_pdf(dcl_arquivo, pag_inicio):
    """Extrai a data correta do PDF para uma ata específica"""
    import pdfplumber

    caminho = DIR_DOWNLOADS / dcl_arquivo

    if not caminho.exists():
        return None

    try:
        with pdfplumber.open(caminho) as pdf:
            if pag_inicio > len(pdf.pages):
                return None

            pagina = pdf.pages[pag_inicio - 1]
            texto_raw = (pagina.extract_text() or "").upper()
            texto = " ".join(texto_raw.split())

            # Procurar por data com padrão mais flexível
            # Tenta: "EM 4 DEZEMBRO DE 2007" ou "EM4DEZEMBRO DE2007" ou "EM 5 ZEMBRO 2007"
            match_data = re.search(
                r'(?:EM|REALIZADA)\s*(\d{1,2})\s*DE\s*(\w+)\s*DE\s*(200\d)',
                texto
            )

            if match_data:
                dia, mes_ext, ano = match_data.groups()
                # Tentar encontrar o mês mesmo com OCR ruim
                mes = None
                for mes_completo, mes_num in MESES_MAP.items():
                    if mes_ext in mes_completo or mes_completo in mes_ext:
                        mes = mes_num
                        break

                if mes:
                    return f"{ano}-{mes}-{dia.zfill(2)}", f"{dia}/{mes}/{ano}"

    except Exception as e:
        print(f"❌ Erro ao extrair data de {dcl_arquivo}: {e}")

    return None

def main():
    """Função principal"""
    print("\n" + "="*70)
    print("CORRIGIR - Datas problemáticas e sessões > 117")
    print("="*70)
    
    # Instalar dependências
    instalar_dependencias()
    
    # Carregar JSON
    with open(ARQUIVO_JSON_ENTRADA, 'r', encoding='utf-8') as f:
        atas = json.load(f)
    
    print(f"\nTotal de atas antes da correção: {len(atas)}")
    
    # Filtrar e corrigir
    atas_corrigidas = []
    removidas = []
    
    for ata in atas:
        # Corrigir encoding
        ata['tipo_sessao'] = ata['tipo_sessao'].replace('EXTRAORDINARIA', 'EXTRAORDINÁRIA')
        
        # Verificar número de sessão
        try:
            num_sessao = int(ata['sessao_num'])
            if num_sessao > 117:
                removidas.append(ata)
                continue
        except:
            pass
        
        # Corrigir datas com mês 00
        if "-00-" in ata['nomenclatura']:
            print(f"\n🔧 Corrigindo data de {ata['dcl_original']} (sessão {ata['sessao_num']})")
            
            resultado = extrair_data_correta_pdf(ata['dcl_original'], ata['pag_inicio'])
            
            if resultado:
                data_iso, data_real = resultado
                ata['nomenclatura'] = ata['nomenclatura'].replace('-00-', f"-{data_iso.split('-')[1]}-")
                ata['data_real'] = data_real
                print(f"   ✅ Corrigida para: {data_real}")
            else:
                print(f"   ⚠️  Não foi possível corrigir, mantendo como SEM DATA")
                ata['data_real'] = "SEM DATA"
        
        atas_corrigidas.append(ata)
    
    print(f"\n📊 RESUMO DA CORREÇÃO:")
    print("="*70)
    print(f"   Total antes: {len(atas)}")
    print(f"   Removidas (sessão > 117): {len(removidas)}")
    print(f"   Total após: {len(atas_corrigidas)}")
    
    # Salvar JSON corrigido
    with open(ARQUIVO_JSON_SAIDA, 'w', encoding='utf-8') as f:
        json.dump(atas_corrigidas, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ JSON salvo em: {ARQUIVO_JSON_SAIDA}")
    
    # Salvar TXT formatado
    with open(ARQUIVO_TXT_SAIDA, 'w', encoding='utf-8') as f:
        f.write("FASE 2 - ATAS CIRCUNSTANCIADAS CORRIGIDAS (117 ATAS)\n")
        f.write("="*70 + "\n\n")
        
        f.write(f"Total de atas encontradas: {len(atas_corrigidas)}\n\n")
        
        f.write("Nome da Sessão,Tipo de Ata,Data da Sessão,Pág. Inicial,Pág. Final,Nomenclatura Padrão\n")
        
        for ata in atas_corrigidas:
            tipo_sessao = ata['tipo_sessao']
            data = ata['data_real']
            pag_ini = ata['pag_inicio']
            pag_fim = ata['pag_fim']
            nomenclatura = ata['nomenclatura']
            sessao_num = ata['sessao_num']
            
            f.write(f"{sessao_num}ª {tipo_sessao},Circunstanciada,{data},{pag_ini},{pag_fim},{nomenclatura}\n")
    
    print(f"✅ TXT salvo em: {ARQUIVO_TXT_SAIDA}")
    
    print(f"\n✅ CORREÇÃO CONCLUÍDA!")

if __name__ == "__main__":
    main()

