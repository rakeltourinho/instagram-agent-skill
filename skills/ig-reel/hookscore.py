#!/usr/bin/env python3
"""
hookscore.py - score the first line of a Reel on the five things strong hooks
have in common, and rank a batch of them against each other.

What this is:  five local heuristics, computed on your machine from the text
alone. They measure properties that hooks which hold attention tend to share -
a length you can say in under three seconds, a concrete marker, something at stake,
the payload at the front rather than the back, and a viewer to aim it at.

What this is NOT:  a view predictor. It was tested against 74 real short-form
hooks, transcribed from the first three seconds of the top eight and bottom
eight performers on five channels. Separating a real hook from a deliberately
bad one it does well: AUC 0.83, and 9 of 10 written-to-be-bad hooks scored
below the real median. Separating a good creator's hits from that same
creator's misses it barely does at all: AUC 0.56, where 0.50 is a coin flip.
(Those numbers are for English. The Portuguese tables have not been validated
against a real corpus yet, see the README.)

So use it for what it measured well. It catches greetings, preambles, hooks
with nothing concrete in them and hooks that take five seconds to say. It will
not tell you which of two decent hooks will travel, and nothing that reads text
can, because that is decided by your face, your edit, your audio and who
Instagram shows it to. Trust the retention graph over this script.

Each check returns 0 to 100. Higher is better.

Languages:  English and Brazilian Portuguese. The language is detected per
hook; --lang en|pt forces one. Each language has its own vocabulary for the
five checks (numbers said out loud, stakes, weak openers, imperatives, who is
being addressed) and its own dealbreakers. The scoring maths is the same, so a
75 in Portuguese means the same thing as a 75 in English.

Usage
  python3 hookscore.py hooks.txt              # one hook per line, ranked
  python3 hookscore.py --hook "I lost $18,000 on one missing contract."
  python3 hookscore.py --hook "Perdi R$ 18 mil por causa de uma cláusula."
  pbpaste | python3 hookscore.py -
  python3 hookscore.py hooks.txt --json
  python3 hookscore.py hooks.txt --lang pt    # force Portuguese
"""

import argparse
import json
import re
import statistics
import sys

# Unicode-aware: "Ninguém" and "não" are one word each, not "Ningu" and "n".
WORD_RE = re.compile(r"[\w$%'’º-]+")
HASHTAG_RE = re.compile(r"(?:^|\s)#\w+")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿]")


# --------------------------------------------------------------------------
# English
# --------------------------------------------------------------------------

EN = {"code": "en"}

EN["number_re"] = re.compile(
    r"\$\s?\d[\d,]*(?:\.\d+)?"                       # money, whole
    r"|\b\d[\d,]*(?:\.\d+)?\s?"                      # a figure, with or
    r"(?:%|k\b|x\b|hrs?\b|hours?\b|mins?\b|minutes?\b"  # without a unit
    r"|days?\b|weeks?\b|months?\b|years?\b)?",
    re.IGNORECASE)
EN["proper_re"] = re.compile(r"(?<!^)\b[A-Z][a-z]{2,}\b")
EN["price_re"] = re.compile(r"\$\s?\d")
EN["max_chars"] = 60
EN["wps"] = 2.75                                    # ~165 words per minute

# Spoken hooks say their numbers out loud. "Zero dollars" and "twenty grand"
# are as concrete as "$0" and "$20,000", and counting only digits missed them.
# "one" and "first" are deliberately absent: they are filler far more often
# than they are a quantity.
EN["spoken_numbers"] = {
    "zero", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "ten", "eleven", "twelve", "fifteen", "twenty", "thirty", "forty", "fifty",
    "sixty", "seventy", "eighty", "ninety", "hundred", "thousand", "million",
    "billion", "dozen", "half", "twice", "triple",
}
EN["money_words"] = {
    "dollars", "dollar", "bucks", "grand", "percent", "cents",
    "millionaire", "billionaire", "revenue", "profit", "salary", "rent",
}

