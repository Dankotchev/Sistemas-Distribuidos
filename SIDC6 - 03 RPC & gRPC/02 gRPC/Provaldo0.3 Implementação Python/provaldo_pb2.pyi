from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ProvaldoRequest(_message.Message):
    __slots__ = ["docn", "doct"]
    DOCN_FIELD_NUMBER: _ClassVar[int]
    DOCT_FIELD_NUMBER: _ClassVar[int]
    docn: str
    doct: int
    def __init__(self, docn: _Optional[str] = ..., doct: _Optional[int] = ...) -> None: ...

class ProvaldoReply(_message.Message):
    __slots__ = ["dtvd", "docn", "doct", "docv"]
    DTVD_FIELD_NUMBER: _ClassVar[int]
    DOCN_FIELD_NUMBER: _ClassVar[int]
    DOCT_FIELD_NUMBER: _ClassVar[int]
    DOCV_FIELD_NUMBER: _ClassVar[int]
    dtvd: str
    docn: str
    doct: int
    docv: int
    def __init__(self, dtvd: _Optional[str] = ..., docn: _Optional[str] = ..., doct: _Optional[int] = ..., docv: _Optional[int] = ...) -> None: ...
