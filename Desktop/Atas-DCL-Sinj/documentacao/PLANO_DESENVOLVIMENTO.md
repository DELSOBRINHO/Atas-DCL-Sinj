# 📋 PLANO DE DESENVOLVIMENTO - ATAS DCL-SINJ 2007

**Versão:** 1.0  
**Data de Criação:** 2026-01-06  
**Última Atualização:** 2026-01-06  
**Status:** Em Progresso

---

## 📊 VISÃO GERAL DO PROJETO

### Objetivo
Catalogar, validar e organizar todas as Atas Circunstanciadas da Câmara Legislativa do Distrito Federal (CLDF) do ano de 2007.

### Escopo
- **Total de Atas Esperadas:** ~147 (96 ordinárias + 51 extraordinárias)
- **Atas Catalogadas Atualmente:** 111 (87 ordinárias + 22 extraordinárias)
- **Atas Faltando:** 32 (24 ordinárias + 8 extraordinárias)

---

## 🎯 FASES DO PROJETO

### **FASE 1: Extração de DCLs** ✅ CONCLUÍDA
- [x] Baixar DCLs de 2007 do SINJ
- [x] Organizar arquivos localmente
- [x] Criar índice de DCLs

### **FASE 2: Catalogação e Limpeza de Dados** 🔄 EM PROGRESSO
- [x] Extrair metadados das atas (sessão, data, páginas)
- [x] Remover duplicatas (10 removidas)
- [x] Adicionar atas faltantes (84, 85, 86 adicionadas)
- [x] Adicionar ata 001 (01/02/2007 - Pág 10-22)
- [x] Adicionar atas 20, 21 extraordinárias (27/09/2007 e 02/10/2007)
- [x] Corrigir páginas finais (101, 104, 106, 107, 110, 111)
- [ ] Conferência manual completa de todas as 111 atas
- [ ] Procurar e adicionar 32 atas faltantes
- [ ] Corrigir páginas finais das atas 61-70, 104, 108, 109 (ord) e 16, 17 (ext)

### **FASE 3: Extração e Renomeação** ⏳ PENDENTE
- [ ] Extrair PDFs individuais dos DCLs
- [ ] Renomear com nomenclatura padrão (YYYY-MM-DD-C-TT-NNN-T-TA.pdf)
- [ ] Validar nomenclaturas

### **FASE 4: Processamento OCR** ⏳ PENDENTE
- [ ] Processar OCR dos PDFs
- [ ] Validar qualidade do OCR
- [ ] Corrigir erros de reconhecimento

### **FASE 5: Indexação e Disponibilização** ⏳ PENDENTE
- [ ] Criar índice de busca
- [ ] Disponibilizar dados em formato aberto
- [ ] Criar interface de consulta

---

## 📈 PROGRESSO GERAL

```
Fase 1: ████████████████████ 100% ✅
Fase 2: ██████████████░░░░░░  67% 🔄
Fase 3: ░░░░░░░░░░░░░░░░░░░░   0% ⏳
Fase 4: ░░░░░░░░░░░░░░░░░░░░   0% ⏳
Fase 5: ░░░░░░░░░░░░░░░░░░░░   0% ⏳
```

---

## 📋 CHECKLIST DE TAREFAS - FASE 2

### Subtarefas Concluídas ✅
- [x] Remover 10 duplicatas identificadas
- [x] Adicionar atas 84, 85, 86
- [x] Corrigir páginas finais de 6 atas
- [x] Gerar relatório XLSX atualizado
- [x] Criar sistema de versionamento de relatórios

### Subtarefas em Progresso 🔄
- [ ] Conferência manual de todas as 108 atas
- [ ] Validação de datas reais
- [ ] Validação de números de páginas

### Subtarefas Pendentes ⏳
- [ ] Procurar 25 atas ordinárias faltantes
- [ ] Procurar 10 atas extraordinárias faltantes
- [ ] Corrigir páginas finais das atas 61-70
- [ ] Corrigir páginas finais das atas 104, 108, 109
- [ ] Corrigir páginas finais das atas extraordinárias 16, 17

---

## 📁 ESTRUTURA DE ARQUIVOS

```
documentacao/
├── PLANO_DESENVOLVIMENTO.md          (Este arquivo)
├── CHECKLIST_TAREFAS.md              (Checklist detalhado)
├── relatorios_conferencia/
│   ├── v1.0_2026-01-06.xlsx          (Versão inicial)
│   ├── v1.1_2026-01-06.xlsx          (Versão com validações)
│   └── CHANGELOG.md                  (Histórico de versões)
└── PADROES_NOMENCLATURA.md           (Padrão de nomenclatura)
```

---

## 🔄 SISTEMA DE VERSIONAMENTO

Cada relatório de conferência será versionado com:
- **Formato:** `v{MAJOR}.{MINOR}_{YYYY-MM-DD}.xlsx`
- **Exemplo:** `v1.0_2026-01-06.xlsx`
- **Changelog:** Registrar todas as mudanças em CHANGELOG.md

---

## 📞 CONTATOS E REFERÊNCIAS

- **Responsável:** DELMIR BARTOLOMEU SOBRINHO
- **Repositório:** https://github.com/DELSOBRINHO/Atas-DCL-Sinj
- **Fonte de Dados:** SINJ-DF (Sistema de Informações Normativas do Judiciário)

---

**Próxima Revisão:** 2026-01-13