# Words that put something on the line. A hook with none of these is a
# statement; a hook with one is a reason to keep watching.
EN["stakes"] = {
    "stop", "never", "wrong", "mistake", "mistakes", "lost", "lose", "losing",
    "cost", "costs", "broke", "broken", "failed", "failure", "fail", "nobody",
    "no", "not", "don't", "dont", "doesn't", "didn't", "can't", "won't",
    "quit", "quitting", "fired", "deleted", "delete", "killed", "kills", "kill",
    "replaced", "replaces", "cut", "beat", "free", "paid", "charged", "hired",
    "saved", "first",
    "banned", "illegal", "worst", "hate", "hated", "wasted", "waste", "scam",
    "lie", "lied", "lying", "truth", "secret", "hidden", "stole", "stolen",
    "before", "until", "instead", "but", "except", "unless", "problem",
    "risk", "danger", "warning", "regret", "wish", "should", "shouldn't",
    "still", "already", "only", "without", "versus", "vs", "actually",
}
EN["stake_phrases"] = []

# Openers that spend the first second saying nothing.
EN["weak_openers"] = [
    "so", "ok", "okay", "hey", "hi", "hello", "guys", "yo", "alright",
    "welcome", "today", "basically", "honestly", "look", "listen", "um",
    "just", "let", "lets", "let's", "i wanted", "i want", "one of",
    "have you", "did you", "do you", "are you", "in this", "in today",
    "the thing", "a lot", "there is", "there are", "this is", "it is",
    "as a", "when it", "if you've", "you know",
]

# Imperatives that earn the front position.
EN["imperatives"] = {
    "stop", "steal", "copy", "delete", "try", "watch", "read", "save",
    "use", "build", "make", "write", "send", "take", "start", "quit",
    "never", "always", "don't", "dont", "do", "put", "run", "check",
}

EN["you_re"] = re.compile(r"\b(you|your|you're|youre|yourself)\b")
EN["me_re"] = re.compile(r"\b(i|my|me|we|our)\b")

EN["dealbreakers"] = [
    (re.compile(r"(?i)^\s*(?:stop scrolling|don'?t scroll)"),
     "Opens with \"stop scrolling\". Asking for attention proves you have not earned it."),
    (re.compile(r"(?i)\b(?:in (?:this|today'?s) (?:video|reel)|i'?m going to show you|i'?ll show you how)\b"),
     "Video preamble. Delete it and open on the payoff."),
    (re.compile(r"(?i)^\s*(?:hey |hi |what'?s up |welcome )"),
     "Greeting. Nobody came to the feed to be greeted."),
    (HASHTAG_RE,
     "Hashtag in the hook. Hashtags belong at the bottom of the caption, if anywhere."),
    (EMOJI_RE,
     "Emoji in the hook. On-screen text at hook size has room for words or for an emoji, not both."),
]


# --------------------------------------------------------------------------
# Português do Brasil
# --------------------------------------------------------------------------
# Not a translation of the English lists. Spoken Brazilian Portuguese hooks
# have their own fillers ("então", "gente", "fala galera"), their own money
# ("R$ 18 mil", "dez conto", "pix"), their own internet stakes ("flopar",
# "cancelado", "shadowban") and drop the subject pronoun most of the time
# ("Perdi R$ 18 mil" has no "eu" in it and is still first person).

PT = {"code": "pt"}

PT["number_re"] = re.compile(
    r"R\$\s?\d[\d.]*(?:,\d+)?(?:\s?(?:mil|mi|milh[õo]es|milh[ãa]o|k)\b)?"   # dinheiro
    r"|\b\d[\d.]*(?:,\d+)?(?:º|ª)?\s?"
    r"(?:%|mil\b|mi\b|k\b|x\b|h\b|hrs?\b|horas?\b|min\b|minutos?\b|seg\b|segundos?\b"
    r"|dias?\b|semanas?\b|m[eê]s(?:es)?\b|anos?\b|reais\b|views\b|seguidores\b)?",
    re.IGNORECASE)
# Sentence starts are capitalised in Portuguese too, so they are not names.
PT["proper_re"] = re.compile(
    r"(?<!^)(?<![.!?:]\s)(?<![.!?:]\s\")\b[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõçà]{2,}\b")
PT["price_re"] = re.compile(r"R\$\s?\d")
# Portuguese runs about 15% longer in characters for the same number of words.
PT["max_chars"] = 70
PT["wps"] = 2.5                                     # ~150 palavras por minuto

