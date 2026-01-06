#!/usr/bin/env python3
import csv
from pathlib import Path

USUARIO = "omega"
ARQUIVO_CSV = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/atas_faltantes_para_buscar_atualizado.csv")

# Atas ainda faltando
ordinarias_faltando = [39, 41, 57, 60, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 97, 99, 115, 116, 117]
extraordinarias_faltando = []

# Datas das atas sucintas (para referência)
datas_ordinarias = {
    37: "08/05/2007", 39: "10/05/2007", 41: "16/05/2007", 57: "26/06/2007",
    60: "01/08/2007", 71: "28/08/2007", 72: "29/08/2007", 73: "30/08/2007",
    74: "04/09/2007", 75: "05/09/2007", 76: "06/09/2007", 77: "11/09/2007",
    78: "12/09/2007", 79: "13/09/2007", 80: "18/09/2007", 81: "19/09/2007",
    82: "20/09/2007", 83: "25/09/2007", 84: "26/09/2007", 85: "27/09/2007",
    86: "02/10/2007", 97: "25/10/2007", 99: "31/10/2007", 112: "04/12/2007",
    113: "05/12/2007", 114: "06/12/2007", 115: "11/12/2007", 116: "12/12/2007",
    117: "13/12/2007"
}

datas_extraordinarias = {37: "14/12/2007"}

# Gerar CSV
with open(ARQUIVO_CSV, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f, delimiter=';')
    
    # Cabeçalho
    writer.writerow(['Tipo', 'Numero', 'Data', 'Status', 'Observacoes'])
    
    # EXTRAORDINÁRIAS
    for num in extraordinarias_faltando:
        data = datas_extraordinarias.get(num, "")
        writer.writerow([
            'EXTRAORDINÁRIA',
            f'{num:02d}',
            data,
            'FALTANDO',
            'Procurar no site da CLDF'
        ])
    
    # ORDINÁRIAS
    for num in ordinarias_faltando:
        data = datas_ordinarias.get(num, "")
        writer.writerow([
            'ORDINÁRIA',
            f'{num:03d}',
            data,
            'FALTANDO',
            'Procurar no site da CLDF'
        ])

print(f"✅ Arquivo gerado: {ARQUIVO_CSV.name}")
print(f"   Total de atas faltantes: {len(ordinarias_faltando) + len(extraordinarias_faltando)}")

