from datetime import datetime
from typing import Optional

from google.cloud import bigquery

DATASET = "Matomo"


def with_batched_at(schema: list[dict], rows: list[dict]):
    return (
        schema + [{"name": "_batched_at", "type": "TIMESTAMP"}],
        [
            {**row, "_batched_at": datetime.utcnow().isoformat(timespec="seconds")}
            for row in rows
        ],
    )


def load(
    table: str,
    schema: list[dict],
    write_disposition: bigquery.WriteDisposition,
    time_partitioning: Optional[bigquery.TimePartitioning],
):
    def _load(rows: list[dict]) -> int:
        client = bigquery.Client()

        _schema, _rows = with_batched_at(schema, rows)

        _table = f"{DATASET}.p_{table}" if time_partitioning else f"{DATASET}.{table}"

        output_rows = (
            client.load_table_from_json(
                _rows,
                _table,
                job_config=bigquery.LoadJobConfig(
                    schema=_schema,
                    create_disposition="CREATE_IF_NEEDED",
                    write_disposition=write_disposition,
                    time_partitioning=time_partitioning,
                ),
            )
            .result()
            .output_rows
        )

        return output_rows

    return _load
