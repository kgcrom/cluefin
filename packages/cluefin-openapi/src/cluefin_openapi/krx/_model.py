from dataclasses import dataclass
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T_KrxHttpBody = TypeVar("T_KrxHttpBody", bound="KrxHttpBody")


@dataclass
class KrxHttpBody:
    pass


@dataclass
class KrxHttpResponse(Generic[T_KrxHttpBody]):
    body: T_KrxHttpBody