# "um", "uma" and "primeiro" are left out on purpose, same reason as "one"
# in English: they are filler far more often than they are a quantity.
PT["spoken_numbers"] = {
    "zero", "dois", "duas", "três", "tres", "quatro", "cinco", "seis", "sete",
    "oito", "nove", "dez", "onze", "doze", "quinze", "vinte", "trinta",
    "quarenta", "cinquenta", "sessenta", "setenta", "oitenta", "noventa",
    "cem", "cento", "duzentos", "trezentos", "quinhentos", "mil", "milhão",
    "milhões", "bilhão", "bilhões", "dúzia", "metade", "dobro", "triplo",
    "dobrei", "tripliquei",
}
PT["money_words"] = {
    "reais", "real", "conto", "contos", "pila", "grana", "dinheiro",
    "faturamento", "faturei", "faturar", "lucro", "lucrei", "salário",
    "aluguel", "pix", "boleto", "centavos", "porcento", "milionário",
    "milionária", "prejuízo", "dívida", "dívidas", "orçamento",
}
PT["stakes"] = {
    # parar / nunca / erro
    "pare", "parem", "nunca", "jamais", "errado", "errada", "errados",
    "erradas", "erro", "erros", "errando", "errei", "erra",
    # perder / custar / quebrar
    "perdi", "perder", "perdendo", "perdeu", "perda", "custou", "custa",
    "custam", "quebrei", "quebrou", "faliu", "falhei", "falhou", "fracasso",
    "fracassei", "prejuízo", "flopar", "flopou", "flopa", "flopando", "flop",
    # negação
    "ninguém", "ninguem", "não", "nao", "nem", "nada",
    # largar / demitir / apagar
    "desisti", "larguei", "larga", "demitido", "demitida", "demiti",
    "apaguei", "apaga", "apague", "deletei", "acabou", "acaba", "mata",
    "matou", "matando", "substituiu", "substitui", "cortei", "corta",
    # dinheiro e troca
    "grátis", "gratuito", "paguei", "pagava", "cobrei", "cobra", "cobrar",
    "contratei", "economizei", "economiza", "ganhei", "vendi",
    # proibido / segredo / mentira
    "proibido", "ilegal", "pior", "piores", "odeio", "odiei", "odeiam",
    "desperdicei", "desperdício", "golpe", "mentira", "mentiram", "mentem",
    "verdade", "segredo", "escondido", "escondem", "roubou", "roubaram",
    "cancelado", "cancelada", "bloqueado", "bloqueada", "shadowban",
    "banido", "banida", "processado", "multa",
    # contraste e tensão
    "antes", "até", "mas", "porém", "só", "sem", "exceto", "problema",
    "risco", "perigo", "cuidado", "alerta", "arrependi", "arrependimento",
    "deveria", "devia", "ainda", "já", "contra", "versus", "vs",
    "realmente", "culpa", "medo", "vergonha",
}
# Multi-word stakes. "para" alone is almost always the preposition, so the
# imperative only counts when it is "para de" / "para com".
PT["stake_phrases"] = [
    "para de", "pare de", "parem de", "para com", "pare com", "em vez de",
    "ao invés de", "de graça", "na real", "a real é", "deu errado",
    "deu ruim", "não faz", "não faça",
]

PT["weak_openers"] = [
    "oi", "olá", "ola", "e aí", "e ai", "eai", "fala", "gente", "galera",
    "pessoal", "bom dia", "boa tarde", "boa noite", "hoje", "então",
    "entao", "bom", "tipo", "basicamente", "sinceramente", "olha", "escuta",
    "seguinte", "o seguinte", "é o seguinte", "vamos", "bora", "eu queria",
    "eu quero", "eu vou", "vou", "queria", "um dos", "uma das", "você sabia",
    "você já", "vocês já", "nesse", "neste", "no vídeo", "a questão",
    "muita gente", "muitas pessoas", "existe", "existem", "tem gente",
    "isso é", "esse é", "essa é", "como um", "como uma", "quando se",
    "se você já", "meus amores", "amores", "minha gente", "tudo bem",
    "beleza", "enfim", "ah", "ahn", "é", "aqui",
]

PT["imperatives"] = {
    "pare", "parem", "rouba", "roube", "copia", "copie", "apaga", "apague",
    "testa", "teste", "tenta", "tente", "assiste", "assista", "lê", "leia",
    "salva", "salve", "usa", "use", "monta", "monte", "faz", "faça",
    "escreve", "escreva", "manda", "mande", "pega", "pegue", "começa",
    "comece", "larga", "largue", "nunca", "sempre", "não", "coloca",
    "coloque", "confere", "confira", "presta", "guarda", "guarde", "anota",
    "anote", "esquece", "esqueça", "evita", "evite", "troca", "troque",
    "corta", "corte", "cobra", "cobre", "aprende", "aprenda",
}

