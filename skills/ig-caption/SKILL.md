---
name: ig-caption
description: >-
  Escreve a legenda do Instagram - a linha que sobrevive ao corte do "... mais",
  o corpo, o pedido único, os termos de busca e até cinco hashtags - e revisa
  antes de sair. Funciona em português e em inglês. Use quando pedirem
  "escreve a legenda", "legenda pra esse post", "o que eu ponho na descrição",
  "quais hashtags", "write the caption", ou quando a pessoa tem um reels ou um
  carrossel pronto e precisa do texto.
---

# ig-caption

Uma ferramenta mora nesta pasta e ela roda:

```bash
python3 caption.py legenda.txt
python3 caption.py legenda.txt --keywords "contrato freelancer,precificação de design"
```

Ela imprime a legenda do jeito que o feed imprime: os primeiros 125 caracteres
numa caixa, o resto atrás do toque. Lê essa caixa antes de ler qualquer outra
coisa que você escreveu.

Reconhece os dois idiomas ao mesmo tempo, sem flag: os pedidos em português
("comenta CONTRATO", "me chama na DM", "salva esse post", "manda pro sócio",
"link na bio"), as hashtags genéricas daqui (#explorar, #reelsbrasil,
#viralizar) e o que é concreto (R$ 18 mil, WhatsApp, março).

## Primeiro, decide qual é o trabalho dessa legenda

É essa decisão que estraga legenda quando é pulada.

**Trabalho A: o vídeo já prendeu.** O Reels carrega o próprio gancho nos dois
primeiros segundos, falado e na tela. A legenda não é um segundo gancho, e
competir com o vídeo é o jeito de perder os dois. O trabalho dela é o pedido, o
contexto que faz o pedido fazer sentido e as palavras que as pessoas buscam.

**Trabalho B: a legenda é o conteúdo.** Uma foto, uma imagem única, a capa de
um carrossel que abre uma curiosidade. Aqui a linha um é o gancho e funciona
igual ao gancho de Reels: concreta, curta, cortada num suspense e não no meio
de uma oração.

Diz qual dos dois você está escrevendo. Se a pessoa tem um Reels com gancho
forte, escreve o A e explica por quê.

## O formato

```
Linha 1     125 caracteres visíveis. Trabalho A: o pedido, direto.
            Trabalho B: o gancho.
            Nunca um cumprimento ("Oi, gente!"), nunca hashtag, nunca emoji
            como primeiro caractere.
Corpo       parágrafos curtos, uma linha em branco entre eles. De dois a seis.
            É aqui que moram os termos de busca.
O pedido    um. Comenta uma palavra, salva, manda pra alguém ou chama na DM. Um.
Hashtags    até cinco, numa linha própria no fim, ou nenhuma.
```

O limite é 2.200 caracteres e quase nada precisa disso. Uma legenda que ganha o
toque e entrega 600 caracteres vence uma que entrega 1.800.

## Hashtags, com honestidade

Hashtag não é mais alavanca de alcance, e a plataforma já disse isso com uma
mudança de produto. **O Instagram limitou as hashtags a cinco por post em 18 de
dezembro de 2025**, caindo de trinta, dizendo aos criadores que usar menos
hashtags (até 5) e mais específicas, em vez de muitas genéricas, funciona
melhor. O Adam Mosseri já tinha dito em fevereiro de 2025 que hashtag não
aumenta alcance: é etiqueta, não distribuição.

Então: até cinco, específicas, como etiqueta de tema. Se a pessoa tem um bloco
de vinte salvo no bloco de notas, esse bloco virou peso morto e o `caption.py`
vai reprovar.

`#viral`, `#explorar`, `#reelsbrasil`, `#fyp`, `#sucesso`, `#motivação` não
descrevem nada. Corta.

## Termo de busca importa mais que hashtag

A busca do Instagram lê o texto da legenda. Então a frase pela qual a pessoa
quer ser encontrada vai na legenda do jeito que alguém digitaria, numa frase
normal. "Contrato de freelancer" escrito na linha três, não "#contratodefreelancer"
num bloco lá embaixo.

Pensa em como o brasileiro busca: com acento e sem acento, no singular, com a
cidade quando é negócio local ("confeitaria em Curitiba", "psicóloga online").
Negócio local deve pôr bairro e cidade na legenda e no perfil.

Pede dois ou três termos e passa pro `caption.py`:

```bash
python3 caption.py rascunho.txt --keywords "contrato de freelancer,precificação de design"
```

## O pedido, do jeito brasileiro

- **Palavra-chave nos comentários** ("Comenta CONTRATO que eu te mando") é muito
  comum aqui e funciona, porque o público já sabe o que acontece depois: chega
  uma DM. Uma palavra, sem espaço, sem emoji, e escrita em maiúscula. Fala ela no
  vídeo também. `Comenta CONTRATO` funciona. `Comenta "quero o guia do
  contrato"` não. Evita `EU QUERO`: todo perfil usa, então não diz nada sobre o
  seu post.
- **Mandar pra alguém** é o pedido mais forte que existe, porque o envio é o
  sinal que o Instagram mais valoriza, e no Brasil boa parte disso vai pro
  WhatsApp. Pede pra mandar pra uma pessoa específica: "manda pro sócio que
  ainda cobra na aprovação", "manda no grupo da família". "Compartilha com quem
  precisa" é genérico e o `/ig-human` corta.
- **Salvar** é o pedido certo pra conteúdo de consulta: lista, passo a passo,
  receita, roteiro.

## Regras

- **Nada de link na legenda.** Legenda não é clicável. URL no corpo é texto morto
  que diz "eu não uso esta plataforma". Bio, story com link ou DM.
- **Um pedido.** Dois pedidos é o mesmo que nenhum. O `caption.py` conta.
- **Publi tem que dizer que é publi.** Post pago, permuta ou link de afiliado:
  marca como parceria paga e escreve "publi" ou "#publi" logo no começo. É o que
  o guia do CONAR pede pra influenciadores, e o público brasileiro perdoa a
  publi mas não perdoa a publi escondida.
- **Escreve o primeiro comentário separado** se tiver link ou informação extra.
  Diz isso no recibo.
- **Emoji como pontuação, não enfeite.** O `caption.py` aponta mais de 4 a cada
  100 caracteres.
- **Texto alternativo vale 20 segundos.** Em carrossel e foto, escreve. É lido
  por leitor de tela e pelo Instagram.

## O ciclo

1. Decide Trabalho A ou B e diz qual.
2. Rascunha.
3. Passa pelo `/ig-human`. Legenda é curta, então o vício aparece mais aqui do
   que em qualquer outro lugar do pacote.
4. Roda `caption.py` com os termos de busca da pessoa. Corrige todo FAIL. Decide
   cada WARN em voz alta em vez de ignorar em silêncio.
5. Entrega o bloco pronto pra copiar e depois o recibo:

```
LEGENDA PRONTA
trabalho:   A - o reels carrega o gancho
visível:    118 de 125 caracteres usados antes do corte
pedido:     um, comenta CONTRATO
hashtags:   3
busca:      "contrato de freelancer" na linha 3, "precificação" na linha 5
revisão:    READY
```

Nada é publicado. A pessoa cola.
