#!/usr/bin/env python3
"""
detect.py - a five-check panel that scores how machine-written a draft looks.

What this is:  five local heuristics modelled on the signals public AI
detectors actually measure - sentence-length variation, concreteness, stock
vocabulary, typographic fingerprint, and voice. Every score is computed on
your machine from the text alone. Nothing is uploaded.

What this is NOT:  GPTZero, Originality, Copyleaks, Winston or Turnitin.
It does not call their APIs and it cannot promise their verdict. It catches
the things they all key on, which is why fixing them tends to move their
numbers too - but the only honest claim is the one on this line.

Each check returns a HUMAN score from 0 to 100. Higher is better.

Usage
  python3 detect.py draft.txt
  pbpaste | python3 detect.py -
  python3 detect.py draft.txt --json
  python3 detect.py before.txt after.txt      # compare two drafts
  python3 detect.py draft.txt --lang pt       # force Portuguese (default: auto)

Languages:  English and Brazilian Portuguese, detected from the text. In
Portuguese the lexicon is slop.pt.json, "contractions" become the marks of
spoken Brazilian Portuguese (tá, tô, pra, né, cê, a gente), and first person
counts verb endings too, because Portuguese drops the "eu".
"""

import argparse
import json
import os
import re
import statistics
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "slop.json")
LEX_PT = os.path.join(HERE, "slop.pt.json")

SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")
WORD_RE = re.compile(r"[A-Za-z']+")
CONTRACTIONS = re.compile(r"\b\w+'(?:s|t|re|ve|ll|d|m)\b", re.IGNORECASE)
PRONOUNS = re.compile(r"\b(i|me|my|mine|we|us|our|you|your)\b", re.IGNORECASE)
NUMBERS = re.compile(r"\b\d[\d,.]*%?\b|\$\d")
PROPER = re.compile(r"(?<![.!?]\s)(?<!^)\b[A-Z][a-z]{2,}\b", re.MULTILINE)

LANG = {
    "en": {"word": WORD_RE, "contractions": CONTRACTIONS, "pronouns": PRONOUNS,
           "numbers": NUMBERS, "proper": PROPER,
           "contraction_human": 3.0, "person_human": 8.0},
    "pt": {
        "word": re.compile(r"[^\W\d_]+(?:['’-][^\W\d_]+)*"),
        # Spoken Brazilian Portuguese has no apostrophes. Its equivalent of
        # "don't" and "it's" is "tá", "pra", "né": the marks of someone talking.
        "contractions": re.compile(
            r"\b(?:tá|tô|tava|tavam|tamo|tamos|pra|pro|pras|pros|né|cê|cês|vc|vcs|tb|tbm|"
            r"daí|aí|num|numa|dum|duma|cadê|bora|beleza|tipo|mano|sô)\b", re.IGNORECASE),
        # Portuguese drops the subject: "perdi", "postei" are first person alone.
        "pronouns": re.compile(
            r"\b(?:eu|me|mim|meu|minha|meus|minhas|comigo|nós|nosso|nossa|nossos|nossas|"
            r"você|vocês|voce|vc|vcs|cê|te|seu|sua|seus|suas|tu|teu|tua|a gente)\b"
            r"|\b[^\W\d_]{2,}ei\b"
            r"|\b(?:perdi|vendi|aprendi|entendi|consegui|descobri|decidi|fiz|tive|fui|"
            r"sou|estou|tenho|tinha|achei|acho|sei|quero|queria|posso|faço|levo|uso)\b",
            re.IGNORECASE),
        # Portuguese writes its numbers out ("três meses") and its months in
        # lower case ("em março"), so both count as concrete here. English gets
        # its months for free through the capital letter.
        "numbers": re.compile(
            r"R\$\s?\d|\b\d[\d.,]*%?\b|\$\d"
            r"|\b(?:dois|duas|três|quatro|cinco|seis|sete|oito|nove|dez|onze|doze|quinze|"
            r"vinte|trinta|quarenta|cinquenta|cem|duzentos|quinhentos|mil|milhão|milhões)\b"
            r"|\b(?:janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|"
            r"outubro|novembro|dezembro|segunda-feira|terça-feira|quarta-feira|"
            r"quinta-feira|sexta-feira|sábado|domingo)\b", re.IGNORECASE),
        # Names, including brand names in CamelCase ("WhatsApp", "ManyChat").
        "proper": re.compile(
            r"(?<![.!?]\s)(?<!^)\b[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõçà]{2,}(?:[A-Z][a-z]+)*\b",
            re.MULTILINE),
        "contraction_human": 3.0, "person_human": 6.0,
    },
}

