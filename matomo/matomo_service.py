from typing import Optional
from datetime import date, timedelta

from compose import compose

from db import bigquery
from matomo.pipeline.interface import Pipeline
from matomo.pipeline import pipelines
from matomo.matomo_repo import get
from tasks import cloud_tasks


def pipeline_service(
    pipeline: Pipeline,
    start: Optional[str],
    end: Optional[str],
) -> int:
    end = date.today().isoformat() if not end else end
    start = (date.today() - timedelta(days=7)).isoformat() if not start else start
    return compose(
        lambda x: {"output_rows": x},
        bigquery.load(pipeline.name, pipeline.schema, pipeline.write_dispotition, pipeline.time_partitioning),
        pipeline.transform,
        get(pipeline.get_options),
    )((1, start, end))


def create_tasks_service() -> dict[str, int]:
    return {
        "tasks": cloud_tasks.create_tasks(
            "matomo",
            [{"table": table} for table in pipelines.keys()],
            lambda x: x["table"],
        )
    }
