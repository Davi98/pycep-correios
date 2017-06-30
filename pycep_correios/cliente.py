# -*- coding: utf-8 -*-

import re
import requests
import six

from .excecoes import CEPInvalido
from .parser import parse_resposta_com_erro, parse_resposta, monta_requisicao

CARACTERES_NUMERICOS = re.compile(r'[^0-9]')

URL = 'https://apps.correios.com.br/SigepMasterJPA/AtendeClienteService/' \
      'AtendeCliente?wsdl'


def consultar_cep(cep):
    """Retorna o endereço correspondente ao número de CEP informado.

    :param cep: CEP a ser consultado.
    :returns: Dict com os dados do endereço do CEP consultado.
    """

    xml = monta_requisicao(formatar_cep(cep))

    header = {'Content-type': 'text/xml; charset=;%s' % 'utf8'}

    try:
        resposta = requests.post(URL, data=xml, headers=header, verify=False)
    except requests.exceptions.RequestException as e:
        raise e
    else:
        if resposta.ok:
            return parse_resposta(resposta.text)
        else:
            msg = parse_resposta_com_erro(resposta.text)
            raise CEPInvalido(msg)


def formatar_cep(cep):
    """Formata CEP, removendo qualquer caractere nao numerico

    :param cep: CEP a ser formatado
    :returns: string contendo o CEP formatado
    """
    if not isinstance(cep, six.string_types) or not cep:
        raise ValueError('cep deve ser uma string nao vazia contendo somente numeros')
    return CARACTERES_NUMERICOS.sub('', cep)


def validar_cep(cep):
    """Verifica se o CEP informado possui 8 digitos e é constituído apenas de
    números

    :param cep: CEP a ser validado
    :returns: True se o CEP informado é valido. Caso contrário, retorna False
    """
    cep = formatar_cep(cep)
    return cep.isdigit() and len(cep) == 8
