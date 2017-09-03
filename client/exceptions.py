class TogglClientException(Exception):
    pass


class ArquivoCOnfiguracaoNaoEncontrado(TogglClientException):
    pass


class TarefaAtivaException(TogglClientException):
    pass