PT["you_re"] = re.compile(
    r"\b(você|vocês|voce|voces|vc|vcs|cê|ce|te|ti|contigo|seu|sua|seus|suas|tu|teu|tua)\b",
    re.IGNORECASE)
# Portuguese drops the subject pronoun. "Perdi", "postei", "testei" are first
# person on their own, so first-person verb endings count as well.
PT["me_re"] = re.compile(
    r"\b(eu|meu|minha|meus|minhas|me|mim|comigo|nós|nosso|nossa|nossos|nossas)\b"
    r"|\ba gente\b"
    r"|\b\w{2,}ei\b"
    r"|\b(perdi|vendi|aprendi|entendi|consegui|descobri|decidi|fiz|tive|fui|sou|"
    r"tô|estou|tenho|tinha|pagava|cobrava|trabalhei|levei|levo|uso|faço|sei)\b",
    re.IGNORECASE)

PT["dealbreakers"] = [
    (re.compile(r"(?i)^\s*(?:(?:para|pare|parem)\s+de\s+(?:rolar|passar|scrollar|arrastar)"
                r"|n[ãa]o\s+(?:passa|pula|role|rola|arrasta|scrolla)\b"
                r"|espera[,!.]?\s+n[ãa]o\s+(?:passa|pula|rola))"),
     "Abre com \"para de rolar o feed\". Pedir atenção prova que você ainda não conquistou."),
    (re.compile(r"(?i)\b(?:n(?:esse|este)\s+(?:vídeo|video|reels?|post)\b"
                r"|no\s+(?:vídeo|video|reels?)\s+de\s+hoje"
                r"|hoje\s+(?:eu\s+)?(?:vou|vim|quero|queria)\b"
                r"|vou\s+(?:te\s+|lhe\s+)?(?:mostrar|ensinar|explicar)\s+(?:como|pra\s+voc|para\s+voc|uma\b|um\b)"
                r"|vou\s+(?:contar|falar)\s+(?:pra|para)\s+voc"
                r"|vim\s+(?:aqui\s+)?(?:te\s+)?(?:mostrar|falar|contar)"
                r"|resolvi\s+fazer\s+(?:esse|este)\s+v[íi]deo)"),
     "Preâmbulo de vídeo. Apaga e abre direto no resultado."),
    (re.compile(r"(?i)^\s*(?:oi+\b|ol[áa]\b|e\s*a[íi]\b|eai\b"
                r"|fala\s+(?:galera|pessoal|gente|meu\s+povo|time|fam[íi]lia|a[íi])\b"
                r"|bom\s+dia\b|boa\s+(?:tarde|noite)\b|sej(?:a|am)\s+bem[- ]vind"
                r"|tudo\s+bem\b|meus\s+amores\b)"),
     "Cumprimento. Ninguém abriu o feed pra ser cumprimentado."),
    (HASHTAG_RE,
     "Hashtag no gancho. Hashtag vai no fim da legenda, se for."),
    (EMOJI_RE,
     "Emoji no gancho. Texto na tela em tamanho de gancho tem espaço pra palavra ou pra emoji, não pros dois."),
]

LANGS = {"en": EN, "pt": PT}

# Words that are frequent in one language and rare in the other. Accented
# letters count double: English almost never has them.
_PT_MARKERS = {
    "não", "nao", "você", "voce", "vc", "que", "de", "da", "do", "das", "dos",
    "é", "um", "uma", "eu", "isso", "esse", "essa", "como", "mais", "seu",
    "sua", "ninguém", "porque", "tá", "pra", "pro", "com", "por", "para",
    "os", "as", "no", "na", "nos", "em", "mas", "meu", "minha", "te", "já",
    "só", "tem", "foi", "vai", "são", "isto", "aqui", "hoje", "gente",
    "o", "ou", "se", "meus", "minhas", "seus", "suas", "deu", "deram",
    "primeiros", "primeiro", "nunca", "ninguem", "pela", "pelo", "ao", "às",
    "também", "quando", "onde", "ele", "ela", "eles", "elas", "dia", "dias",
}
_EN_MARKERS = {
    "the", "you", "your", "and", "is", "to", "that", "of", "it", "this",
    "i", "my", "for", "was", "are", "with", "what", "how", "nobody",
    "don't", "stop", "if", "on", "in", "be", "have", "will", "just",
}


