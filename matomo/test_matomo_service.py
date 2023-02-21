import pytest

from matomo.pipeline import pipelines
from matomo import matomo_service

TIMEFRAME = [
    ("auto", (None, None)),
    # ("manual", ("2022-07-15", "2023-02-17")),
]


@pytest.fixture(
    params=[i[1] for i in TIMEFRAME],
    ids=[i[0] for i in TIMEFRAME],
)
def timeframe(request):
    return request.param


class TestMatomo:
    @pytest.fixture( # type: ignore
        params=pipelines.values(),
        ids=pipelines.keys(),
    )
    def pipeline(self, request):
        return request.param

    def test_service(self, pipeline, timeframe):
        res = matomo_service.pipeline_service(pipeline, *timeframe)
        assert res["output_rows"] >= 0


class TestTasks:
    def test_service(self):
        res = matomo_service.create_tasks_service()
        assert res["tasks"] > 0
