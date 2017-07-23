import plexapi.exceptions
import requests.exceptions
from plexapi.server import PlexServer
from plexapi.myplex import MyPlexAccount


class PlexRetriever:
    def __init__(self, config):
        self.config = config
        if not self.config.plex_token:
            self._get_auth_token()

    def _get_auth_token(self):
        if not self.config.plex_username and not self.config.plex_password:
            print('Please set plex.username and plex.password in the config.yml')
            exit(1)

        print('Retrieving auth token from Plex.tv')
        try:
            try:
                my_plex_account = MyPlexAccount.signin(self.config.plex_username, self.config.plex_password)
                self.config.plex_token = my_plex_account.authenticationToken
                print(f"Welcome {my_plex_account.email}")
            except plexapi.exceptions.NotFound:
                print("Unable to connect to Plex.tv to get auth token")
        except plexapi.exceptions.Unauthorized:
            print(f"Failed to authenticate to Plex.tv with username: {self.config.plex_username}")
            exit(1)

    def get_current_streams(self):
        active_streams = {}
        for server in self.config.plex_server_list:
            try:
                plex_server = PlexServer(f"http://{server}:32400", token=self.config.plex_token)
                if active_streams.get(server) is None:
                    active_streams[server] = []
                for stream in plex_server.sessions():
                    active_streams[server].append(stream)
            except plexapi.exceptions.NotFound:
                print(f"Unable to connect to {server}")
            except requests.exceptions.ConnectionError:
                print(f"Error connecting to {server}")
        return active_streams

    def get_library_data(self):
        lib_data = {}
        for server in self.config.plex_server_list:
            try:
                plex_server = PlexServer(f"http://{server}:32400")
                library_sections = plex_server.library.sections()
                print(f"Retrieved libraries from {server}")
                media_libs = {}
                for lib in library_sections:
                    print(f"Getting library data for {lib.title}")
                    media_libs[lib.title] = lib.all()
                lib_data[server] = media_libs
            except plexapi.exceptions.NotFound:
                print(f"Unable to connect to {server}")
            except requests.exceptions.ConnectionError:
                print(f"Error connecting to {server}")
        return lib_data
