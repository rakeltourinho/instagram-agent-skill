---
name: ig-viral
description: >-
  Vai atrás dos reels que estão funcionando agora no nicho da pessoa, ranqueia
  pelo quanto cada um superou a própria conta, nomeia a fórmula de gancho de
  cada um e transforma isso num arquivo de referências pra gravar. Funciona com
  perfis brasileiros e gringos. Use quando pedirem "acha vídeos virais", "o que
  tá funcionando agora", "o que estão postando no meu nicho", "faz engenharia
  reversa desse perfil", "monta um swipe file", "por que esse reels bombou",
  "find viral videos", ou quando perguntam o que fazer a seguir e não têm
  evidência pra responder.
---

# ig-viral

A skill de pesquisa. Todo o resto do pacote escreve; esta vai e olha. Roda uma
vez por mês, não todo dia. Fórmula dura uma temporada.

Uma ferramenta mora nesta pasta e ela roda:

```bash
python3 swipe.py capturados.tsv --out ~/.claude/instagram/swipe.md
```

## A única ideia que faz isso valer a pena

**View bruta não é evidência.** Um perfil de dois milhões de seguidores fazendo
400 mil views teve uma terça fraca. Um perfil de quatro mil seguidores fazendo
400 mil views achou alguma coisa, e essa coisa dá pra copiar.

Então tudo aqui é ranqueado pelo **múltiplo**: views divididas pela mediana
recente daquela conta. Acima de 3x é sinal. Abaixo de 1,5x é o dia normal da
conta e não ensina nada, por maior que o número pareça.

Coleta contas **até umas 10x o tamanho da pessoa**. Fórmula que funciona com 2
milhões de seguidores muitas vezes funciona porque tem 2 milhões de seguidores.

## Passo 1: escolher as contas

Pede à pessoa de 6 a 12 contas, ou sugere e pede aprovação:

- **4 diretas** - mesmo nicho, mesma oferta, um pouco à frente.
- **4 vizinhas** - outro nicho, mesmo público. É daqui que os formatos são
  emprestados antes de alguém do nicho ter.
- **2 a 4 grandes** - contas bem maiores, só pelo formato, nunca pela
  frequência ou pelo tom.

**Mistura Brasil e gringa com critério.** Formato gringo costuma chegar aqui
alguns meses depois, então olhar contas americanas do mesmo nicho é um jeito
legítimo de ver o que vem. Mas humor, gíria, referência e ritmo não viajam:
copia a estrutura, nunca a piada. E o que funciona no Brasil tem coisas que lá
fora não tem (POV de identificação, storytime longo, achadinho, humor com
regionalismo), então pelo menos metade das contas deve ser brasileira.

Pede também pra pessoa abrir a **coleção de Salvos** dela. É o corpus mais
rápido e mais relevante que existe, e já vem filtrado pelo gosto dela.

## Passo 2: ir lá e olhar

Usa a ferramenta de navegação que esta sessão tiver de verdade: navegador
embutido, extensão conectada ao Chrome da própria pessoa, ou uma ferramenta de
uso de computador. Não tem API pra isso e não precisa ter, porque o volume é
pequeno o bastante pra ler.

**Regras que não se negociam:**

- **Nunca entra no Instagram no lugar da pessoa e nunca pede senha.** Se a
  página pede login, quem já está logada é ela. Conduz o navegador dela com
  ela presente, ou pede pra ela colar.
- **Isso é leitura, não raspagem.** Dez contas, uma dúzia de reels cada, em
  velocidade humana. Coleta automatizada em volume viola os Termos de Uso do
  Instagram e bloqueia contas. Não constrói crawler, não usa serviço de scraping
  e não roda isso em segundo plano.
- **Copia a fórmula, nunca o vídeo.** O formato do gancho, a estrutura, a
  duração, o padrão de cortes. Não o roteiro, não a voz, não a edição. Atribui
  cada linha do arquivo à conta de onde veio.

**O que capturar por reels**, nas palavras da própria criadora:

| campo | notas |
| --- | --- |
| account | @ |
| followers | do perfil, do jeito que aparece ("48,2 mil" serve) |
| median | olha os últimos 12 reels e pega a view do meio |
| views | deste reels ("412 mil", "1,2 mi" e "48k" servem) |
| hook | a primeira frase, falada ou na tela, literal, com erro de português e tudo |
| on-screen | a primeira cartela, se for diferente |
| length | segundos |
| cta | o que ela pediu no fim |
| audio | áudio original ou áudio em alta |

A mediana é o que importa. Sem ela você volta a ranquear por seguidor, que é
exatamente o que esta skill existe pra impedir.

