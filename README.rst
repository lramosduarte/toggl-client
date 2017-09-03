Toggle API Client
=======================

Um cliente simples para algumas funcionalidades básicas da api da [TOGGL](https://toggl.com)

#### Configuração inicial

Para o cliente funcionar ele precisa da sua token de acesso, que você encontra nessa [URL](https://toggl.com/app/profile)

***TODO - IMAGEM DO SITE***

Com a token em mãos digita no terminal:
```
    $: tgc --config
```


#### Exemplo

Iniciar uma nova tarefa sem nome:

```
    $: tgc
```
Iniciar uma nova tarefa com nome:

```
    $: tgc 'nome da tarefa'
```
Iniciar uma nova tarefa com a branch ativa como nome:

```
    $: tgc --branch
```

Iniciar uma nova tarefa com tags:

```
    $: tgc --tags 'novatag' 'tagtoog'
```
Finalizar uma tarefa:

```
    $: tgc --finalizar
    $: tgc --f
```

#### TODO

- [x] Iniciar tarefa
- [x] Finalizar tarefa
- [x] Tarefa com nome
- [x] Branch ativa
- [x] tags
- [ ] tests
- [ ] Cache(Diminuir alguns requests e aumentar o desempenho)
    * Foi implementado de algumas funcionalidades
- [x] Arquivo de configuração em pasta do sistema
- [x] SETUP
- [x] PIP install
