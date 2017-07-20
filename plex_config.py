import yaml
import os


class PlexConfig:
    _default_yaml = {
        "general": {
            "interval": 10
        },
        "logging": {
            "enabled": True
        },
        "plex": {
            "servers": [],
            "api_token": "",
            "username": "",
            "password": ""
        },
        "influxdb": {
            "server_address": "localhost",
            "port": 8086,
            "database": "",
            "ssl": False,
            "ignore_ssl_check": False
        },
        "datadog": {
            "app_token": "",
            "api_token": "",
            "prefix": "plex"
        }
    }

    def __init__(self, yml=None):
        if yml is not None:
            print(f'Loading config from {yml}')
            self.yml_file = yml
            self._parse_config(self._get_yaml())
        else:
            self._parse_config(self._default_yaml)

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

    def generate_config(self):
        with open('config.yml', 'w') as f:
            f.write(yaml.dump(self._default_yaml, default_flow_style=False))
        print(f"Config file successfully created at {os.path.join(os.getcwd(), 'config.yml')}")
