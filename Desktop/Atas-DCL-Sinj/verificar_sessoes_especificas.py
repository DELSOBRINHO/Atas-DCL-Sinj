#!/usr/bin/env python3
import json

with open('fase2_atas_2007_final.json', 'r', encoding='utf-8') as f:
    atas = json.load(f)

# Verificar sessões específicas mencionadas
sessoes_verificar = [
    ('001', 'ORDINÁRIA'),
    ('002', 'ORDINÁRIA'),  # Há múltiplas, vamos mostrar todas
    ('002', 'EXTRAORDINÁRIA'),
    ('032', 'ORDINÁRIA'),
    ('033', 'ORDINÁRIA'),
    ('034', 'ORDINÁRIA'),
    ('035', 'ORDINÁRIA'),
    ('038', 'ORDINÁRIA'),
]

print("=" * 100)
print("VERIFICAÇÃO DAS SESSÕES ESPECÍFICAS")
print("=" * 100)
print(f"{'Sessão':>6} | {'Tipo':^15} | {'Data Real':^12} | {'Págs':^10} | {'DCL Original':^30}")
print("-" * 100)

for ata in sorted(atas, key=lambda x: (x['tipo_sessao'], int(str(x['sessao_num'])))):
    sessao = str(ata['sessao_num']).zfill(3)
    for s, t in sessoes_verificar:
        if sessao.lstrip('0') == s.lstrip('0') or sessao == s:
            if t in ata['tipo_sessao']:
                print(f"{ata['sessao_num']:>6} | {ata['tipo_sessao']:^15} | {ata['data_real']:^12} | {ata['pag_inicio']:>4}-{ata['pag_fim']:<4} | {ata['dcl_original']}")
                break

print("\n" + "=" * 100)
print("EXPECTATIVAS DO USUÁRIO VS RESULTADO")
print("=" * 100)

expectativas = [
    ("001", "ORDINÁRIA", "10-22", "Sessão 1 deveria terminar na 22"),
    ("002", "ORDINÁRIA", "22-25", "Sessão 2 ordinária deveria terminar na 25"),
    ("002", "EXTRAORDINÁRIA", "1-4", "Sessão 2 extraordinária deveria terminar na 4"),
    ("032", "ORDINÁRIA", "1-13", "Sessão 32 termina na 13 (próxima sessão começa na 14)"),
    ("033", "ORDINÁRIA", "14-19", "Sessão 33 deveria terminar na 19"),
    ("034", "ORDINÁRIA", "19-32", "Sessão 34 deveria terminar na 32"),
    ("038", "ORDINÁRIA", "4-11", "Sessão 38 deveria terminar na 11"),
]

for sessao, tipo, esperado, descricao in expectativas:
    for ata in atas:
        s = str(ata['sessao_num']).zfill(3)
        if (s.lstrip('0') == sessao.lstrip('0') or s == sessao) and tipo in ata['tipo_sessao']:
            atual = f"{ata['pag_inicio']}-{ata['pag_fim']}"
            status = "✅" if atual == esperado else "❌"
            print(f"{status} Sessão {sessao} ({tipo}): {atual} (esperado: {esperado}) - {descricao}")
            break

