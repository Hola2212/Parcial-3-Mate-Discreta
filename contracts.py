"""Contrato de integración; este módulo no contiene algoritmos RSA."""
from dataclasses import dataclass, field
from typing import Protocol


PENDING = "Lógica RSA pendiente de integrar"


@dataclass(frozen=True)
class EncryptRequest:
    message: str
    p: int
    q: int
    e: int


@dataclass(frozen=True)
class DecryptRequest:
    ciphertext: str
    length: int
    p: int
    q: int
    e: int


@dataclass(frozen=True)
class DetailRow:
    block: int
    characters: str
    ascii_codes: str
    input_block: str
    output_block: str


@dataclass(frozen=True)
class EncryptResult:
    ciphertext: str
    length: int
    public_key: tuple[int, int]
    n: int
    phi: int
    padding_used: bool
    details: list[DetailRow] = field(default_factory=list)


@dataclass(frozen=True)
class DecryptResult:
    message: str
    d: int
    n: int
    phi: int
    padding_removed: bool
    details: list[DetailRow] = field(default_factory=list)


class RSAService(Protocol):
    """El servicio futuro valida toda la matemática y el contenido RSA.

    Debe devolver los resultados tipados o lanzar ValueError con un mensaje
    comprensible para entradas inválidas. No debe acceder a widgets.
    """

    def encrypt(self, request: EncryptRequest) -> EncryptResult: ...

    def decrypt(self, request: DecryptRequest) -> DecryptResult: ...


class PendingRSAService:
    def encrypt(self, request: EncryptRequest) -> EncryptResult:
        raise NotImplementedError(PENDING)

    def decrypt(self, request: DecryptRequest) -> DecryptResult:
        raise NotImplementedError(PENDING)
