from datadog import initialize, api
from plexapi.video import Show
import time
import re


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
        metrics = []
        for host, libs in libraries.items():
            for lib_name, lib_items in libs.items():
                n = re.sub(r'[- ]', '_', str(lib_name).lower())
                metrics.append({
                    "host": host,
                    "metric": f"{self.metric_prefix}.library.{n}",
                    "points": len(lib_items)
                })
                if type(lib_items[0]) is Show:
                    metrics.append({
                        "host": host,
                        "metric": f"{self.metric_prefix}.library.{n}.seasons",
                        "points": sum([x.childCount for x in lib_items])
                    })
                    metrics.append({
                        "host": host,
                        "metric": f"{self.metric_prefix}.library.{n}.episodes",
                        "points": sum([x.leafCount for x in lib_items])
                    })
        print("Library Metrics")
        print(metrics)
        api.Metric.send(metrics)

    def send_stream_metrics(self, streams):
        metrics = []
        for host, stream in dict(streams).items():
            metrics.append([
                {
                    "host": host,
                    "metric": f"{self.metric_prefix}.stream",
                    "points": len(stream),
                }
            ])
        print("Streaming Metrics")
        print(metrics)
        api.Metric.send(metrics)
