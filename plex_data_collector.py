import os
from plex_config import PlexConfig
from argparse import ArgumentParser


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
        config = PlexConfig(args.yml_file)

if __name__ == '__main__':
    entry_point()
