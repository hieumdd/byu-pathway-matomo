from typing import Any

import dateparser

from matomo.pipeline.interface import Pipeline


def parse_date(date_str: str):
    dt = dateparser.parse(date_str)
    return dt.date().isoformat() if dt else None


def split_goal_id(goal: str):
    key, value = goal.split("=")
    return {key: value}


def transform(res: dict[str, Any]):
    data = res["reportData"]

    with_dates = [
        {**row, "date": parse_date(key)}
        for key, values in data.items()
        for row in values
    ]

    with_goals = [
        {
            **row,
            "goals": [
                {**value, **split_goal_id(key)}
                for key, value in row.get("goals", {}).items()
            ],
        }
        for row in with_dates
    ]

    return with_goals


pipeline = Pipeline(
    name="MarketingCampaignSource",
    get_options={
        "module": "API",
        "method": "API.getProcessedReport",
        "period": "day",
        "apiModule": "MarketingCampaignsReporting",
        "apiAction": "getSource",
        "hideMetricsDoc": "1",
        "showRawMetrics": "true",
    },
    transform=transform,
    schema=[
        {"name": "label", "type": "STRING"},
        {"name": "nb_uniq_visitors", "type": "NUMERIC"},
        {"name": "nb_visits", "type": "NUMERIC"},
        {"name": "nb_actions", "type": "NUMERIC"},
        {"name": "nb_users", "type": "NUMERIC"},
        {"name": "max_actions", "type": "NUMERIC"},
        {"name": "sum_visit_length", "type": "NUMERIC"},
        {"name": "bounce_count", "type": "NUMERIC"},
        {"name": "nb_visits_converted", "type": "NUMERIC"},
        {
            "name": "goals",
            "type": "RECORD",
            "mode": "REPEATED",
            "fields": [
                {"name": "idgoal", "type": "NUMERIC"},
                {"name": "nb_conversions", "type": "NUMERIC"},
                {"name": "nb_visits_converted", "type": "NUMERIC"},
                {"name": "revenue", "type": "NUMERIC"},
            ],
        },
        {"name": "nb_conversions", "type": "NUMERIC"},
        {"name": "revenue", "type": "STRING"},
        {"name": "conversion_rate", "type": "STRING"},
        {"name": "nb_actions_per_visit", "type": "NUMERIC"},
        {"name": "avg_time_on_site", "type": "STRING"},
        {"name": "bounce_rate", "type": "STRING"},
        {"name": "date", "type": "DATE"},
    ],
)