def detect_lang(text):
    low = text.lower()
    toks = re.findall(r"[^\W\d_]+(?:'[a-z]+)?", low)
    pt = sum(t in _PT_MARKERS for t in toks) + 2 * len(re.findall(r"[ãõçâêôáéíóúà]", low))
    en = sum(t in _EN_MARKERS for t in toks)
    return "pt" if pt > en else "en"


def clamp(n):
    return max(0.0, min(100.0, n))


def words(text):
    # "$18,000" and "18.000" are one word when spoken, so one word here too.
    return WORD_RE.findall(re.sub(r"(?<=\d)[,.](?=\d{3}\b)", "", text))


def _low_words(text):
    return [x.lower().strip("'’") for x in words(text)]


def _starts_with(tokens, phrase):
    parts = phrase.split()
    return tokens[:len(parts)] == parts


def _phrase_hits(low_text, phrases):
    return [p for p in phrases if re.search(r"\b" + re.escape(p) + r"\b", low_text)]


def check_length(text, L):
    """A hook has to land before the thumb moves. Roughly two seconds."""
    w = words(text)
    n = len(w)
    secs = n / L["wps"]
    chars = len(text.strip())
    if 5 <= n <= 12:
        score = 100.0
    elif n < 5:
        score = clamp(100 - (5 - n) * 20)
    else:
        score = clamp(100 - (n - 12) * 11)
    if chars > L["max_chars"]:           # two lines of big on-screen text
        score -= 12
    return clamp(score), f"{n} words, {chars} chars, ~{secs:.1f}s spoken (want 5-12 words)"


def check_specificity(text, L):
    """One concrete thing beats three abstract ones."""
    nums = [n.strip() for n in L["number_re"].findall(text) if n.strip()]
    propers = set(L["proper_re"].findall(text))
    low = _low_words(text)
    spoken = [w for w in low if w in L["spoken_numbers"] or w in L["money_words"]]
    hits = len(nums) + len(propers) + len(spoken)
    score = 15.0 if hits == 0 else clamp(45 + hits * 30)
    found = ", ".join(nums[:2] + sorted(propers)[:2] + spoken[:2])
    return score, (f"{hits} concrete marker(s)" + (f": {found}" if found else
                   " - no number, no name, nothing checkable"))


def check_stakes(text, L):
    """Tension, cost, negation. Something the viewer might lose."""
    w = _low_words(text)
    hits = [x for x in w if x in L["stakes"]]
    hits += _phrase_hits(text.lower(), L["stake_phrases"])
    markers = sorted(set(hits))
    if L["price_re"].search(text):
        markers.append("a price")
    n = len(markers)
    score = {0: 20.0, 1: 70.0}.get(n, 100.0)
    detail = f"{n} tension marker(s)" + (f": {', '.join(markers[:4])}" if markers else
                                         " - nothing is at stake in this line")
    return clamp(score), detail


def check_frontload(text, L):
    """The interesting word cannot be in position nine."""
    w = words(text)
    if not w:
        return 0.0, "empty"
    low = [x.lower().strip("'’") for x in w]
    penalty = 0
    hit_opener = None
    # Whole words only: "so" must not fire on "social", nor "bom" on "bomba".
    for weak in L["weak_openers"]:
        if _starts_with(low, weak):
            penalty, hit_opener = 30, weak
            break
    phrase_starts = set()
    for p in L["stake_phrases"]:
        parts = p.split()
        for i in range(len(low) - len(parts) + 1):
            if low[i:i + len(parts)] == parts:
                phrase_starts.add(i)
    payload = None
    for i, token in enumerate(low):
        if (token in L["stakes"] or token in L["spoken_numbers"] or token in L["money_words"]
                or i in phrase_starts
                or L["number_re"].match(w[i]) or (i and L["proper_re"].match(w[i]))):
            payload = i
            break
    if payload is None:
        base = 30.0
        where = "no payload word anywhere in the line"
    elif payload <= 3:
        base = 100.0
        where = f"payload at word {payload + 1}"
    elif payload <= 6:
        base = 70.0
        where = f"payload at word {payload + 1}, could move forward"
    else:
        base = 40.0
        where = f"payload at word {payload + 1}, too late"
    detail = where + (f"; weak opener \"{hit_opener}\"" if hit_opener else "")
    return clamp(base - penalty), detail


