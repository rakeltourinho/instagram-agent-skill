---
name: ig-plan
description: >-
  Monta a semana no Instagram - o que postar, em que formato, quando e com quem
  interagir - com o calendário comercial brasileiro. Funciona em português e em
  inglês. Use quando pedirem "planeja minha semana", "o que eu posto",
  "calendário de conteúdo", "cronograma", "não tenho o que postar", "plan my
  week", ou quando a pessoa quer frequência de posts e uma lista de interação.
---

# ig-plan

A sala de controle. Todo o resto do pacote executa; esta decide o que vai ser
executado. Roda uma vez por semana, sempre no mesmo dia.

## Entrada

Se `~/.claude/instagram/voice.md`, `swipe.md` e `log.md` existirem, lê. O swipe é
a evidência da própria pessoa, vinda do `/ig-viral`, sobre quais fórmulas estão
funcionando no nicho dela agora, e vale mais que qualquer coisa deste arquivo. O
log impede o plano de repetir um tema das últimas duas semanas.

Se não existirem, pede quatro coisas e anota:

1. O que a pessoa vende, e pra quem.
2. Os três ou quatro temas pelos quais ela quer ser conhecida.
3. O que aconteceu de verdade esta semana: uma conversa com cliente, um número,
   um erro, uma coisa que ela fez, uma discussão. É daí que os posts saem.
4. Dez contas pra quem vale a pena aparecer.

## O que postar

De quatro a cinco posts por semana, e pelo menos três deles Reels. Reels é o
único formato do Instagram que chega com regularidade em quem não segue a conta.
Carrossel aprofunda com quem já segue. Story é diário e é planejado à parte.

Mistura ao longo da semana, nunca dois do mesmo tipo seguidos:

| tipo | quantidade | trabalho |
| --- | --- | --- |
| **Prova** | 1 por semana | algo que aconteceu, com número. Reels. |
| **Ensino** | 1 a 2 por semana | uma coisa que dá pra fazer hoje. Reels ou carrossel. |
| **Opinião** | 1 por semana | uma posição que pode te fazer perder seguidor. Reels. |
| **História** | 1 a cada duas semanas | uma cena com um custo. Reels (storytime). |
| **Identificação** | 1 a cada duas semanas | POV, "quem é X sabe", expectativa x realidade. Reels. É o formato que mais vira envio no Brasil. |
| **Oferta** | 1 a cada duas semanas | o que você vende, dito sem rodeio e sem pedir desculpa. Carrossel ou stories. |

Pra cada espaço: o tema, o ângulo específico tirado do que aconteceu na semana, o
formato e o número da fórmula do `ig-reel/hooks.pt.json`. Não um assunto, um
ângulo. "IA" não é plano. "A proposta que a gente perdeu porque o rascunho tinha
um travessão" é um Reels.

## O calendário brasileiro

Antes de montar a semana, confere se ela encosta numa data que move o público
dela. As que mais mexem com consumo no Brasil:

| quando | data | pra quem |
| --- | --- | --- |
| jan-fev | volta às aulas, planejamento do ano, IPVA e IPTU | educação, finanças, papelaria |
| fev-mar | Carnaval (data móvel) | quase todo nicho, pra bem ou pra pausar |
| mar-mai | Imposto de Renda (o prazo da declaração costuma ir até o fim de maio; confere o do ano) | finanças, contabilidade, MEI |
| 8 de março | Dia Internacional da Mulher | marcas e criadoras com público feminino |
| maio, 2º domingo | Dia das Mães, a maior data do varejo depois do Natal | comércio, serviço, presente |
| 12 de junho | Dia dos Namorados (no Brasil não é em fevereiro) | presente, gastronomia, beleza |
| junho-julho | festas juninas, férias de julho | gastronomia, turismo, infantil |
| agosto, 2º domingo | Dia dos Pais | comércio, presente |
| 15 de setembro | Dia do Cliente | comércio e serviço |
| 12 de outubro | Dia das Crianças | infantil, brinquedo, educação |
| fim de novembro | Black Friday, a sexta depois do Thanksgiving americano (e o "esquenta" do mês inteiro) | quem vende qualquer coisa |
| nov-dez | 13º salário, Natal, retrospectiva, metas do ano novo | quase todo nicho |

Data comercial é pra quem vende. Pra quem ensina ou opina, a data serve de
gancho ("o que ninguém te conta sobre a Black Friday da sua loja"), não de
promoção. Não força data que não tem nada a ver com o público.

## Quando postar

Posta quando o público está acordado e fora do trabalho. Pra muito público
consumidor no Brasil isso é o horário do almoço e o começo da noite, depois do
expediente e do trânsito. Pra público de negócio, cedo de manhã. Mas o padrão
vale menos que o Insights da própria conta: a aba de público mostra os horários
em que os seguidores dela estão ativos, e é esse número que manda.

Fala isso com todas as letras: **o horário importa muito menos que os dois
primeiros segundos.** O Instagram continua mostrando um Reels por dias se ele vai
bem, e enterra um bem cronometrado que vai mal. Se a pessoa está otimizando
horário antes de o gancho funcionar, está polindo a coisa errada, e você tem que
dizer isso.

Usa o fuso do público, não o da pessoa. O Brasil tem quatro: a maior parte do
país está no horário de Brasília; Amazonas, Roraima, Rondônia, Mato Grosso e Mato
Grosso do Sul estão uma hora atrás; o Acre, duas; e Fernando de Noronha, uma à
frente.

## A rodada de interação, que não é opcional

20 minutos por dia, antes de postar, não depois. Monta uma lista de 10:

- **5 de alcance** - contas com o público que a pessoa quer, onde um bom
  comentário é visto. Comenta cedo, antes de o post ter 200 comentários.
- **3 pares** - mesmo tamanho, mesma área. É o grupo que retribui.
- **2 compradores** - gente que pode comprar de verdade. Comenta por semanas
  antes de qualquer DM, e nunca oferece nada num comentário.

Passa a lista pro `/ig-comment`.

Grupo de engajamento ("pod", o grupo de WhatsApp em que todo mundo curte todo
mundo) não entra nessa lista. Interação de quem não é o público ensina o
Instagram a mostrar o post pra gente errada.

## Saída

```
SEMANA DE 15 DE SETEMBRO  (Dia do Cliente na segunda)

SEG  só interação (20 min, lista abaixo) + stories do Dia do Cliente
TER  19h30  REELS      PROVA          #5  Tempo Encurtado   - proposta de 5h pra 20 min
QUA  só stories + interação
QUI  12h00  CARROSSEL  ENSINO         Trabalho B            - a cláusula em 4 slides
SEX  19h30  REELS      OPINIÃO        #2  Ordem Negativa    - para de fazer reunião de briefing
SÁB  -
DOM  18h00  REELS      IDENTIFICAÇÃO  #27 POV               - "é só uma alteraçãozinha"

STORIES  todo dia, 3 a 5 frames, caixinha de pergunta na quinta.

INTERAÇÃO  (5 alcance / 3 pares / 2 compradores)
  ...

Fala "escreve a terça" que eu rascunho.
```

Escreve o plano em `~/.claude/instagram/plan.md` pras outras skills lerem. Nada é
agendado nem publicado em lugar nenhum. É um plano, e quem executa é a pessoa.
