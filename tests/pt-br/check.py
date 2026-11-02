#!/usr/bin/env python3
"""
check.py - mede as ferramentas em português com o corpus desta pasta.

Roda de qualquer lugar:   python3 tests/pt-br/check.py

O que mede:
  1. hookscore.py separa gancho bom de gancho ruim? (média, e AUC: a chance de
     um gancho bom aleatório tirar nota maior que um ruim aleatório. 0,5 é cara
     ou coroa, 1,0 é separação perfeita.)
  2. detect.py separa legenda humana de legenda com cara de IA?
  3. O inglês continua dando as mesmas notas de antes?

Atenção: os ganchos daqui foram escritos pra testar, não tirados de reels reais.
Servem pra pegar regressão quando você mexe no léxico. Não provam que a
ferramenta acerta no mundo real. Pra isso, troque por ganchos transcritos de
reels brasileiros de verdade, com as views de cada um.
"""
import json
import os
import statistics
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "skills", "ig-reel"))
sys.path.insert(0, os.path.join(ROOT, "skills", "ig-human"))
import hookscore  # noqa: E402
import detect     # noqa: E402


def lines(name):
    return [l.strip() for l in open(os.path.join(HERE, name), encoding="utf-8") if l.strip()]


def auc(pos, neg):
    wins = sum((p > n) + 0.5 * (p == n) for p in pos for n in neg)
    return wins / (len(pos) * len(neg))


good = [hookscore.run(h)[1] for h in lines("hooks_bons.txt")]
bad = [hookscore.run(h)[1] for h in lines("hooks_ruins.txt")]
print("GANCHOS (hookscore.py)")
print(f"  bons   n={len(good):<3} média {statistics.mean(good):5.1f}   mediana {statistics.median(good):5.1f}")
print(f"  ruins  n={len(bad):<3} média {statistics.mean(bad):5.1f}   mediana {statistics.median(bad):5.1f}")
print(f"  AUC bons x ruins: {auc(good, bad):.2f}")
below = sum(b < statistics.median(good) for b in bad)
print(f"  ruins abaixo da mediana dos bons: {below}/{len(bad)}")

print("\nLEGENDAS (detect.py)")
for name in ("legenda_humana.txt", "legenda_ia.txt"):
    text = open(os.path.join(HERE, name), encoding="utf-8").read()
    lang = detect.detect_lang(text)
    _, overall, verdict = detect.run(text, detect.load_lexicon(detect.LEX, lang), lang)
    print(f"  {name:<20} {lang}  {overall:5.1f}  {verdict}")

print("\nINGLÊS (não pode mudar)")
expected = {
    "Nobody tells you that your first 30 reels are supposed to flop.": 85.6,
    "I lost $18,000 because of one missing contract.": 81.4,
    "Hey guys, today I wanted to talk about content strategy": 9.6,
}
ok = True
for hook, want in expected.items():
    got = round(hookscore.run(hook)[1], 1)
    flag = "ok" if got == want else f"MUDOU (era {want})"
    ok &= got == want
    print(f"  {got:5.1f}  {flag:<14} {hook[:52]}")
sys.exit(0 if ok else 1)
