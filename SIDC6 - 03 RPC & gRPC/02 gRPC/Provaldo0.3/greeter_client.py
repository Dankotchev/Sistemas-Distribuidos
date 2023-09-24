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


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Will try to greet world ...")
    with grpc.insecure_channel("localhost:1996") as channel:
        stub = provaldo_pb2_grpc.ValidadorStub(channel)
        response = stub.Validar(provaldo_pb2.ProvaldoRequest(docn="437.169.308-30", doct=1))

    print("Documento validade em:", response.dtvd)
    print("Número do Documento:", response.docn)
    print("Tipo do Documento:", response.doct)
    print("Resposta da validação:", response.docv)


if __name__ == "__main__":
    logging.basicConfig()
    run()
