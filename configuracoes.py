import yaml

from exceptions import ArquivoCOnfiguracaoNaoEncontrado


TOGGL_ENDPOINTS = {
    'INICIAR_CONTADOR': 'time_entries/start',
    'ENCERRAR_CONTADOR': 'time_entries/{tarefa_id}/stop',
}

VARIAVEIS_TOGGL = {
    'toggl_api': {
        'token': 'Informe qual a token que sera utilizada pelo client: ',
        'url_base': 'Digite a url da api do toggl: ',
        'usuario': 'Digite o nome do seu usuario: '
    }
}

PATH_ARQUIVO_CONFIGURACAO = 'configuracoes.yml'


def carrega_configuracoes():
    try:
        with open(PATH_ARQUIVO_CONFIGURACAO, 'r') as stream:
            configuracoes = yaml.load(stream)
    except FileNotFoundError:
        raise ArquivoCOnfiguracaoNaoEncontrado(('Arquivo de configuracao nao encontrado, inicie o'
                                               ' programa com o parametro --config'))
    return configuracoes


def configura():
    with open(PATH_ARQUIVO_CONFIGURACAO, 'w') as stream:
        configuracoes = {
            'toggl_api': {var: None for var in VARIAVEIS_TOGGL['toggl_api'].keys()}
        }
        for variavel in configuracoes['toggl_api']:
            valor = input(VARIAVEIS_TOGGL['toggl_api'][variavel])
            configuracoes['toggl_api'][variavel] = valor
        yaml.dump(configuracoes, stream)
    return configuracoes
