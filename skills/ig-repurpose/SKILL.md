---
name: ig-repurpose
description: >-
  Transforma um conteúdo longo - vídeo do YouTube, podcast, live, newsletter,
  post de blog, aula ou ligação com cliente - numa semana de reels e
  carrosséis. Funciona em português e em inglês. Use quando pedirem
  "reaproveita isso", "transforma em reels", "tenho um vídeo/podcast/
  transcrição", "corta isso", "repurpose this", ou quando colarem algo longo e
  quiserem no Instagram.
---

# ig-repurpose

Um bom conteúdo longo tem de quatro a seis posts dentro. A maioria das pessoas
tira um e joga o resto fora.

## Entrada

Uma transcrição, um artigo, uma newsletter, um roteiro, um resumo de ligação, uma
live. Se a pessoa mandar um link e esta sessão tiver ferramenta de transcrição,
usa; senão, pede pra colar. Lê tudo antes de extrair qualquer coisa.

Se a fonte é um vídeo da própria pessoa, pede o arquivo também. Reels feito com a
gravação dela ganha de um feito com as palavras dela lidas de novo.

Live e podcast em português costumam ter muito "né", "tipo", "então" e frase que
recomeça. Na hora de extrair, limpa a muleta mas mantém o jeito de falar: a
frase tem que continuar soando como ela.

## Extrai, não resume

Resumo de vídeo não é Reels. Ninguém quer o resumo. Passa pelo conteúdo e tira
as coisas que se sustentam sozinhas:

| o que tirar | o que é |
| --- | --- |
| **Afirmações** | toda frase que começaria uma discussão |
| **Números** | todo valor, custo, duração, porcentagem |
| **Histórias** | todo momento com uma pessoa, uma cena e um custo |
| **Mecanismos** | todo "o jeito que isso funciona de verdade é..." |
| **Erros** | toda admissão de algo que deu errado |
| **Frases** | toda frase que já pode ser citada do jeito que está |

Lista o que achou, com contagem, antes de escrever qualquer coisa. Se o conteúdo
rende menos de quatro itens, ele é raso, e quatro posts espremidos dele também
vão ser. Diz isso.

## Depois escolhe o formato de cada extração

Nem tudo é Reels.

- **Afirmação, erro, história** viram Reels. Precisam de voz e de rosto.
- **Mecanismo, lista numerada** viram carrossel. Precisam ser relidos.
- **Uma frase citável** vira frame de story, ou carrossel de texto, não post.

## Depois monta a semana

Cada extração vira um post e cada post se sustenta sozinho. Quem assiste não viu
a fonte e nunca vai ver. Nunca escreve "como eu falei no meu último vídeo". O post
é a coisa.

Dá uma fórmula de gancho do `ig-reel/hooks.pt.json` pra cada um e varia. Cinco
posts da mesma fonte com o mesmo formato de gancho parecem fábrica de conteúdo,
porque são.

Se a fonte é vídeo da própria pessoa, **usa a gravação de verdade**. O trecho em
que ela falou a coisa, com a reação real, ganha de uma regravação sempre. Corta
na frase, não na respiração.

Ordena a semana pra afirmação mais forte ir primeiro, a história cair no meio da
semana e o mecanismo ir por último, quando quem gostou dos primeiros está
esperando por ele.

## Saída

```
FONTE: "Por que a gente acabou com a reunião de briefing" (podcast de 42 min, 8.900 palavras)

ACHEI  5 afirmações, 9 números, 3 histórias, 4 mecanismos, 2 erros, 7 frases citáveis

SEMANA
TER  REELS      #2  Ordem Negativa       Para de fazer reunião de briefing
                                         usa o trecho de 14:20, ele ri no fim
QUA  CARROSSEL  Trabalho B               O formulário de 4 perguntas que substituiu a reunião
SEX  REELS      #21 Meio da Frase        "...e nove dias depois ele pediu reembolso"
DOM  REELS      #5  Tempo Encurtado      Seis horas por semana de volta, um link apagado

Fala "escreve a terça" que eu rascunho.
```

Depois rascunha quando pedirem, um por vez, cada um pelo `/ig-reel` e pelo
`/ig-human`. Não despeja quatro roteiros prontos de uma vez. Vão soar todos
iguais e a pessoa não vai gravar nenhum.
