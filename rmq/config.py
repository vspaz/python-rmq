from dataclasses import dataclass


@dataclass
class Config:
    host: str = "localhost"
    user: str = "guest"
    password: str = "guest"
    port: str = 5672

    timeout: int = 10
