# 📋 PADRÕES DE NOMENCLATURA - ATAS DCL-SINJ

**Versão:** 1.0  
**Data:** 2026-01-06

---

## 📝 PADRÃO DE NOMENCLATURA DE ARQUIVOS

### Formato Geral
```
YYYY-MM-DD-C-TT-NNN-T-TA.pdf
```

### Componentes

| Componente | Descrição | Exemplo | Notas |
|------------|-----------|---------|-------|
| **YYYY** | Ano | 2007 | 4 dígitos |
| **MM** | Mês | 01, 02, ..., 12 | 2 dígitos com zero à esquerda |
| **DD** | Dia | 01, 02, ..., 31 | 2 dígitos com zero à esquerda |
| **C** | Câmara | 1 | 1 = CLDF |
| **TT** | Tipo de Sessão | SO, SE | SO = Ordinária, SE = Extraordinária |
| **NNN** | Número da Sessão | 001, 002, ..., 096 | 3 dígitos com zeros à esquerda |
| **T** | Tipo de Documento | 2 | 2 = Ata Circunstanciada |
| **TA** | Tipo de Arquivo | AC | AC = Ata Circunstanciada |

---

## 📌 EXEMPLOS

### Ata Ordinária
```
2007-02-06-1-SO-002-2-AC.pdf
├─ Data: 06/02/2007
├─ Tipo: Ordinária (SO)
├─ Sessão: 002
└─ Tipo de Arquivo: Ata Circunstanciada (AC)
```

### Ata Extraordinária
```
2007-05-02-2-SE-002-2-AC.pdf
├─ Data: 02/05/2007
├─ Tipo: Extraordinária (SE)
├─ Sessão: 002
└─ Tipo de Arquivo: Ata Circunstanciada (AC)
```

---

## ✅ VALIDAÇÃO

### Checklist de Validação
- [x] Ano está entre 2000-2099
- [x] Mês está entre 01-12
- [x] Dia está entre 01-31
- [x] Câmara é 1
- [x] Tipo de Sessão é SO ou SE
- [x] Número da Sessão está entre 001-999
- [x] Tipo de Documento é 2
- [x] Tipo de Arquivo é AC
- [x] Extensão é .pdf

---

## 🔄 CONVERSÃO DE NOMENCLATURAS ANTIGAS

### Padrão Antigo
```
DCL_2007-03-044.pdf (arquivo original do DCL)
```

### Padrão Novo
```
2007-02-06-1-SO-002-2-AC.pdf (ata extraída)
```

### Processo de Conversão
1. Extrair ata do DCL
2. Obter data real da ata (não do DCL)
3. Obter número da sessão
4. Obter tipo de sessão (ordinária/extraordinária)
5. Aplicar padrão de nomenclatura

---

## 📊 ESTATÍSTICAS DE NOMENCLATURAS

### Atas Ordinárias
- Total esperado: 96
- Catalogadas: 86
- Faltando: 25 (1, 5, 9, 30, 37, 39, 41, 50, 57, 60, 71-83, 97, 99)

### Atas Extraordinárias
- Total esperado: 51
- Catalogadas: 20
- Faltando: 10 (1, 4, 11, 12, 15, 18, 19, 20, 22, 26)

---

## 🛠️ FERRAMENTAS DE VALIDAÇÃO

### Script Python para Validar Nomenclatura
```python
import re

def validar_nomenclatura(filename):
    pattern = r'^\d{4}-\d{2}-\d{2}-1-(SO|SE)-\d{3}-2-AC\.pdf$'
    return bool(re.match(pattern, filename))

# Exemplos
print(validar_nomenclatura('2007-02-06-1-SO-002-2-AC.pdf'))  # True
print(validar_nomenclatura('2007-05-02-2-SE-002-2-AC.pdf'))  # False (câmara 2)
```

---

**Próxima Revisão:** 2026-02-06

