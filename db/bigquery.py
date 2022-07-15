from datetime import datetime

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


def load(table: str, schema: list[dict]):
    def _load(rows: list[dict]) -> int:
        client = bigquery.Client()

        _schema, _rows = with_batched_at(schema, rows)

        output_rows = (
            client.load_table_from_json(
                _rows,
                f"{DATASET}.p_{table}",
                job_config=bigquery.LoadJobConfig(
                    schema=_schema,
                    create_disposition="CREATE_IF_NEEDED",
                    write_disposition="WRITE_APPEND",
                    time_partitioning=bigquery.TimePartitioning(
                        type_=bigquery.TimePartitioningType.DAY,
                        field="date",
                    ),
                ),
            )
            .result()
            .output_rows
        )

        return output_rows

    return _load
