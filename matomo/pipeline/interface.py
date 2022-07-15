from typing import Callable, Any
from dataclasses import dataclass

Data = list[dict[str, Any]]


@dataclass
class Pipeline:
    name: str
    get_options: dict[str, str]
    transform: Callable[[dict[str, Any]], list[dict[str, Any]]]
    schema: list[dict[str, Any]]
