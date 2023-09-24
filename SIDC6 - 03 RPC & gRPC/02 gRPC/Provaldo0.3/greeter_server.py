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
"""The Python implementation of the GRPC helloworld.Validador server."""

from concurrent import futures
import logging
import datetime

import grpc

import provaldo_pb2
import provaldo_pb2_grpc


class Validador(provaldo_pb2_grpc.ValidadorServicer):
    def Validar(self, request, context):
        data_validacao = datetime.datetime.now()
        if request.doct == 1:
            docv = valida_cpf(request.docn)
        elif request.doct == 2:
            docv = valida_cnpj(request.docn)
        else:
            docv = 200

        return provaldo_pb2.ProvaldoReply(dtvd=data_validacao.strftime("%Y-%m-%d %H:%M:%S"),
                                          docn=request.docn,
                                          doct=request.doct,
                                          docv=docv)


def valida_cpf(cpf):
    # Remova caracteres não numéricos do CPF
    cpf = ''.join(filter(str.isdigit, cpf))

    # Verifique se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return 100

    # Verifique se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return 100

    # Calcule o primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = soma % 11
    if resto < 2:
        digito_verificador1 = 0
    else:
        digito_verificador1 = 11 - resto

    # Verifique o primeiro dígito verificador
    if digito_verificador1 != int(cpf[9]):
        return 100

    # Calcule o segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = soma % 11
    if resto < 2:
        digito_verificador2 = 0
    else:
        digito_verificador2 = 11 - resto

    # Verifique o segundo dígito verificador
    if digito_verificador2 != int(cpf[10]):
        return 100

    return 110


def valida_cnpj(cnpj):
    # Remove caracteres não numéricos do CNPJ
    cnpj = ''.join(filter(str.isdigit, cnpj))

    # Verifique se o CNPJ tem 14 dígitos
    if len(cnpj) != 14:
        return 100

    # Verifique se todos os dígitos são iguais
    if cnpj == cnpj[0] * 14:
        return 100

    # Calcula o primeiro dígito verificador
    soma = 0
    peso = 5
    for i in range(12):
        soma += int(cnpj[i]) * peso
        peso -= 1
        if peso == 1:
            peso = 9
    resto = soma % 11
    if resto < 2:
        digito_verificador1 = 0
    else:
        digito_verificador1 = 11 - resto

    # Verifique o primeiro dígito verificador
    if digito_verificador1 != int(cnpj[12]):
        return 100

    # Calcula o segundo dígito verificador
    soma = 0
    peso = 6
    for i in range(13):
        soma += int(cnpj[i]) * peso
        peso -= 1
        if peso == 1:
            peso = 9
    resto = soma % 11
    if resto < 2:
        digito_verificador2 = 0
    else:
        digito_verificador2 = 11 - resto

    # Verifique o segundo dígito verificador
    if digito_verificador2 != int(cnpj[13]):
        return 100

    return 110


def serve():
    port = "1996"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    provaldo_pb2_grpc.add_ValidadorServicer_to_server(Validador(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
