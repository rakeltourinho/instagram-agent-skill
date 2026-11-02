---
name: ig-human
description: >-
  Tira a marca de máquina de qualquer rascunho - travessão, vocabulário de IA
  ("no mundo de hoje", "vale ressaltar", "jornada", "virada de chave"),
  caracteres invisíveis - e pontua o texto num painel de cinco checagens antes
  de sair. Funciona em português e em inglês. Use sempre que o texto precisar
  soar humano, quando pedirem "humaniza", "tá com cara de IA?", "tira os
  travessões", "parece ChatGPT", "de-slop this", ou antes de mostrar qualquer
  legenda, roteiro, comentário, resposta ou DM.
---

# ig-human

Duas ferramentas moram nesta pasta e as duas rodam de verdade. Usa elas. Não
faz isso no olho.

```bash
python3 humanize.py rascunho.txt --report       # limpa e mostra o que mudou
python3 detect.py rascunho.txt                  # pontua, cinco checagens
python3 detect.py antes.txt depois.txt          # prova a diferença
```

As duas detectam o idioma do texto. Em português usam `slop.pt.json`: mais de
200 palavras e expressões que a IA repete em português, com troca que mantém
gênero e número ("jornada" vira "trajetória", não "caminho", pra frase não
quebrar), e 19 estruturas típicas. Em inglês usam `slop.json`. Os caracteres
invisíveis e a tipografia são os mesmos nos dois. `--lang pt` ou `--lang en`
força um idioma.

O léxico é pra ser editado. Se a pessoa sempre usa uma palavra que o léxico
corta (uma nutricionista fala "essencial" o tempo todo, e com razão), tira a
palavra do arquivo.

## Por que isso pesa mais no Instagram do que parece

Legenda é curta e roteiro é falado. Uma frase com cara de escrita numa legenda
de 600 caracteres é uma fatia maior do texto do que a mesma frase num artigo, e
uma locução que ninguém falaria naturalmente aparece na primeira tomada. O
sinal aqui não é um detector marcando o post. É alguém rolando o feed e
passando reto por algo que parece texto de marca, ou a criadora tropeçando no
próprio roteiro.

Em português tem um agravante: a IA escreve português de redação do ENEM. "Além
disso", "dessa forma", "em suma", "é fundamental". Ninguém fala assim no story.

## O que é corrigido automaticamente

**1. Caracteres invisíveis.** Espaço de largura zero, word joiner, hífen
suave, BOM, caracteres de tag Unicode, espaço não separável. Teclado de celular
não produz isso. Sobrevive ao copiar e colar, é invisível em qualquer editor, e
é a coisa mais mecânica num texto gerado. O `humanize.py` apaga todos.

**2. Tipografia.** Travessão vira vírgula, meia-risca vira hífen, aspas curvas
viram retas, reticências viram três pontos, marcador vira hífen. O travessão é
o que mais importa: ele vira vírgula e o script ainda limpa a pontuação dupla
que sobra.

**3. O léxico.** Em português: "no mundo de hoje", "vale ressaltar que",
"alavancar", "potencializar", "jornada", "robusto", "crucial", "virada de
chave", "além disso", "dessa forma", "em suma", e o bloco do Instagram
brasileiro: "para de rolar o feed", "nesse vídeo eu vou te mostrar", "me segue
pra mais dicas", "marca alguém que precisa ver isso", "o algoritmo ama", "esse
é o seu sinal". Cada um vira uma palavra simples ou é apagado, mantendo a
maiúscula e sem mexer em link.

## O que NÃO é corrigido automaticamente

As estruturas são **apontadas, não reescritas**, porque mudar o formato de uma
frase exige julgamento:

- "Não é só X, é Y" e "não só X, mas também Y"
- "Não é sobre X. É sobre Y."
- Lista de três ("clareza, segurança e profissionalismo")
- Pergunta retórica sozinha na linha: "O resultado?"
- O preâmbulo de vídeo: "nesse vídeo eu vou te mostrar"
- Lista com ✅ no lugar de marcador
- Três ou mais palavras em CAIXA ALTA seguidas
- Muro de hashtag
- Fecho de coach: "Bora?", "Vamos juntos?"
- "Você sabia que...?" na abertura
- Isca genérica: "me segue", "marca alguém", "concorda?"

Essa lista é trabalho seu. Reescreve cada linha apontada à mão, mantendo o
sentido, e roda o `detect.py` de novo. É essa parte que leva a nota de REVIEW
pra PASS, e é a parte que script nenhum faz.

## As cinco checagens

O `detect.py` dá nota de 0 a 100 pra cinco sinais, quanto maior, mais humano:

| checagem | o que mede | cara de máquina |
| --- | --- | --- |
| BURSTINESS | variação no tamanho das frases | toda frase do mesmo tamanho |
| SPECIFICITY | números, nomes, meses, marcas por 100 palavras | substantivo abstrato, nenhum número |
| SLOP DENSITY | ocorrências do léxico por 100 palavras | vocabulário de banco |
| FINGERPRINT | invisíveis, travessões, aspas curvas por 1.000 caracteres | tipografia perfeita demais |
| VOICE | marcas de fala, pessoa, estruturas | nenhuma marca de fala, revelação encenada |

Em português, VOICE conta as marcas do português falado no lugar das
contrações do inglês: "tá", "tô", "pra", "né", "cê", "aí", "a gente". E conta
a primeira pessoa pelo verbo também ("perdi", "postei", "testei"), porque em
português ninguém fala "eu" o tempo todo.

O veredito pesa a média em 60% e a **pior checagem sozinha** em 40%, porque um
sinal basta. PASS exige 70+ no geral e nenhuma checagem abaixo de 55.

## Fala isso com honestidade

São cinco heurísticas locais, modeladas nos sinais que os detectores públicos
usam. Rodam inteiras na máquina da pessoa e nada é enviado. **Não são** GPTZero,
Originality, Copyleaks, Winston ou Turnitin, não chamam essas APIs e não
garantem o veredito deles. Corrigir o que elas medem costuma mexer nesses
números também, porque medem as mesmas coisas por baixo. Essa é a promessa.
Não faz uma maior no nome da pessoa, e nunca diz que um texto é "indetectável".

## Ordem das operações

1. `humanize.py rascunho.txt -o limpo.txt --report`
2. Lê as estruturas apontadas. Reescreve essas linhas você mesmo.
3. `detect.py rascunho.txt limpo.txt` pra mostrar o antes e o depois.
4. Se o veredito não é PASS, corrige a pior checagem que a saída nomeou e roda
   de novo. Duas rodadas é normal. Cinco quer dizer que o rascunho foi escrito
   na fórmula, e a solução é outro rascunho, não mais rodadas.
5. Mostra pra pessoa o texto limpo e a nota. Nunca só a nota.
