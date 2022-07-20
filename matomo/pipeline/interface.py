from typing import Callable, Any, Optional
from dataclasses import dataclass

from google.cloud.bigquery import WriteDisposition, TimePartitioning

Data = list[dict[str, Any]]


@dataclass
class Pipeline:
    name: str
    get_options: Any
    transform: Callable[[Any], list[dict[str, Any]]]
    schema: list[dict[str, Any]]
    write_dispotition: WriteDisposition
    time_partitioning: Optional[TimePartitioning] = None