**Quando o Instagram não mostrar o bastante:** a mesma gramática de gancho
roda no YouTube Shorts, onde views e transcrição são públicas e não precisa de
login. É um segundo corpus legítimo, e o gancho falado é mais fácil de pegar:

```bash
# views dos shorts de um canal
python3 -m yt_dlp --flat-playlist --playlist-end 40 -J \
  "https://www.youtube.com/@CANAL/shorts" > canal.json

# a primeira frase falada de um short, pela legenda automática
python3 -m yt_dlp --skip-download --write-auto-subs --sub-langs "pt.*" \
  --sub-format json3 -o gancho "https://www.youtube.com/watch?v=ID_DO_VIDEO"
```

Pega toda palavra da legenda com tempo abaixo de 3,0 segundos. Esse é o gancho,
como foi dito, não como foi escrito. Pra canal gringo, troca `pt.*` por `en.*`.

## Passo 3: ranquear

Preenche um arquivo separado por tabulação com uma linha de cabeçalho e roda o
script:

```
account	followers	median	views	hook
@confeitaria	4,8 mil	3 mil	412 mil	Ninguém te conta que bolo de pote não dá lucro
```

```bash
python3 swipe.py capturados.tsv --out ~/.claude/instagram/swipe.md
```

Ele calcula o múltiplo, nomeia a fórmula do gancho com as mesmas fórmulas que o
`/ig-reel` usa pra escrever (gancho em português contra `hooks.pt.json`, em
inglês contra `hooks.json`), pontua cada gancho com o `hookscore.py` e mostra o
que separa o terço de cima do terço de baixo.

## Passo 4: dizer o que significa, com cuidado

Relata três coisas e só:

1. **Quais fórmulas aparecem mais** no terço de cima, com contagem. Duas
   fórmulas aparecendo quatro vezes cada em seis contas é achado. Uma
   aparecendo duas vezes não é.
2. **O que o terço de cima tem em comum** na estrutura e o de baixo não tem:
   tamanho do gancho, se a entrega é visual, se o primeiro frame se mexe, onde
   está o pedido, se usa áudio em alta ou original.
3. **As linhas sem classificação.** Todo gancho que o classificador não
   reconheceu é ruído ou é uma fórmula que ainda não está no `hooks.pt.json`.
   Lê à mão. É a coluna mais valiosa da saída e é por isso que o script mostra a
   contagem. Se o mesmo formato aparecer três vezes, sugere adicionar ao
   `hooks.pt.json`, com modelo, exemplo e regex.

Depois diz o tamanho da amostra e a confiança em palavras simples. Quarenta
reels em seis contas sustentam uma afirmação. Doze não, e dizer isso é a
diferença entre pesquisa e horóscopo.

## Passo 5: virar algo pra gravar

Pras três fórmulas de cima, escreve **a versão da pessoa**: a história dela, o
número dela, no formato que está funcionando. Passa cada uma pro `/ig-reel` com
o número da fórmula já escolhido.

Nunca devolve "faz um reels igual esse". Devolve uma frase de gancho que ela
poderia falar amanhã.

## Saída

```
SWIPE  ·  38 reels  ·  7 contas  ·  base: mediana da conta

FORA DA CURVA (acima de 3x)
  137,3x  gancho 87  #3  Ninguém Te Conta   @conta_a    412.000  (mediana 3.000)
   90,0x  gancho 41  #27 POV                @conta_c    180.000  (mediana 2.000)
  ...

O QUE ESTÁ APARECENDO MAIS
  #27 POV               x5 no terço de cima, 0 no de baixo
  #3  Ninguém Te Conta  x4
  tamanho do gancho     8 palavras em cima, 19 embaixo

SEM CLASSIFICAÇÃO (6)
  Dois têm o mesmo formato e ele não está no hooks.pt.json: um gancho que
  começa lendo em voz alta o comentário de outra pessoa. Vale adicionar.

SUA VERSÃO
  #27  "POV: você manda o orçamento e a cliente responde 'nossa, achei que era mais barato'."
  ...
```

Repara que o POV tirou nota 41 no `hookscore.py` e mesmo assim fez 90x. É o
limite honesto da ferramenta: POV vive de identificação, de cena e de atuação,
coisas que um script que lê texto não vê. Quando a nota e o múltiplo
discordam, acredita no múltiplo.

Escreve o arquivo em `~/.claude/instagram/swipe.md`. O `/ig-reel` e o
`/ig-plan` leem esse arquivo, e é essa a ideia: depois que isto roda uma vez, o
resto do pacote trabalha com a evidência da própria pessoa em vez do padrão.

Nada é publicado, seguido, curtido ou enviado por esta skill. Ela lê.