def check_address(text, L):
    """Aimed at one viewer, or floating in the air."""
    low = text.lower()
    w = _low_words(text)
    if L["you_re"].search(low):
        return 100.0, "speaks to the viewer"
    if w and w[0] in L["imperatives"]:
        return 90.0, f"imperative opener (\"{w[0]}\")"
    if w and L["code"] == "pt" and _starts_with(w, "para de"):
        return 90.0, "imperative opener (\"para de\")"
    if L["me_re"].search(low):
        return 70.0, "first person, no viewer named"
    return 35.0, "third person, nobody in the room"


CHECKS = ["LENGTH", "SPECIFICITY", "STAKES", "FRONTLOAD", "ADDRESS"]


def run(text, lang="auto"):
    code = detect_lang(text) if lang in (None, "auto") else lang
    L = LANGS[code]
    results = {
        "LENGTH": check_length(text, L),
        "SPECIFICITY": check_specificity(text, L),
        "STAKES": check_stakes(text, L),
        "FRONTLOAD": check_frontload(text, L),
        "ADDRESS": check_address(text, L),
    }
    flags = [msg for pattern, msg in L["dealbreakers"] if pattern.search(text)]
    scores = [results[c][0] for c in CHECKS]
    # The weakest property caps the hook, same logic as detect.py: one bad
    # property is enough for the thumb to keep moving.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4 - len(flags) * 15
    overall = clamp(overall)
    verdict = "STRONG" if overall >= 70 and min(scores) >= 55 and not flags else (
        "OK" if overall >= 50 else "WEAK")
    return results, overall, verdict, flags


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render_one(text, results, overall, verdict, flags, out=sys.stdout):
    print("\nHOOK SCORE", file=out)
    print("=" * 62, file=out)
    print(f"  \"{text.strip()}\"\n", file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<13} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<13} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'HOOK SCORE':<13} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    for f in flags:
        print(f"\n  DEALBREAKER  {f}", file=out)
    if verdict != "STRONG":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Weakest property: {weakest}. Fix that one and re-run.", file=out)
    print("", file=out)


def render_table(rows, out=sys.stdout):
    print("\nHOOK RANKING\n" + "=" * 78, file=out)
    for i, r in enumerate(rows, 1):
        mark = "->" if i == 1 else "  "
        hook = r["hook"] if len(r["hook"]) <= 62 else r["hook"][:59] + "..."
        print(f"{mark} {r['score']:5.1f} {r['verdict']:<7} {hook}", file=out)
        print(f"        weakest: {r['weakest']} ({r['checks'][r['weakest']]['score']:.0f})", file=out)
        for f in r["flags"]:
            print(f"        dealbreaker: {f}", file=out)
    print("\nShoot the top one. If the top one is under 50, none of these are the hook.\n",
          file=out)


def main():
    ap = argparse.ArgumentParser(description="Score a Reel hook on five properties.")
    ap.add_argument("input", nargs="?", default="-", help="file with one hook per line, or -")
    ap.add_argument("--hook", help="score a single hook given on the command line")
    ap.add_argument("--lang", choices=["auto", "en", "pt"], default="auto",
                    help="language of the hooks (default: detect per hook)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.hook:
        lines = [args.hook]
    else:
        raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
    if not lines:
        print("nothing to score", file=sys.stderr)
        sys.exit(2)

    payload = []
    for line in lines:
        results, overall, verdict, flags = run(line, args.lang)
        payload.append({
            "hook": line,
            "lang": detect_lang(line) if args.lang == "auto" else args.lang,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "weakest": min(CHECKS, key=lambda c: results[c][0]),
            "flags": flags,
            "score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if len(payload) > 1 else payload[0], indent=2, ensure_ascii=False))
        return

    if len(payload) == 1:
        results, overall, verdict, flags = run(lines[0], args.lang)
        render_one(lines[0], results, overall, verdict, flags)
    else:
        render_table(sorted(payload, key=lambda r: -r["score"]))

    sys.exit(0 if max(p["score"] for p in payload) >= 70 else 1)


if __name__ == "__main__":
    main()
