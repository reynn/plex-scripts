from datadog import initialize, api


class DatadogMetric():
    def __init__(self) -> None:
        super().__init__()


class DatadogPublisher:
    def __init__(self, config):
        self.plex_config = config
        options = {
            'api_key': config.plex_api_token,
            'app_key': config.plex_app_token
        }
        initialize(**options)

    def send_metric(self, metric):
        if metric is DatadogMetric:
            metric = [metric]
        api.Metric.send(metric)
