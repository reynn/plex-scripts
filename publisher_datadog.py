from datadog import initialize, api
import time


class DatadogMetric:
    def __init__(self):
        super().__init__()


class DatadogPublisher:
    def __init__(self, config):
        self.plex_config = config
        self.metric_prefix = config.datadog_metric_prefix
        options = {
            'api_key': config.datadog_api_token,
            'app_key': config.datadog_app_token
        }
        initialize(**options)

    def send_library_metrics(self, libraries):
        for host, libs in libraries.items():
            metrics = dict()
            for lib_name, lib_items in libs.items():
                n = str(lib_name).lower()
                metrics[f"{self.metric_prefix}.library.{n}"] = len(lib_items)

            print(metrics)

    def send_stream_metrics(self, streams):
        metrics = []
        #     {
        #         "host": host,
        #         "metric": f"{self.metric_prefix}.streams",
        #         "points": [time.time(), len(streams)],
        #         "tags": []
        #     }
        #     for host, streams in dict(streams).items()
        # ]
        # api.Metric.send(metrics)
        for host, stream in dict(streams).items():
            metrics = [
                {
                    "host": host,
                    "metric": f"{self.metric_prefix}.stream",
                    "points": len(stream),
                }
            ]
        print(metrics)
        api.Metric.send(metrics)
