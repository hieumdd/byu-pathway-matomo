from google.cloud.bigquery import WriteDisposition

from matomo.pipeline.interface import Pipeline

pipeline = Pipeline(
    name="Goals",
    get_options={
        "module": "API",
        "method": "Goals.getGoals",
    },
    transform=lambda rows: rows,
    schema=[
        {"name": "idsite", "type": "STRING"},
        {"name": "idgoal", "type": "STRING"},
        {"name": "name", "type": "STRING"},
        {"name": "description", "type": "STRING"},
        {"name": "match_attribute", "type": "STRING"},
        {"name": "pattern", "type": "STRING"},
        {"name": "pattern_type", "type": "STRING"},
        {"name": "case_sensitive", "type": "STRING"},
        {"name": "allow_multiple", "type": "STRING"},
        {"name": "revenue", "type": "STRING"},
        {"name": "deleted", "type": "STRING"},
        {"name": "event_value_as_revenue", "type": "STRING"},
    ],
    write_dispotition=WriteDisposition.WRITE_TRUNCATE,
)
