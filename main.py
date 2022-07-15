from typing import Any

from matomo import matomo_service
from matomo.pipeline import pipelines


def main(request):
    data: dict[str, Any] = request.get_json()
    print(data)

    if "tasks" in data:
        response = matomo_service.create_tasks_service()
    elif "table" in data:
        response = matomo_service.pipeline_service(
            pipelines[data["table"]],
            data.get("start"),
            data.get("end"),
        )
    else:
        raise ValueError(data)

    print(response)
    return response
