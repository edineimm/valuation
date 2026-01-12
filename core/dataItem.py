from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

class Status(Enum):
    PENDENTE = "PENDENTE"
    COMPLETO = "COMPLETO"
    EXCECAO = "EXCECAO"

@dataclass
class WorkItem:
    id: int
    payload: dict
    status: Status = Status.PENDENTE
    tentativa: int = 0
    erro: str | None = None
    inicio: datetime | None = None
    fim: datetime | None = None
    
    # dados gerados pelo item
    resultado: dict = field(default_factory=dict)
