import arrow
import csv
import json
import os
import requests
from requests.auth import HTTPBasicAuth

from .configuracoes import TOGGL_ENDPOINTS, PATH_CACHE


def basic_auth(configuracao):
    return HTTPBasicAuth(configuracao['toggl_api']['token'], 'api_token')


class GerenciadorTarefas:

    def __init__(self, configuracao):
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

    def normaliza_data(self, periodo):
        if periodo:
            datas = str(periodo).split('-')
            data_inicio = arrow.get(datas[0], 'DD/MM/YYYY').to('America/Sao_Paulo')
            data_fim = arrow.get(datas[1], 'DD/MM/YYYY').to('America/Sao_Paulo')
        if not periodo:
            data_inicio = arrow.now().replace(hour=0, minute=0, second=0)
            data_fim = data_inicio.replace(hour=23, minute=59, second=59)
        return data_inicio.isoformat(), data_fim.isoformat()

    def pega_tarefa_ativa_toggl(self):
        url = '{url_base}{endpoint}'.format(url_base=self.configuracao['toggl_api']['url_base'],
                                            endpoint='time_entries/current')
        self.resposta = requests.get(url, auth=basic_auth(self.configuracao))
        return json.loads(self.resposta.content.decode('utf8'))

    def relatorio_tarefas(self, periodo):
        data_inicio, data_fim = self.normaliza_data(periodo)
        self._relatorio_tarefas_toggl(data_inicio, data_fim)
        return json.loads(self.resposta.content.decode('utf8'))

    def _relatorio_tarefas_toggl(self, data_inicio, data_fim):
        endpoint = TOGGL_ENDPOINTS['LISTAR_ENTRADAS_TEMPO'].format(inicio=data_inicio, fim=data_fim)
        url = '{url_base}{endpoint}'.format(url_base=self.configuracao['toggl_api']['url_base'],
                                            endpoint=endpoint)
        self.resposta = requests.get(url, auth=basic_auth(self.configuracao))

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


class GeraArquivoCsv:

    MAPEAMENTO_CAMPOS = {
        'Data': 'start',
        'Descrição': 'description',
        'Inicio': 'start',
        'Fim': 'stop',
    }

    def __init__(self, dicionarios):
        """Gera um arquivo csv a partir de uma lista de dicionários, opcionalmente você pode
        informar uma tupla de chaves que pode ser usada para gerar o arquivo csv de acordo
        a essa tupla.

        Args:
            dicionarios (list(dict)): Dados que vão ser utilizados
            campos (tuple)(OPCIONAL): Tupla contendo lista de chaves que serão as colunas do
                arquivo csv.
        """
        self.dicionarios = dicionarios

    def gera_arquivo(self):
        arquivo_csv = open('relatorio.csv', 'w+')
        self._escreve_arquivo(arquivo_csv)
        arquivo_csv.close()

    def _escreve_arquivo(self, arquivo_csv):
        writer = csv.DictWriter(arquivo_csv, fieldnames=('Data', 'Descrição', 'Inicio', 'Fim'))
        writer.writeheader()
        for dicionario in self.dicionarios:
            dados = self._pega_dados_dicionario(dicionario)
            writer.writerow(dados)

    def _extrai_dia(self, datetime_str):
        datetime_brasil = arrow.get(datetime_str).to('America/Sao_Paulo')
        return str(datetime_brasil.strftime('%d/%m/%Y'))

    def _extrai_tempo(self, datetime_str):
        datetime_brasil = arrow.get(datetime_str).to('America/Sao_Paulo')
        return str(datetime_brasil.time())

    def _pega_dados_dicionario(self, dicionario):
        dados = {}
        for chave, valor in self.MAPEAMENTO_CAMPOS.items():
            if chave == 'Data':
                dados[chave] = self._extrai_dia(dicionario[valor])
            elif chave in ('Inicio', 'Fim'):
                dados[chave] = self._extrai_tempo(dicionario[valor])
            else:
                try:
                    dados[chave] = dicionario[valor]
                except KeyError:
                    dados[chave] = 'sem valor informado para %s' % valor
        return dados
