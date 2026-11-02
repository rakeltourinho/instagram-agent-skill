---
name: ig-profile
description: >-
  Dá nota de 0 a 100 pra um perfil do Instagram numa régua de 12 itens e
  reescreve o que perdeu ponto - campo de nome, bio, link, destaques, os três
  fixados, grid. Funciona em português e em inglês. Use quando pedirem
  "otimiza meu perfil", "arruma minha bio", "dá nota pro meu Instagram", "por
  que ninguém me segue", "optimize my profile", ou quando colarem o perfil e
  perguntarem como ele se lê.
---

# ig-profile

Quase todo mundo otimiza a coisa errada aqui. O perfil não é uma vitrine que as
pessoas ficam olhando. É uma **tela de decisão**, à qual se chega a partir de um
Reels, e ela tem uns três segundos pra responder uma pergunta: tem mais disso
aqui, e é pra mim?

## Entrada

Pede pra pessoa colar ou mandar print: o campo de nome, o @, a bio, pra onde vai
o link, o nome dos destaques, o que está fixado e as nove primeiras capas do
grid. Um print do topo do perfil mais as duas primeiras linhas do grid basta pra
uma primeira passada.

Não entra no Instagram no lugar dela.

## A nota

Lê `rubric.json` nesta pasta. Doze itens, 100 pontos, cada um com o que é nota
cheia e como costuma falhar (em português; o original em inglês está nos campos
`*_en`). Pontua todos, mostra a tabela, dá o total. Com honestidade. A maioria
dos perfis tira entre 30 e 49 na primeira passada, e nota generosa não serve pra
nada.

```
NOTA DO PERFIL  38/100

  campo de nome     2/12   só o nome, nenhuma palavra que alguém busca
  bio, linha 1      3/12   três substantivos e um emoji de café
  três fixados      0/10   nada fixado
  destaques         2/8    "Aleatório", "Vida", "2023"
  grid legível      4/8    seis das nove capas são um rosto no meio da frase
  ...
```

## Depois reescreve, nesta ordem

Corrige do que perdeu mais ponto pro que perdeu menos. Não reescreve tudo de uma
vez, a pessoa tem que ir lá e mudar cada coisa.

**1. O campo de nome (30 caracteres).** A linha em negrito embaixo da foto, não o
@. É o campo que a busca do Instagram usa, e a maioria das contas põe só um nome.
O formato que funciona: `{Nome} | {o que faz, nas palavras que buscam}`. Negócio
local põe cidade ou bairro: `Ana | Confeitaria em Curitiba`. Dá três opções. Pensa
em como o brasileiro digita na busca: sem acento muitas vezes, e com a palavra
mais comum ("psicóloga", não "psicoterapeuta clínica").

**2. Bio, linha um.** Pra quem é e o que muda. Não é cargo, não é adjetivo, não é
lista de identidades separada por barra. O resto dos 150 caracteres leva uma
prova ou uma oferta direta.

**3. Os três fixados.** Três espaços, três trabalhos: a melhor prova, a
explicação mais clara da oferta, a melhor apresentação da pessoa. É a correção de
maior impacto do perfil inteiro e leva quatro toques. Grid sem nada fixado mostra
o que foi postado por último, que é cara ou coroa.

**4. Destaques.** De quatro a seis, com o nome das perguntas que quem compra faz:
Preços, Resultados, Como funciona, Depoimentos, Sobre mim. Não "Aleatório". Apaga
o resto. No Brasil, um destaque de **Depoimentos** com print de conversa de
cliente (nome borrado, com autorização) costuma ser o mais visto.

**5. O link.** Um destino que bate com o que a bio acabou de prometer. Pode ter
cinco; dois já é cardápio, e cardápio converte menos que porta. No Brasil o link
direto pro WhatsApp, com mensagem pronta (`wa.me/55DDDNUMERO?text=...`),
geralmente é a melhor porta pra quem vende serviço ou produto, porque é onde o
cliente já está. Pra infoproduto, o link vai direto pra página de venda, não pra
um menu.

**6. Capas do grid.** As nove primeiras em miniatura. Capa de Reels se escolhe,
não fica no primeiro frame. Quatro palavras de texto numa capa deixam o grid
legível numa olhada.

## Profissões com regras de publicidade

Se a pessoa é de profissão regulamentada (saúde, psicologia, direito, nutrição,
odontologia), o conselho de classe dela (CFM, CFP/CRP, OAB, CFN, CFO e outros)
tem regras sobre o que pode ir na bio e nos posts: promessa de resultado, antes e
depois, preço, depoimento, título de especialista. Antes de reescrever a bio,
pergunta se ela segue alguma dessas regras e, na dúvida, escreve a versão mais
conservadora e avisa. Isso está no `voice.md`, na seção "Fora dos limites".

## Saída

A tabela de nota, depois as reescritas em blocos prontos pra copiar, na ordem de
correção, cada uma passada pelo `/ig-human`. Dá a nota de novo no fim e mostra a
diferença com honestidade. Se a reescrita chega a 84 e não a 98, diz 84, e diz o
que falta, que normalmente é grid, hábito de story e um post fixado que ainda não
existe. Nada disso é reescrita.

Nada é salvo no Instagram por esta skill. A pessoa edita cada campo.
