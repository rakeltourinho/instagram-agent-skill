---
name: ig-reel
description: >-
  Escreve um Reels do Instagram a partir de uma ideia crua - opções de gancho
  tiradas de 32 fórmulas em português (26 clássicas + 6 formatos brasileiros
  como POV, storytime e achadinho), o roteiro falado, o texto da tela e uma
  decupagem cronometrada - na voz da própria pessoa e com o gancho pontuado
  antes de gravar. Use sempre que pedirem um reels, roteiro de vídeo curto,
  gancho, locução, "faz um reels sobre X", "o que eu falo nesse vídeo", "write
  a reel", ou quando a pessoa vai gravar e ainda não tem a primeira frase.
---

# ig-reel

Transforma uma ideia crua num Reels que alguém assiste até o fim.

Duas ferramentas moram nesta pasta e as duas rodam de verdade. Usa elas. Não
avalia o gancho no olho e não chuta a duração.

```bash
python3 hookscore.py ganchos.txt             # ranqueia as opções de gancho
python3 hookscore.py --hook "uma frase"      # pontua uma só
python3 beats.py roteiro.txt --target 30     # decupagem cronometrada antes de gravar
```

As duas detectam o idioma sozinhas (português ou inglês). `--lang pt` força o
português. Em português, `beats.py` cronometra a 150 palavras por minuto, porque
a palavra em português tem mais sílaba; se a pessoa já se cronometrou lendo um
roteiro, passa `--wpm` com o número dela.

## Idioma

Escreve no idioma da pessoa. Se ela escreveu em português, tudo sai em
português do Brasil, do jeito que se fala: "tá", "pra", "a gente", "você".
Nada de português de Portugal ("estou a fazer", "telemóvel", "ecrã") e nada de
português de redação ("estamos", "para", "realizar") num texto que vai ser
falado. Se ela escreveu em inglês, usa `hooks.json` e escreve em inglês.

## Antes de escrever

1. Lê `~/.claude/instagram/voice.md` se existir. É o perfil de voz da pessoa:
   como ela fala na câmera, o que nunca diz, com quem está falando, se usa
   gíria regional ("bah", "uai", "oxe", "mano"). Se não existir, pede **três
   reels dela**, transcreve ou lê, deduz a voz e escreve o arquivo. Roteiro na
   voz errada não serve, porque ela vai ter que falar em voz alta.
2. Lê `hooks.pt.json` nesta pasta (ou `hooks.json` em inglês). São 32
   fórmulas, cada uma com modelo, exemplo preenchido, versão de tela, pra que
   serve e como costuma ser estragada. As seis últimas (POV, Quem É Sabe,
   Testei Pra Você, O Dia Em Que, Achadinho, Expectativa x Realidade) são
   formatos muito fortes no Instagram brasileiro e não existem na versão em
   inglês.
3. Se a ideia está rasa, não enche linguiça. Faz uma pergunta só, agrupada: o
   que aconteceu, com quem, e quanto custou ou rendeu. Reels precisa de uma
   coisa específica e verdadeira. Consegue ela antes de escrever.
4. Se `~/.claude/instagram/swipe.md` existir, lê. O `/ig-viral` escreve esse
   arquivo, e é a evidência da própria pessoa sobre quais fórmulas estão
   funcionando no nicho dela agora. Vale mais que o padrão deste arquivo.

## O formato

Um Reels é decidido nos dois primeiros segundos e mantido nos cinco seguintes.

```
0:00 - 0:02   GANCHO      a afirmação. Frase falada e frase da tela, escritas
                          separadas. Movimento no primeiro frame, não rosto parado.
0:02 - 0:07   O RISCO     por que isso importa pra quem está assistindo. Uma frase.
0:07 - ...    O CORPO     uma ideia por batida, e o enquadramento muda a cada batida.
ÚLTIMOS 3s    A ENTREGA   cumpre o que o gancho prometeu, depois o pedido único.
ÚLTIMA FRASE  O LOOP      repete uma palavra do gancho pra o replay emendar limpo.
```

Duração: de 15 a 45 segundos é a faixa que funciona. Reels vai até 3 minutos e
quase ninguém deveria usar isso. Abaixo de 7 segundos os loops inflam a conta e
mais nada.

Storytime ("O dia em que...") é a exceção que confirma a regra: o público
brasileiro assiste história longa até o fim quando a virada aparece antes da
metade. Pode ir a 60-90 segundos, desde que cada batida mude alguma coisa.

## O ciclo

**1. Escolhe três ganchos, não um.** Passa a ideia pelo `hooks.pt.json`,
escolhe três fórmulas que encaixam de verdade e escreve a frase falada e a
frase da tela de cada uma. Fórmulas diferentes, não três versões da mesma.

**2. Pontua.** Põe as três frases faladas num arquivo, uma por linha, e roda
`hookscore.py`. Mostra o ranking pra pessoa. Se a primeira está abaixo de 50,
ainda não tem gancho, e nenhuma edição resolve isso.

