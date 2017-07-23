import yaml
import os


class PlexConfig:
    _default_yml = {
        "general": {
            "interval": 10
        },
        "logging": {
            "enabled": True
        },
        "plex": {
            "servers": [],
            "token": "",
            "username": "",
            "password": ""
        },
        "influxdb": {
            "enabled": False,
            "server_address": "localhost",
            "port": 8086,
            "database": "",
            "ssl": False,
            "ignore_ssl_check": False
        },
        "datadog": {
            "enabled": False,
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
            self._parse_config(self._default_yml)

    def _get_yaml(self):
        try:
            with open(self.yml_file, 'r') as yf:
                return yaml.load(yf.read())
        except FileNotFoundError:
            print("Unable to load config")
            self._parse_config(self._default_yml)

    def _parse_config(self, yml_dict):
        # General Settings
        self.general_interval = os.getenv('GENERAL_INTERVAL', yml_dict.get('general').get('interval'))

        # Logging Settings
        self.logging_enabled = os.getenv('LOGGING_ENABLED', yml_dict.get('logging').get('enabled', False))

        # Datadog Settings
        self.datadog_enabled = os.getenv('DATADOG_ENABLED', yml_dict.get('datadog').get('enabled', False))
        self.datadog_app_token = os.getenv('DATADOG_APP_TOKEN', yml_dict.get('datadog').get('app_token'))
        self.datadog_api_token = os.getenv('DATADOG_API_TOKEN', yml_dict.get('datadog').get('api_token'))
        self.datadog_metric_prefix = os.getenv('DATADOG_METRIC_PREFIX', yml_dict.get('datadog').get('prefix'))

        # Plex Settings
        self.plex_server_list = os.getenv('PLEX_SERVERS', yml_dict.get('plex').get('servers'))
        if self.plex_server_list is str:
            self.plex_server_list = str(self.plex_server_list).split(',')
        self.plex_token = os.getenv('PLEX_TOKEN', yml_dict.get('plex').get('token'))
        self.plex_username = os.getenv('PLEX_USERNAME', yml_dict.get('plex').get('username'))
        self.plex_password = os.getenv('PLEX_PASSWORD', yml_dict.get('plex').get('password'))

        # InfluxDB Settings
        self.influxdb_enabled = os.getenv('INFLUXDB_ENABLED', yml_dict.get('influxdb').get('enabled', False))
        self.influxdb_server_address = os.getenv('INFLUXDB_SERVER_ADDRESS',
                                                 yml_dict.get('influxdb').get('server_address'))
        self.influxdb_port = os.getenv('INFLUXDB_PORT', yml_dict.get('influxdb').get('port'))
        self.influxdb_database = os.getenv('INFLUXDB_DATABASE', yml_dict.get('influxdb').get('database'))
        self.influxdb_ssl = os.getenv('INFLUXDB_SSL', yml_dict.get('influxdb').get('ssl'))
        self.influxdb_ignore_ssl_check = os.getenv('INFLUXDB_IGNORE_SSL_CHECK',
                                                   yml_dict.get('influxdb').get('ignore_ssl_check'))

    def generate_config(self):
        with open('config.yml', 'w') as f:
            f.write(yaml.dump(self._default_yaml, default_flow_style=False))
        print(f"Config file successfully created at {os.path.join(os.getcwd(), 'config.yml')}")
