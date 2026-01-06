"""
Teste de extração de data com verbose
"""

import os
from extrair_data_real_ata import extrair_data_real_ata

atas_dir = "atas_circunstanciadas_2007"

if os.path.exists(atas_dir):
    print("🔍 Testando extração de data com VERBOSE...\n")
    
    # Testar com a ata que deveria ser de 2006
    arquivo_teste = "2007-02-15-1-SO-113-2-AC.pdf"
    pdf_path = os.path.join(atas_dir, arquivo_teste)
    
    if os.path.exists(pdf_path):
        print(f"📄 Testando: {arquivo_teste}")
        print(f"   Nome sugere: 2007-02-15")
        print(f"   Você disse que é: 2006-12-19\n")
        
        data_real, sessao = extrair_data_real_ata(pdf_path, verbose=True)
        
        print(f"\n✅ Resultado:")
        print(f"   Data extraída: {data_real}")
        print(f"   Sessão: {sessao}")

