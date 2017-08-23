## Toggl-Client

toggl-client é um cliente CLI para a api do [TOGGL](https://toggl.com/).


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
- [ ] Arquivo de configuração em pasta do sistema
- [ ] SETUP
- [ ] PIP install
