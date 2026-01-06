"""
Script melhorado para extrair data real da ata
Procura em todo o PDF, não apenas primeiras páginas
Trata OCR ruim
"""

import os
import re
from pathlib import Path
import pdfplumber
from datetime import datetime

def limpar_texto_ocr(text):
    """Remove caracteres de controle e lixo de OCR"""
    # Remove caracteres de controle
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    # Remove múltiplos espaços
    text = re.sub(r'\s+', ' ', text)
    return text

def extrair_data_melhorado(pdf_path, verbose=False):
    """
    Extrai data real da ata com tratamento de OCR ruim
    Procura em todo o PDF
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Processa todas as páginas
            for page_num in range(len(pdf.pages)):
                text = pdf.pages[page_num].extract_text()
                if not text:
                    continue
                
                # Limpar OCR
                text_limpo = limpar_texto_ocr(text)
                
                if verbose and page_num < 3:
                    print(f"\n--- Página {page_num + 1} (limpo) ---")
                    print(text_limpo[:300])
                
                # Padrão 1: "EM DD DE MÊS DE YYYY"
                pattern1 = r'EM\s+(\d{1,2})\s+DE\s+(\w+)\s+DE\s+(\d{4})'
                matches = re.findall(pattern1, text_limpo, re.IGNORECASE)
                
                if matches:
                    for dia, mes_nome, ano in matches:
                        data_str = processar_data_pt(dia, mes_nome, ano)
                        if data_str:
                            if verbose:
                                print(f"✅ Data encontrada (padrão 1): {data_str}")
                            return data_str
                
                # Padrão 2: "DD DE MÊS DE YYYY"
                pattern2 = r'(\d{1,2})\s+DE\s+(\w+)\s+DE\s+(\d{4})'
                matches = re.findall(pattern2, text_limpo, re.IGNORECASE)
                
                if matches:
                    for dia, mes_nome, ano in matches:
                        data_str = processar_data_pt(dia, mes_nome, ano)
                        if data_str:
                            if verbose:
                                print(f"✅ Data encontrada (padrão 2): {data_str}")
                            return data_str
                
                # Padrão 3: "DD/MM/YYYY"
                pattern3 = r'(\d{1,2})/(\d{1,2})/(\d{4})'
                matches = re.findall(pattern3, text_limpo)
                
                if matches:
                    dia, mes, ano = matches[0]
                    data_str = f"{ano}-{int(mes):02d}-{int(dia):02d}"
                    if verbose:
                        print(f"✅ Data encontrada (padrão 3): {data_str}")
                    return data_str
        
        if verbose:
            print(f"⚠️  Nenhuma data encontrada")
        return None
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

def processar_data_pt(dia, mes_nome, ano):
    """Converte data em português para YYYY-MM-DD"""
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
            datetime.strptime(data_str, "%Y-%m-%d")
            return data_str
        except:
            return None
    
    return None

# Teste
if __name__ == "__main__":
    atas_dir = "atas_circunstanciadas_2007"
    
    if os.path.exists(atas_dir):
        print("🔍 Testando extração melhorada...\n")
        
        for arquivo in sorted(os.listdir(atas_dir))[:10]:
            if arquivo.endswith('.pdf'):
                pdf_path = os.path.join(atas_dir, arquivo)
                print(f"📄 {arquivo}")
                
                data_real = extrair_data_melhorado(pdf_path, verbose=False)
                
                if data_real:
                    print(f"   ✅ Data: {data_real}")
                else:
                    print(f"   ⚠️  Data não encontrada")
                
                print()

