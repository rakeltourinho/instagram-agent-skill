---
name: ig-carousel
description: >-
  Monta um carrossel do Instagram - a capa que faz arrastar, o texto de cada
  slide e os arquivos 1080x1350 pra subir. Funciona em português e em inglês.
  Use quando pedirem "carrossel", "slides", "post de arrastar", "transforma isso
  num carrossel", "carousel", ou quando a ideia é uma lista ou um passo a passo
  que morreria numa imagem só.
---

# ig-carousel

Carrossel é o formato do grid com mais tempo de permanência, porque arrastar é
uma interação e rolar não é. Ele também ganha uma segunda chance: o Instagram
pode mostrar o carrossel de novo, a partir de um slide mais à frente, pra quem
não interagiu na primeira vez. Então o slide dois também tem que se sustentar
sozinho.

O formato premia uma ideia quebrada em passos. Castiga uma legenda picotada em
pedaços.

## Quando usar em vez de Reels

Usa carrossel quando a ideia tem **sequência e precisa ser relida**: passo a
passo, método com partes, antes e depois, lista que vale print. Usa Reels quando
a ideia tem movimento, rosto, ou uma entrega que precisa ser vista acontecendo.

Se a ideia é uma afirmação só, não é nenhum dos dois. Passa pro `/ig-reel` e
fala isso.

No Brasil o carrossel de texto (fundo liso, frase grande, estilo "tweet") é
muito compartilhado no WhatsApp e no story, porque vira print fácil. Se a
ideia é uma opinião forte ou uma lista curta, esse estilo funciona melhor que
design elaborado.

## Estrutura

De 6 a 10 slides. O limite é 20, e 20 quase sempre é um livro que ninguém
termina. Abaixo de 5, o arrastar nem começa.

```
1         CAPA      o gancho. 6 palavras ou menos, num tamanho que dá pra ler
                    no grid em miniatura. Uma linha de promessa embaixo.
2         O RISCO   por que isso importa, numa frase. Este slide também é uma
                    segunda capa, então não pode ser introdução.
3 a N     UMA IDEIA POR SLIDE. Título de 3 a 7 palavras, no máximo 25 palavras
                    embaixo. Se um slide precisa de um parágrafo, são dois slides.
N+1       RESUMO    tudo numa lista. É o slide que vira print.
ÚLTIMO    PEDIDO    uma ação. Salvar, comentar uma palavra, mandar pra alguém ou
                    seguir. Uma.
```

## Regras do texto dos slides

- **A capa é 80% do resultado.** Seis palavras. Grande. Nada no resto salva uma
  capa que ninguém arrasta.
- **Desenha pro corte do grid.** O grid do perfil corta em retângulo vertical,
  e a proporção exata já mudou mais de uma vez. Monta em 1080x1350 e deixa o
  texto da capa bem no meio, longe dos 120 pixels de cada borda, e o corte deixa
  de importar.
- **Numera os slides** (3/8). Mais gente chega ao fim quando consegue ver o fim.
- **Nenhum slide é um parágrafo.** Se não cabe em 25 palavras, divide.
- **O slide de resumo é o que vira print e é enviado.** Envio é o sinal mais
  forte que dá pra ganhar. Faz ele se sustentar sozinho, legível sem contexto,
  inclusive num print aberto no WhatsApp.
- **O @ em todo slide**, pequeno, no canto de baixo. O print viaja sem você.
- **Texto alternativo pelo menos na capa.** É lido por leitor de tela e pelo
  Instagram.
- **Acento certo.** Erro de digitação em letra de 80px aparece, e no Brasil vira
  comentário antes de virar compartilhamento.

## Montando os arquivos

O Instagram quer 1080x1350 (4:5), JPEG ou PNG, até 20 itens. Monta em HTML e
imprime cada slide:

```bash
# uma <section> por slide, 1080x1350, page-break-after: always
# depois Chrome headless --print-to-pdf, ou qualquer HTML-pra-imagem que você já use
```

Escreve o HTML com `width:1080px; height:1350px`, uma cor de destaque só, e
fonte nunca menor que 32px, porque isso é lido num celular a um terço do tamanho
real. Se o projeto tem uma skill de marca ou um design system, usa e não inventa
paleta. Usa uma fonte com todos os acentos do português (ã, õ, ç, ê): fonte
display importada às vezes não tem e troca a letra por outra fonte no meio da
palavra.

## Saída

Primeiro o texto slide a slide, numa lista numerada que a pessoa lê em dez
segundos e edita antes de qualquer coisa ser gerada. Depois a **legenda**, que
num carrossel é o Trabalho B do `/ig-caption`: aqui a legenda trabalha, porque a
capa já gastou suas seis palavras.

Passa os dois pelo `/ig-human`. Só gera os arquivos depois que a pessoa aprovar o
texto.

```
CARROSSEL  ·  8 slides

1  CAPA    A CLÁUSULA DE R$ 18 MIL
           A linha que eu ponho em todo contrato.
2  RISCO   Eu aprovei o trabalho. Nove dias depois pediram o dinheiro de volta.
3          O QUE ELA DIZ
           Pagamento na entrega, não na aprovação.
...
7  RESUMO  As quatro linhas, em ordem.
8  PEDIDO  Comenta CONTRATO que eu te mando a cláusula inteira.

Legenda: Trabalho B, gancho na linha 1, um pedido, 3 hashtags.
```

Nada é enviado. A pessoa posta.
