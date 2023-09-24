# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Validador client."""

from __future__ import print_function

import logging

import grpc

import provaldo_pb2
import provaldo_pb2_grpc


def valores_doct(doct):
    if doct == 0:
        return 'Não especificado'
    elif doct == 1:
        return 'CPF'
    elif doct == 2:
        return 'CNPJ'
    elif doct == 9:
        return 'Não avaliado'

def valores_docv(docv):
    if docv == 100:
        return 'Documento inválido'
    elif docv == 110:
        return 'Documento válido'
    elif docv == 200:
        return 'Tipo Inválido'
    elif docv == 300:
        return 'Requisição Inválida'
    elif docv == 400:
        return 'Conexões máximas atingidas'
    elif docv == 999:
        return 'Não especificado'


def apresentar_resposta(resposta):
    doct = valores_doct(resposta.doct)
    docv = valores_docv(resposta.docv)

    print("Documento validade em:", resposta.dtvd)
    print("Número do Documento:", resposta.docn)
    print("Tipo do Documento:", doct)
    print("Resposta do servidor:", docv)


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Will try to greet world ...")
    with grpc.insecure_channel("localhost:1996") as channel:
        stub = provaldo_pb2_grpc.ValidadorStub(channel)
        response = stub.Validar(provaldo_pb2.ProvaldoRequest(docn="437.169.308-30", doct=1))
        apresentar_resposta(response)


if __name__ == "__main__":
    logging.basicConfig()
    run()