_PT_MARKERS = {
    "não", "nao", "você", "voce", "vc", "que", "de", "da", "do", "das", "dos",
    "é", "um", "uma", "eu", "isso", "esse", "essa", "como", "mais", "seu",
    "sua", "porque", "tá", "pra", "pro", "com", "por", "para", "os", "as",
    "no", "na", "nos", "em", "mas", "meu", "minha", "te", "já", "só", "tem",
    "foi", "vai", "são", "aqui", "hoje", "gente", "o", "ou", "se", "também",
}
_EN_MARKERS = {
    "the", "you", "your", "and", "is", "to", "that", "of", "it", "this",
    "i", "my", "for", "was", "are", "with", "what", "how", "if", "on", "in",
    "be", "have", "will", "just",
}


def detect_lang(text):
    low = text.lower()
    toks = re.findall(r"[^\W\d_]+(?:'[a-z]+)?", low)
    pt = sum(t in _PT_MARKERS for t in toks) + 2 * len(re.findall(r"[ãõçâêôáéíóúà]", low))
    en = sum(t in _EN_MARKERS for t in toks)
    return "pt" if pt > en else "en"


def load_lexicon(path=LEX, lang="en", pt_path=LEX_PT):
    """Invisible characters and typography are shared. Words, phrases and
    structural tells come from the lexicon of the text's language."""
    lex = json.load(open(path, encoding="utf-8"))
    if lang == "pt" and os.path.exists(pt_path):
        pt = json.load(open(pt_path, encoding="utf-8"))
        for key in ("words", "phrases", "structures"):
            lex[key] = pt[key]
    return lex


def clamp(n):
    return max(0.0, min(100.0, n))


def scale(value, human, machine):
    """Map value onto 0-100 where `human` -> 100 and `machine` -> 0."""
    if human == machine:
        return 50.0
    return clamp((value - machine) / (human - machine) * 100)


def sentences(text):
    return [s.strip() for s in SENT_RE.findall(text) if len(s.split()) > 2]


def words(text, L=None):
    return (L or LANG["en"])["word"].findall(text)


def check_burstiness(text):
    """Humans vary sentence length hard. Models write even."""
    lens = [len(s.split()) for s in sentences(text)]
    if len(lens) < 4:
        return 50.0, "too short to judge"
    mean = statistics.mean(lens)
    cv = statistics.pstdev(lens) / mean if mean else 0
    score = scale(cv, human=0.70, machine=0.22)
    return score, f"variation {cv:.2f} across {len(lens)} sentences (want 0.55+)"


def check_specificity(text, L):
    """Numbers, names and concrete nouns. Slop is abstract."""
    w = words(text, L)
    if len(w) < 25:
        return 50.0, "too short to judge"
    per100 = 100 / len(w)
    hits = len(L["numbers"].findall(text)) + len(set(L["proper"].findall(text)))
    density = hits * per100
    score = scale(density, human=6.0, machine=0.5)
    return score, f"{hits} concrete markers, {density:.1f} per 100 words (want 4+)"


def check_slop(text, lex, L):
    """Stock vocabulary density against the lexicon."""
    w = words(text, L)
    if not w:
        return 50.0, "empty"
    hits, found = 0, []
    for entry in lex["words"] + lex["phrases"]:
        pattern = re.compile(r"\b" + re.escape(entry["find"]).replace(r"\ ", r"\s+") + r"\b",
                             re.IGNORECASE)
        n = len(pattern.findall(text))
        if n:
            hits += n
            found.append(entry["find"])
    density = hits * 100 / len(w)
    score = scale(density, human=0.0, machine=4.0)
    detail = f"{hits} stock terms, {density:.1f} per 100 words"
    if found:
        detail += " (" + ", ".join(sorted(found)[:4]) + (", ..." if len(found) > 4 else "") + ")"
    return score, detail


def check_fingerprint(text):
    """Characters a phone keyboard does not produce."""
    invisible = sum(1 for c in text if unicodedata.category(c) == "Cf")
    em = text.count("—")
    curly = sum(text.count(c) for c in "‘’“”")
    ellip = text.count("…")
    nbsp = sum(text.count(c) for c in "   ")
    total = invisible * 4 + em * 2 + curly + ellip + nbsp
    per1k = total * 1000 / max(len(text), 1)
    score = scale(per1k, human=0.0, machine=12.0)
    detail = (f"{invisible} invisible, {em} em dash, {curly} curly quote, "
              f"{ellip} ellipsis, {nbsp} hard space")
    return score, detail


