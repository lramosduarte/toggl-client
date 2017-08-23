import json
import requests
from requests.auth import HTTPBasicAuth

from configuracoes import TOGGL_ENDPOINTS


def basic_auth(configuracao):
    return HTTPBasicAuth(configuracao['toggl_api']['token'], 'api_token')


class GerenciadorTarefas:

    def __init__(self, argumentos, configuracao):
        self.argumentos = argumentos
        self.configuracao = configuracao

    def pega_tarefa_ativa(self):
        url = '{url_base}{endpoint}'.format(url_base=self.configuracao['toggl_api']['url_base'],
                                            endpoint='time_entries/current')
        resposta = requests.get(url, auth=basic_auth(self.configuracao))
        tarefa = json.loads(resposta.content.decode('utf8'))
        return tarefa['data']

    def finaliza_tarefa(self):
        tarefa_id = self.pega_tarefa_ativa()
        endpoint = TOGGL_ENDPOINTS['ENCERRAR_CONTADOR'].format(tarefa_id=tarefa_id)
        url = '{url_base}{endpoint}'.format(url_base=self.configuracao['toggl_api']['url_base'],
                                            endpoint=endpoint)
        resposta = requests.put(url, auth=basic_auth(self.configuracao))
        return resposta

    def inicia_tarefa_toggl(self, endpoint, payload):
        url = '{url_base}{endpoint}'.format(url_base=self.configuracao['toggl_api']['url_base'],
                                            endpoint=endpoint)
        resposta = requests.post(url, auth=basic_auth(self.configuracao), json=payload)
        return resposta