**3. Escreve o roteiro** em cima do gancho vencedor. Português falado, do jeito
que a pessoa fala de verdade. Frase curta. Nenhuma frase que ela precise
ensaiar.

**4. Cronometra.** Roda `beats.py roteiro.txt --target {duração}`. Corrige todo
alerta: gancho passando de 3 segundos, batida acima de 4 segundos, sequência de
batidas sem nada concreto, sem loop. Roda de novo até ficar limpo.

**5. Humaniza.** Passa o roteiro pelo `/ig-human` antes de mostrar. Frase com
cara de escrita fica óbvia no momento em que alguém fala em voz alta.

**6. Entrega o bloco.** O roteiro num bloco de código, o texto da tela numa
lista separada com os tempos, e depois:

```
REELS PRONTO
gancho:     #3 Ninguém Te Conta, nota 87 STRONG
duração:    25,2s em 7 batidas a 150 ppm
na tela:    6 cartelas
humanizer:  4 vícios removidos, nota humana 81 PASS
legenda:    roda /ig-caption em seguida

Responde "sim" pra registrar, ou me diz o que mudar.
```

**7. Nunca publica.** Esta skill produz roteiro. A pessoa grava e posta. No
"sim", acrescenta em `~/.claude/instagram/log.md` a data, a fórmula usada e a
primeira frase, pro `/ig-audit` ter histórico depois.

## O texto da tela é outro roteiro

Escreve separado, sempre. Ele é lido antes de ser ouvido.

- **Seis palavras ou menos por cartela.** Está sendo lido a um braço de
  distância por alguém que ainda não está ouvindo.
- **A cartela do gancho aparece no frame 1**, não depois de um segundo de
  silêncio.
- **Fica dentro da área segura.** Num frame 1080x1920, nada acima de y=230 nem
  abaixo de y=1440, e deixa livres os 230 pixels da direita. A interface fica
  em cima de tudo que está fora dessa caixa: legenda, botões, faixa de áudio.
- **Nunca põe o gancho onde fica a legenda.** É a parte de baixo do frame e
  está coberta.
- **Legenda embutida no corpo.** A maioria assiste sem som primeiro, ainda mais
  no ônibus, no metrô e no trabalho.

## Regras que fazem diferença

- **Uma ideia por Reels.** Se o roteiro tem duas, são dois Reels. Fala isso.
- **Número em vez de adjetivo.** "R$ 4.200" ganha de "muito dinheiro". Se a
  pessoa não deu o número, pergunta, em vez de escrever em volta do buraco.
- **Corta a introdução.** Sem "oi gente", sem "fala galera", sem "nesse vídeo",
  sem nome, sem vinheta. O vídeo começa na frase que você normalmente diria no
  sexto segundo.
- **Muda o enquadramento a cada batida.** Plano parado por 8 segundos é onde as
  pessoas saem, e o `beats.py` vai apontar.
- **Um pedido no fim.** Comenta uma palavra, salva, ou manda pra alguém
  específico ("manda pro sócio que ainda cobra na aprovação"). Um.
- **Nunca inventa.** Nada de métrica, cliente, faturamento ou resultado
  inventado no nome da pessoa, nem como exemplo. Se precisa de um número e ele
  é desconhecido, deixa `{{seu número}}` no roteiro e avisa.
- **Áudio em alta só se a pessoa pode usar.** Conta comercial tem acesso
  limitado à biblioteca de músicas; se a ideia depende de um áudio do momento,
  confirma o tipo de conta. Se a ideia precisa da voz dela, fala isso.
- **Publi é publi.** Se o vídeo é pago, permuta ou tem link de afiliado, lembra
  de marcar como parceria paga e de dizer "publi" no vídeo ou na legenda. É o
  que o CONAR pede, e esconder isso queima a confiança.

## Exemplo

```
/ig-reel a gente cortou o tempo de proposta de 5 horas pra 20 minutos com um modelo
```

```
GANCHOS  (pontuados)
  87  STRONG  #3  Ninguém Te Conta    "Ninguém te conta que proposta não precisa de cinco horas."
                                      na tela: 5 HORAS? NÃO.
  81  STRONG  #1  Confissão           "Eu cobrava quatro horas por semana só pra formatar. Por dois anos."
                                      na tela: 2 ANOS JOGADOS FORA
  55  OK      #5  Tempo Encurtado     "Proposta me tomava cinco horas. Hoje leva vinte minutos."
                                      na tela: 5 HORAS -> 20 MIN

Gravando o #5 mesmo com nota menor: a proporção é crível, lê numa olhada na
tela, e o número é seu. O #3 promete mais do que o vídeo entrega.
```

Repara no último parágrafo: o script pontua texto, não decide o vídeo. Quando a
nota e o bom senso discordam, explica a escolha.
