#!/usr/bin/env python3
import csv
from pathlib import Path

USUARIO = "omega"
ARQUIVO_CSV = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/atas_faltantes_para_buscar.csv")

# Mapa de datas das atas sucintas
datas_sucintas = {
    1: "04/04/2007", 2: "02/05/2007", 3: "02/05/2007", 4: "03/05/2007",
    5: "09/05/2007", 6: "10/05/2007", 7: "16/05/2007", 8: "16/05/2007",
    9: "06/06/2007", 10: "13/06/2007", 11: "19/06/2007", 12: "27/06/2007",
    13: "29/06/2007", 14: "29/06/2007", 15: "02/10/2007", 16: "12/09/2007",
    17: "13/09/2007", 18: "18/09/2007", 19: "19/09/2007", 20: "27/09/2007",
    21: "02/10/2007", 22: "17/10/2007", 23: "18/10/2007", 24: "23/10/2007",
    25: "25/10/2007", 26: "31/10/2007", 27: "13/11/2007", 28: "27/11/2007",
    29: "28/11/2007", 30: "29/11/2007", 31: "04/12/2007", 32: "05/12/2007",
    33: "11/12/2007", 34: "12/12/2007", 35: "13/12/2007", 36: "14/12/2007",
    37: "14/12/2007", 38: "15/12/2007",
}

datas_ordinarias = {
    5: "13/02/2007", 8: "22/02/2007", 9: "27/02/2007", 22: "28/03/2007",
    37: "08/05/2007", 39: "10/05/2007", 41: "16/05/2007", 50: "06/06/2007",
    57: "26/06/2007", 60: "01/08/2007", 71: "28/08/2007", 72: "29/08/2007",
    73: "30/08/2007", 74: "04/09/2007", 75: "05/09/2007", 76: "06/09/2007",
    77: "11/09/2007", 78: "12/09/2007", 79: "13/09/2007", 80: "18/09/2007",
    81: "19/09/2007", 82: "20/09/2007", 83: "25/09/2007", 84: "26/09/2007",
    85: "27/09/2007", 86: "02/10/2007", 97: "25/10/2007", 99: "31/10/2007",
    107: "21/11/2007", 110: "28/11/2007", 112: "04/12/2007", 113: "05/12/2007",
    114: "06/12/2007", 115: "11/12/2007", 116: "12/12/2007", 117: "13/12/2007",
}

# Gerar CSV
with open(ARQUIVO_CSV, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f, delimiter=';')
    
    # Cabeçalho
    writer.writerow(['Tipo', 'Numero', 'Data', 'Status', 'Observacoes'])
    
    # EXTRAORDINÁRIAS
    extraordinarias_faltantes = [1, 4, 11, 12, 15, 19, 20, 26, 31, 32, 33, 34, 35, 36, 37, 38]
    for num in extraordinarias_faltantes:
        data = datas_sucintas.get(num, "")
        writer.writerow([
            'EXTRAORDINÁRIA',
            f'{num:02d}',
            data,
            'FALTANDO',
            'Procurar no site da CLDF'
        ])
    
    # ORDINÁRIAS
    ordinarias_faltantes = [5, 8, 9, 22, 37, 39, 41, 50, 57, 60, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 97, 99, 107, 110, 112, 113, 114, 115, 116, 117]
    for num in ordinarias_faltantes:
        data = datas_ordinarias.get(num, "")
        writer.writerow([
            'ORDINÁRIA',
            f'{num:03d}',
            data,
            'FALTANDO',
            'Procurar no site da CLDF'
        ])

print(f"✅ Arquivo gerado: {ARQUIVO_CSV.name}")
print(f"   Total de atas faltantes: {len(extraordinarias_faltantes) + len(ordinarias_faltantes)}")

