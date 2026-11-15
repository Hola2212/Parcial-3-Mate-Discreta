"""Tres cuentas locales de demostración; independientes de la lógica RSA."""
from dataclasses import dataclass


@dataclass(frozen=True)
class DemoUser:
    username: str
    role: str


# Credenciales públicas para explorar la interfaz, no autenticación de producción.
DEMO_ACCOUNTS = {
    "estudiante1": ("rsa2026", "Estudiante"),
    "estudiante2": ("rsa2026", "Estudiante"),
    "admin": ("admin2026", "Administrador"),
}


def authenticate(username: str, password: str) -> DemoUser | None:
    account = DEMO_ACCOUNTS.get(username)
    if account is None or account[0] != password:
        return None
    return DemoUser(username, account[1])


def credentials_help() -> str:
    return "\n".join(f"{username} / {password} · {role}"
                     for username, (password, role) in DEMO_ACCOUNTS.items())
