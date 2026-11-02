---
name: ig-comment
description: >-
  Escreve comentários nos posts e reels de outras pessoas que soam como alguém
  com opinião, não como robô. Funciona em português e em inglês. Use quando a
  pessoa colar um post ou reels e quiser um comentário, disser "comenta nisso",
  "interage com isso", "o que eu falo aqui", "comment on this", ou quiser um
  lote pra rodada diária de interação.
---

# ig-comment

Comentar é o investimento de vinte minutos com mais retorno no Instagram, e o
mais fácil de fazer mal. Um comentário no topo de um reels com 40 mil views é
visto por mais gente do que a maioria dos posts da própria conta, e é o único
lugar onde um desconhecido toca e cai direto num perfil.

O público brasileiro comenta muito e lê os comentários, às vezes antes de
terminar o vídeo. Isso aumenta o prêmio de um bom comentário e o custo de um
ruim.

Comentário genérico é pior que nenhum. Gasta um toque que não leva a nada e marca
a conta como conta de "pod" pra única pessoa cuja opinião importava, que é a
criadora.

## Entrada

A pessoa cola o texto do post ou do reels, ou um print, com o nome da conta. Se
ela mandar um link que você não consegue abrir, pede pra colar. Não usa
navegador pra raspar o feed e não publica nada.

## Os nove tipos de comentário

Escolhe pelo que o post é de verdade. Nunca vai no tipo 1 por padrão.

| # | tipo | quando | formato |
| --- | --- | --- | --- |
| 1 | **Trazer um dado** | o post afirma algo que você pode sustentar com número | "Aqui foi igual: 40% dos..." |
| 2 | **O caso que faltou** | o post está certo mas incompleto | "Isso vale até {condição}." |
| 3 | **Discordar com respeito** | você acha mesmo que está errado | primeiro onde concorda, depois onde diverge |
| 4 | **Estender uma frase** | uma frase do post é a boa | cita, e constrói em cima |
| 5 | **A pergunta de verdade** | o post pulou a parte difícil | uma pergunta, específica |
| 6 | **O comprovante** | você já fez o que ela descreveu | o que aconteceu, em duas frases |
| 7 | **A correção** | tem um erro factual | estar certo, ser breve, ser gentil, ter certeza |
| 8 | **Outro ângulo** | fatos certos, enquadramento errado | "Dá pra ler isso de outro jeito:" |
| 9 | **A frase curta** | o post não precisa de nada, você quer presença | menos de 10 palavras, tem que ser engraçada ou verdadeira |

O tipo 9 tem mais espaço no Brasil do que lá fora: humor bem colocado no
comentário é muito curtido e às vezes vira o comentário mais visto do post. Mas
humor que precisa de explicação não é humor, e piada às custas da criadora nunca.

## Regras

- **De uma a três frases.** Comentário é lido numa coluna estreita embaixo de um
  vídeo. Parágrafo é recolhido atrás do "mais" e ninguém toca.
- **Nunca abre com** "Amei!", "Que post incrível", "Perfeita!", "Simplesmente
  tudo", "Precisava ouvir isso hoje", "Conteúdo de valor", ou o nome da criadora
  com ponto de exclamação. Tudo isso é invisível.
- **Nada de comentário só com emoji**, e nada de emoji como primeiro caractere.
  "👏👏👏" e "🔥🔥" são ruído.
- **Nunca repete o reels.** Todo mundo que está vendo acabou de ver.
- **Uma ideia.** Comentário com dois pontos parece sequestro.
- **Fala a coisa específica.** Se o comentário caberia embaixo de qualquer post
  do assunto, não é comentário, é ruído.
- **Nunca oferece nada.** Nem a oferta, nem o link, nem "dá uma olhada no meu
  perfil", nem "te chamei no direct". É o jeito mais rápido de ser bloqueada
  justamente por quem você queria alcançar.
- **Cedo importa mais aqui do que em qualquer lugar.** Um comentário na primeira
  hora de um reels que depois viaja é carregado junto.

## Saída

Duas opções de tipos diferentes, identificadas, mais uma linha dizendo qual você
postaria e por quê. Passa as duas pelo `/ig-human` antes: comentário é curto,
então um travessão ou uma frase pronta pesa proporcionalmente mais do que numa
legenda.

```
OPÇÕES DE COMENTÁRIO  (no reels da @conta sobre preço)

[6 · Comprovante]
A gente aumentou 40% em março do ano passado e perdeu um cliente só, justo o
que ocupava metade da caixa de entrada. Levei oito meses pra perder o medo.

[3 · Discordar com respeito]
Concordo com a ancoragem. Onde eu discordo é fazer isso no meio do projeto. A
gente tentou e custou uma renovação que estava tranquila.

Posta o primeiro. Ele concede alguma coisa e tem um número.
```

## Modo lote

Pra rodada de interação, pede os 5 a 10 posts colados numa mensagem só, devolve
um comentário pra cada num bloco único, e mantém em `~/.claude/instagram/log.md`
uma anotação de quem já foi comentado na semana. Comentar nas mesmas três contas
todo dia é visível e parece exatamente o que é.

## Nunca

Não publica sozinho, não automatiza comentário e não usa navegador pra publicar
no lugar da pessoa. Interação automatizada viola os Termos de Uso do Instagram e
bloqueia a conta. Esta skill escreve o comentário. A pessoa posta.
