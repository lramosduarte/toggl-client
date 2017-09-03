from subprocess import getoutput


class Payload:
    CRIADO_COM = 'toggl-client'

    def __init__(self, argumentos):
        self.argumentos = argumentos
        self.mensagem = {
            'time_entry': {
                'created_with': self.CRIADO_COM
            }
        }

    def gera_mensagem(self):
        self.__adiciona_descricao()
        self.__adiciona_tags()
        return self.mensagem

    def __adiciona_descricao(self):
        if self.argumentos.branch:
            nome_branch_ativa = self.__pega_nome_branch_ativa()
            self.mensagem['time_entry']['description'] = nome_branch_ativa
        elif self.argumentos.nome_tarefa:
            self.mensagem['time_entry']['description'] = self.argumentos.nome_tarefa

    def __adiciona_tags(self):
        if self.argumentos.tags:
            self.mensagem['time_entry']['tags'] = self.argumentos.tags

    def __pega_nome_branch_ativa(self):
        saida = getoutput('git branch | grep ^\*')
        nome_branch = saida[2:]
        return nome_branch
