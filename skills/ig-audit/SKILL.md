---
name: ig-audit
description: >-
  Faz o pós-morte do que a pessoa já postou - quais reels funcionaram de
  verdade, por quê, e o que parar de fazer. Funciona em português e em inglês.
  Use quando a pessoa colar o Insights ou os posts antigos e perguntar "o que tá
  funcionando", "por que esse flopou", "lê meus números", "faz uma auditoria do
  meu conteúdo", "audit my content", ou quiser saber do que fazer mais.
---

# ig-audit

A única fonte honesta do que funciona pra uma conta é a própria conta. Toda regra
de todo guia de Instagram, incluindo as deste pacote, é um palpite inicial. Os
últimos 30 posts da pessoa são a evidência.

## Entrada

Pede o que a pessoa tiver:

- Insights por post: visualizações, alcance, interações, tempo de visualização,
  salvamentos, compartilhamentos, seguidores ganhos e a parcela do alcance que
  veio de não seguidores. Print serve. (No app em português os nomes podem variar
  um pouco entre versões; o que importa é o número.)
- Ou o gráfico de retenção dos melhores e piores reels recentes. Esse print vale
  mais que todo o resto junto.
- Ou só os posts e as views, que dá pra uma primeira passada.

Lê também `~/.claude/instagram/log.md` se existir, porque ele registra a fórmula
de gancho de cada post.

## O que medir de verdade

View bruta é o número menos útil da página, porque é basicamente função de
quantas pessoas já seguem a conta. Calcula estes e mostra a conta:

| métrica | como | o que diz |
| --- | --- | --- |
| **Múltiplo** | views / mediana de views da própria conta | se foi um acerto ou um dia normal |
| **Alcance de não seguidores** | % do alcance vindo de quem não segue | se viajou ou não |
| **Retenção em 3s** | quem ainda estava lá em 3s / quem começou | se o gancho funcionou. É a nota do gancho. |
| **Tempo médio** | direto do Insights | se o meio funcionou |
| **Envios por alcance** | compartilhamentos / alcance | o sinal mais forte que dá pra ganhar. Um envio é alguém pondo o próprio nome naquilo. |
| **Seguidores por alcance** | seguidores ganhos / alcance | se o perfil converteu a atenção |

Ranqueia por múltiplo e por envios por alcance, não por view. Um reels com 4 mil
views e 90 envios ganhou do de 60 mil views e 11 envios.

No Brasil olha com carinho os envios: muito compartilhamento daqui vai pro
WhatsApp e pros grupos, e um post muito enviado com pouca curtida é um post que
as pessoas acharam útil demais pra só curtir.

## Depois acha o padrão

Com os cinco de cima e os cinco de baixo lado a lado, procura o que separa os
dois, e aceita concluir algo de que a pessoa não vai gostar:

- **Retenção em 3 segundos.** Se o de cima e o de baixo diferem aqui, é o gancho e
  só o gancho, e todo o resto é distração.
- **Fórmula do gancho.** Quais números do `ig-reel/hooks.pt.json` estão nos cinco
  de cima?
- **Formato.** Reels, carrossel, imagem única.
- **Duração.** Agrupa em menos de 15s, 15 a 30s, 30 a 60s, mais de 60s.
- **Tema.**
- **Áudio.** Original ou em alta.
- **Se a pessoa respondeu os comentários na primeira hora.**
- **Dia e horário.** Olha isso **por último** e só se o resto não mostrar nada.
  Quase nunca é a causa, e é onde as pessoas querem que seja.

Diz o achado como afirmação com a evidência junto, e diz o grau de confiança. Com
30 posts dá pra ver um padrão. Com 6 não dá, e dizer isso é melhor que inventar
um.

## A distinção que economiza meses

**Reels que tem view e não traz seguidor não é reels que falhou, é problema de
perfil.** Reels sem view é problema de gancho. Separa os dois antes de recomendar
qualquer coisa. Se o alcance de não seguidores é alto e os seguidores por alcance
são baixos, para de reescrever gancho e vai pro `/ig-profile`.

## Saída

```
AUDITORIA  ·  31 posts  ·  12 jun - 5 set  ·  mediana de views 4.100

TOP 5 POR MÚLTIPLO
  18,2x  #3  Ninguém Te Conta   74.600 views  62% não seguidores  ret@3s 71%  128 envios
   6,4x  #1  Confissão          26.300 views  48% não seguidores  ret@3s 64%   71 envios
  ...

ÚLTIMOS 5
   0,3x  #11 Lista               1.200 views   9% não seguidores  ret@3s 31%    2 envios
  ...

O QUE OS NÚMEROS DIZEM
1. A retenção em 3 segundos é a história inteira. Os cinco de cima têm média de
   66%, os de baixo 33%. Tudo o mais que te preocupa vem depois dos dois
   primeiros segundos.
2. Os posts em que você foi quem se deu mal: média de 8,1x contra 0,9x de todo o
   resto. n=5. É o sinal mais forte aqui e não é nem perto.
3. Lista de ferramentas dá view e mais nada. Alcance alto, sem envio, sem
   seguidor. Três dos seus cinco piores.
4. Dia da semana não mostra nada. As médias de terça e sexta estão dentro do
   ruído. Para de otimizar isso.

PARA: listas de ferramenta.
FAZ MAIS: os que têm um custo que você pagou e um número junto.
```

Depois passa as conclusões pro `/ig-plan`, pra próxima semana ser montada com a
evidência da própria pessoa em vez do padrão, e pro `/ig-viral`, pro arquivo de
referências ser filtrado pelas fórmulas que funcionam pra esta conta.
