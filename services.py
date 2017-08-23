import json
import os
import requests
from requests.auth import HTTPBasicAuth

from configuracoes import TOGGL_ENDPOINTS, PATH_CACHE


def basic_auth(configuracao):
    return HTTPBasicAuth(configuracao['toggl_api']['token'], 'api_token')


class GerenciadorTarefas:

    def __init__(self, argumentos, configuracao):
        self.argumentos = argumentos
        self.configuracao = configuracao

        self.cache = self.ler_cache()

    def pega_tarefa_ativa(self):
        tarefa = self.cache if self.cache else self.pega_tarefa_ativa_toggl()
        try:
            return tarefa['data']['id']
        except TypeError:
            return None

    def finaliza_tarefa(self):
        self._finaliza_tarefa_toggl()
        self._limpa_cache()
        return self.resposta

    def inicie_tarefa(self, endpoint, payload):
        self._inicia_tarefa_toggl(endpoint, payload)
        self._grava_cache()
        return self.resposta

    def ler_cache(self):
        if not os.path.isfile(PATH_CACHE):
            return None
        with open(PATH_CACHE, 'rb') as arquivo_cache:
            stream = arquivo_cache.read()
        return json.loads(stream.decode('utf8'))

    def _finaliza_tarefa_toggl(self):
        tarefa_id = self.pega_tarefa_ativa()
        endpoint = TOGGL_ENDPOINTS['ENCERRAR_CONTADOR'].format(tarefa_id=tarefa_id)
        url = '{url_base}{endpoint}'.format(url_base=self.configuracao['toggl_api']['url_base'],
                                            endpoint=endpoint)
        self.resposta = requests.put(url, auth=basic_auth(self.configuracao))

    def _grava_cache(self):
        with open(PATH_CACHE, 'wb') as arquivo_cache:
            arquivo_cache.write(self.resposta.content)

    def _inicia_tarefa_toggl(self, endpoint, payload):
        url = '{url_base}{endpoint}'.format(url_base=self.configuracao['toggl_api']['url_base'],
                                            endpoint=endpoint)
        self.resposta = requests.post(url, auth=basic_auth(self.configuracao), json=payload)

    def _limpa_cache(self):
        if os.path.isfile(PATH_CACHE):
            os.remove(PATH_CACHE)

    def pega_tarefa_ativa_toggl(self):
        url = '{url_base}{endpoint}'.format(url_base=self.configuracao['toggl_api']['url_base'],
                                            endpoint='time_entries/current')
        self.resposta = requests.get(url, auth=basic_auth(self.configuracao))
        return json.loads(self.resposta.content.decode('utf8'))
