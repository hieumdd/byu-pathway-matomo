import os

import httpx


def _get_client() -> httpx.Client:
    return httpx.Client(
        base_url="https://analytics.byupw.org/index.php",
        params={"token_auth": os.getenv("MATOMO_TOKEN"), "format": "JSON"},
        follow_redirects=True,
        timeout=None,
    )


def get(get_options: dict[str, str]):
    def _get(options: tuple[int, str, str]):
        id_site, start, end = options
        with _get_client() as client:
            params = {**get_options, "date": f"{start},{end}", "idSite": id_site}
            r = client.get("/", params=params)  # type: ignore
            return r.json()

    return _get
