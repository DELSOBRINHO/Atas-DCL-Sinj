"""
Script para extrair a data REAL da ata do conteúdo do PDF
Procura por padrões como "EM 19 DE DEZEMBRO DE 2006"
"""

import os
import re
from pathlib import Path
import pdfplumber
from datetime import datetime

def extrair_data_real_ata(pdf_path, verbose=False):
    """
    Extrai a data real da ata do conteúdo do PDF
    Procura por padrões como "EM DD DE MÊS DE YYYY"

    Retorna: (data_str, sessao_info) ou (None, None)
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Processa primeiras 5 páginas
            for page_num in range(min(5, len(pdf.pages))):
                text = pdf.pages[page_num].extract_text()
                if not text:
                    continue

                if verbose:
                    print(f"\n--- Página {page_num + 1} ---")
                    print(text[:500])

                # Padrão 1: "EM DD DE MÊS DE YYYY" (mais específico)
                pattern1 = r'EM\s+(\d{1,2})\s+DE\s+(\w+)\s+DE\s+(\d{4})'
                matches = re.findall(pattern1, text, re.IGNORECASE)

                if matches:
                    # Usar o primeiro match que for válido
                    for dia, mes_nome, ano in matches:
                        data_str = processar_data_pt(dia, mes_nome, ano)
                        if data_str:
                            sessao_info = extrair_sessao_info(text)
                            if verbose:
                                print(f"✅ Data encontrada: {data_str}")
                                print(f"   Sessão: {sessao_info}")
                            return data_str, sessao_info

                # Padrão 2: "DD DE MÊS DE YYYY" (sem "EM")
                pattern2 = r'(\d{1,2})\s+DE\s+(\w+)\s+DE\s+(\d{4})'
                matches = re.findall(pattern2, text, re.IGNORECASE)

                if matches:
                    for dia, mes_nome, ano in matches:
                        data_str = processar_data_pt(dia, mes_nome, ano)
                        if data_str:
                            sessao_info = extrair_sessao_info(text)
                            if verbose:
                                print(f"✅ Data encontrada (padrão 2): {data_str}")
                            return data_str, sessao_info

                # Padrão 3: "DD/MM/YYYY"
                pattern3 = r'(\d{1,2})/(\d{1,2})/(\d{4})'
                matches = re.findall(pattern3, text)

                if matches:
                    dia, mes, ano = matches[0]
                    data_str = f"{ano}-{int(mes):02d}-{int(dia):02d}"
                    sessao_info = extrair_sessao_info(text)
                    if verbose:
                        print(f"✅ Data encontrada (padrão 3): {data_str}")
                    return data_str, sessao_info

        if verbose:
            print(f"⚠️  Nenhuma data encontrada em {pdf_path}")
        return None, None

    except Exception as e:
        print(f"❌ Erro ao extrair data de {pdf_path}: {e}")
        return None, None

def processar_data_pt(dia, mes_nome, ano):
    """Converte data em português para formato YYYY-MM-DD"""
    meses_pt = {
        'JANEIRO': '01', 'FEVEREIRO': '02', 'MARÇO': '03',
        'ABRIL': '04', 'MAIO': '05', 'JUNHO': '06',
        'JULHO': '07', 'AGOSTO': '08', 'SETEMBRO': '09',
        'OUTUBRO': '10', 'NOVEMBRO': '11', 'DEZEMBRO': '12'
    }
    
    mes_num = meses_pt.get(mes_nome.upper())
    if mes_num:
        try:
            data_str = f"{ano}-{mes_num}-{int(dia):02d}"
            # Validar data
            datetime.strptime(data_str, "%Y-%m-%d")
            return data_str
        except:
            return None
    
    return None

def extrair_sessao_info(text):
    """Extrai informações de sessão (número, tipo)"""
    # Procura por padrões como "113a SESSÃO ORDINÁRIA"
    pattern = r'(\d+)(?:a|ª)\s+(?:CENTÉSIMA|NONAGÉSIMA|OCTOGÉSIMA|SEPTUAGÉSIMA|SEXAGÉSIMA|QUINQUAGÉSIMA|QUADRAGÉSIMA|TRIGÉSIMA|VIGÉSIMA|DÉCIMA)?\s*(?:SESSÃO|SEÇÃO)\s+(\w+)'
    matches = re.findall(pattern, text, re.IGNORECASE)
    
    if matches:
        num, tipo = matches[0]
        return f"Sessão {num} {tipo}"
    
    return None

def validar_data(data_str, mes_esperado=None, ano_esperado=None):
    """
    Valida se a data extraída é válida
    Permite atas de até 2 meses antes (para casos como dezembro de 2006)
    """
    try:
        data_obj = datetime.strptime(data_str, "%Y-%m-%d")
        
        if ano_esperado:
            # Permitir atas de até 2 meses antes
            if data_obj.year < ano_esperado - 1 or data_obj.year > ano_esperado:
                return False
        
        if mes_esperado:
            # Permitir atas do mês anterior ou do mês esperado
            mes_int = int(mes_esperado)
            if data_obj.month not in [mes_int - 1, mes_int, mes_int + 1]:
                return False
        
        return True
    except:
        return False

# Teste
if __name__ == "__main__":
    # Testar com arquivos existentes
    atas_dir = "atas_circunstanciadas_2007"
    
    if os.path.exists(atas_dir):
        print("🔍 Testando extração de data em atas existentes...\n")
        
        for arquivo in sorted(os.listdir(atas_dir))[:5]:
            if arquivo.endswith('.pdf'):
                pdf_path = os.path.join(atas_dir, arquivo)
                print(f"📄 {arquivo}")
                
                data_real, sessao = extrair_data_real_ata(pdf_path, verbose=False)
                
                if data_real:
                    print(f"   ✅ Data real: {data_real}")
                    print(f"   📋 Sessão: {sessao}")
                else:
                    print(f"   ⚠️  Data não encontrada")
                
                print()

