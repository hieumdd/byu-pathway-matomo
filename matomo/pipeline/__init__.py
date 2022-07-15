from matomo.pipeline import marketing_campaign_source

pipelines = {
    i.name: i
    for i in [
        j.pipeline  # type: ignore
        for j in [
            marketing_campaign_source,
        ]
    ]
}
