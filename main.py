from argparse import ArgumentParser

from configuracoes import TOGGL_ENDPOINTS, configura, carrega_configuracoes
from exceptions import TarefaAtivaException
from mensagem import Payload
from services import GerenciadorTarefas


def inicia_argparser():
    parser = ArgumentParser(prog='toggl-client',
                            description=('Cliente do toggl criado para facilitar a marcacao de'
                                         ' tempo de suas tarefas utilizando a api do toggl'))
    return parser


def adiciona_argumentos(parser):
    parser.add_argument('nome_tarefa', nargs='?', default=None,
                        help='Inicia uma nova tarefa no toogle')
    parser.add_argument('--finalizar', '-f', action='store_true',
                        help='Finaliza a tarefa ativa')
    parser.add_argument('--configurar', action='store_true',
                        help='inicia um ajudante para configurar o cliente')
    parser.add_argument('--branch', '-b', action='store_true',
                        help='Pega o nome da branch ativo para usar como nome da tarefa.')
    parser.add_argument('--tags', '-t', nargs='*',
                        help='Informe o nome do projeto que sera dono dessa tarefa')
    args = parser.parse_args()
    return args


def main():
    parser = inicia_argparser()
    argumentos = adiciona_argumentos(parser)
    if argumentos.configurar:
        configura()
        return
    configuracao = carrega_configuracoes()
    gerenciador = GerenciadorTarefas(argumentos, configuracao)
    if argumentos.finalizar:
        gerenciador.finaliza_tarefa()
        print('Tarefa encerrada')
        return
    if gerenciador.pega_tarefa_ativa():
        raise TarefaAtivaException(('Ja existe uma tarefa ativa, finalize essa tarefa antes de'
                                    ' iniciar outra'))
    payload = Payload(argumentos)
    gerenciador.inicia_tarefa_toggl(TOGGL_ENDPOINTS['INICIAR_CONTADOR'], payload.gera_mensagem())
    print('Tarefa iniciada')


if __name__ == "__main__":
    main()
