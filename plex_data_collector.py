import os
import yaml
from argparse import ArgumentParser


class PlexConfig:
    def __init__(self, yml):
        print(f'Loading config from {yml}')
        self.yml_file = yml
        self._parse_config(self._get_yaml())

    def _get_yaml(self):
        with open(self.yml_file, 'r') as yf:
            return yaml.load(yf.read())

    def _parse_config(self, yml_dict):
        # General Settings
        self.general_interval = yml_dict.get('general').get('interval')

        # Logging Settings
        self.logging_enabled = yml_dict.get('logging').get('enabled')

        # Datadog Settings
        self.datadog_app_token = yml_dict.get('datadog').get('app_token')
        self.datadog_api_token = yml_dict.get('datadog').get('api_token')
        self.datadog_metric_prefix = yml_dict.get('datadog').get('prefix')

        # Plex Settings
        self.plex_server_list = yml_dict.get('plex').get('servers')
        self.plex_api_token = yml_dict.get('plex').get('api_token')
        self.plex_username = yml_dict.get('plex').get('username')
        self.plex_password = yml_dict.get('plex').get('password')

        # InfluxDB Settings
        self.influxdb_server_address = yml_dict.get('influxdb').get('server_address')
        self.influxdb_port = yml_dict.get('influxdb').get('port')
        self.influxdb_database = yml_dict.get('influxdb').get('database')
        self.influxdb_ssl = yml_dict.get('influxdb').get('ssl')
        self.influxdb_ignore_ssl_check = yml_dict.get('influxdb').get('ignore_ssl_check')


def entry_point():
    parser = ArgumentParser()
    parser.add_argument('-y', '--yml-file',
                        help='Path to the YML file containing settings',
                        default=os.path.join(os.getcwd(), 'config.yml'))

    args = parser.parse_args()
    config = PlexConfig(args.yml_file)
    print(config.plex_api_token)
    print(f"Hello {os.getenv('HOSTNAME')}")

if __name__ == '__main__':
    entry_point()
