import os
from time import sleep

from plex_config import PlexConfig
from plex_retriever import PlexRetriever
from publisher_datadog import DatadogPublisher
from publisher_influxdb import InfluxDbPublisher
from argparse import ArgumentParser


def execute_work(yml_file_path):
    config = PlexConfig(yml_file_path)
    retriever = PlexRetriever(config)
    while True:
        # streams = retriever.get_current_streams()
        libraries = retriever.get_library_data()
        if config.datadog_enabled:
            ddog = DatadogPublisher(config)
            # if streams:
            #     ddog.send_stream_metrics(streams)
            if libraries:
                ddog.send_library_metrics(libraries)
        if config.influxdb_enabled:
            infdb = InfluxDbPublisher(config)
        sleep(config.general_interval)


def entry_point():
    parser = ArgumentParser()
    parser.add_argument('-y', '--yml-file',
                        help='Path to the YML file containing settings',
                        default=os.path.join(os.getcwd(), 'config.yml'))
    parser.add_argument('-g', '--generate-config',
                        action='store_true',
                        help='Will create a config.yml file in the current directory',
                        default=False)

    args = parser.parse_args()
    if args.generate_config:
        print('Generating config file')
        PlexConfig().generate_config()
    else:
        execute_work(args.yml_file)

if __name__ == '__main__':
    entry_point()