def check_voice(text, lex, L):
    """Contractions, person, and the shapes models default to."""
    w = words(text, L)
    if len(w) < 25:
        return 50.0, "too short to judge"
    per100 = 100 / len(w)
    contractions = len(L["contractions"].findall(text)) * per100
    person = len(L["pronouns"].findall(text)) * per100
    tells = 0
    names = []
    for s in lex["structures"]:
        try:
            n = len(re.compile(s["regex"], re.MULTILINE).findall(text))
        except re.error:
            continue
        if n:
            tells += n
            names.append(s["id"])
    bullets = [len(b.split()) for b in re.findall(r"(?m)^\s*[-*•]\s+(.+)$", text)]
    uniform = (len(bullets) >= 3 and statistics.pstdev(bullets) < 1.6)
    score = (scale(contractions, human=L["contraction_human"], machine=0.0) * 0.35
             + scale(person, human=L["person_human"], machine=1.0) * 0.35
             + clamp(100 - tells * 22) * 0.30)
    if uniform:
        score -= 12
        names.append("uniform-bullets")
    detail = (f"{contractions:.1f} contractions, {person:.1f} personal pronouns "
              f"per 100 words, {tells} structural tell(s)")
    if names:
        detail += " [" + ", ".join(names[:4]) + "]"
    return clamp(score), detail


CHECKS = ["BURSTINESS", "SPECIFICITY", "SLOP DENSITY", "FINGERPRINT", "VOICE"]


def run(text, lex, lang="en"):
    L = LANG[lang]
    results = {}
    results["BURSTINESS"] = check_burstiness(text)
    results["SPECIFICITY"] = check_specificity(text, L)
    results["SLOP DENSITY"] = check_slop(text, lex, L)
    results["FINGERPRINT"] = check_fingerprint(text)
    results["VOICE"] = check_voice(text, lex, L)
    scores = [results[c][0] for c in CHECKS]
    # The weakest check drags the verdict: a detector only needs one signal.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4
    verdict = "PASS" if overall >= 70 and min(scores) >= 55 else (
        "REVIEW" if overall >= 50 else "FLAGGED")
    return results, overall, verdict


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render(results, overall, verdict, label=None, out=sys.stdout):
    title = "AI DETECTION PANEL" + (f"  -  {label}" if label else "")
    print("\n" + title, file=out)
    print("=" * max(len(title), 62), file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<13} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<13} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'HUMAN SCORE':<13} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    if verdict != "PASS":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Weakest signal: {weakest}. Fix that first.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Score how machine-written a draft looks.")
    ap.add_argument("input", nargs="?", default="-", help="file, or - for stdin")
    ap.add_argument("compare", nargs="?", help="second file, to show before/after")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--lexicon", default=LEX)
    ap.add_argument("--lang", choices=["auto", "en", "pt"], default="auto")
    args = ap.parse_args()

    read = lambda p: sys.stdin.read() if p == "-" else open(p, encoding="utf-8").read()

    targets = [(args.input, read(args.input))]
    if args.compare:
        targets.append((args.compare, read(args.compare)))

    payload, langs = [], []
    for name, text in targets:
        lang = detect_lang(text) if args.lang == "auto" else args.lang
        lex = load_lexicon(args.lexicon, lang)
        langs.append((lang, lex))
        results, overall, verdict = run(text, lex, lang)
        payload.append({
            "source": name,
            "lang": lang,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "human_score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if args.compare else payload[0], indent=2, ensure_ascii=False))
        return

    for (name, text), p, (lang, lex) in zip(targets, payload, langs):
        results, overall, verdict = run(text, lex, lang)
        render(results, overall, verdict, label=os.path.basename(name) if args.compare else None)
    if args.compare:
        a, b = payload
        delta = b["human_score"] - a["human_score"]
        print(f"  {a['human_score']:.1f} {a['verdict']}  ->  "
              f"{b['human_score']:.1f} {b['verdict']}   ({delta:+.1f})\n")

    sys.exit(0 if payload[-1]["verdict"] == "PASS" else 1)


if __name__ == "__main__":
    main()
